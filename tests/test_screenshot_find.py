import json

from angles_python_client.http import AnglesHttpClient
from angles_python_client.requests import ScreenshotRequests
from angles_python_client.models import FindImageOptions


class _FakeResponse:
    status_code = 200

    def __init__(self, body):
        self.content = json.dumps(body).encode()
        self._body = body

    def json(self):
        return self._body


class _RecordingSession:
    """Stands in for requests.Session and records the kwargs of each request."""

    def __init__(self, body=None):
        self.calls = []
        self._body = body or {"matches": [], "bestMatch": None}

    def request(self, **kwargs):
        self.calls.append(kwargs)
        return _FakeResponse(self._body)


def _client(session):
    return AnglesHttpClient(base_url="https://angles.example/rest/api/v1.0/", session=session)


def test_find_image_in_screenshot_builds_params_and_url():
    session = _RecordingSession({"matches": [{"x": 1}], "bestMatch": {"x": 1}})
    requests_client = ScreenshotRequests(_client(session))

    options = FindImageOptions(minConfidence=0.9, maxMatches=3, grayscale=True)
    result = requests_client.find_image_in_screenshot("aaa", "bbb", options)

    call = session.calls[0]
    assert call["url"].endswith("screenshot/aaa/find/bbb")
    assert call["params"] == {"minConfidence": 0.9, "maxMatches": 3, "grayscale": "true"}
    assert result["bestMatch"] == {"x": 1}


def test_find_image_options_are_optional():
    session = _RecordingSession()
    requests_client = ScreenshotRequests(_client(session))

    requests_client.find_image_in_screenshot("aaa", "bbb")

    assert session.calls[0]["params"] is None


def test_find_uploaded_image_drops_json_content_type(tmp_path):
    template = tmp_path / "template.png"
    template.write_bytes(b"not-really-a-png")
    session = _RecordingSession()
    requests_client = ScreenshotRequests(_client(session))

    requests_client.find_uploaded_image_in_screenshot("aaa", str(template))

    call = session.calls[0]
    assert call["url"].endswith("screenshot/aaa/find")
    assert "template" in call["files"]
    # The default JSON content type must not leak into multipart uploads: it would
    # override the multipart boundary and make the body unreadable by the server.
    assert "Content-Type" not in call["headers"]


def test_save_screenshot_multipart_also_drops_json_content_type(tmp_path):
    screenshot = tmp_path / "screenshot.png"
    screenshot.write_bytes(b"not-really-a-png")
    session = _RecordingSession({"_id": "abc"})
    requests_client = ScreenshotRequests(_client(session))

    requests_client.save_screenshot({
        "buildId": "bbb",
        "view": "some-view",
        "timestamp": "2026-01-01T00:00:00Z",
        "filePath": str(screenshot),
    })

    call = session.calls[0]
    assert "screenshot" in call["files"]
    assert "Content-Type" not in call["headers"]


PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 16


def _save_screenshot(tmp_path, name, content):
    screenshot = tmp_path / name
    screenshot.write_bytes(content)
    session = _RecordingSession({"_id": "abc"})
    ScreenshotRequests(_client(session)).save_screenshot({
        "buildId": "bbb",
        "view": "some-view",
        "timestamp": "2026-01-01T00:00:00Z",
        "filePath": str(screenshot),
    })
    return session.calls[0]["files"]["screenshot"]


def test_save_screenshot_sends_image_content_type(tmp_path):
    # The server rejects screenshot uploads whose part type is not an image type.
    file_name, _, content_type = _save_screenshot(tmp_path, "screenshot.png", PNG_BYTES)
    assert file_name == "screenshot.png"
    assert content_type == "image/png"


def test_save_screenshot_content_type_comes_from_the_file_bytes(tmp_path):
    _, _, content_type = _save_screenshot(tmp_path, "screenshot.png", JPEG_BYTES)
    assert content_type == "image/jpeg"

    _, _, content_type = _save_screenshot(tmp_path, "screenshot", PNG_BYTES)
    assert content_type == "image/png"


def test_save_screenshot_content_type_falls_back_to_the_extension(tmp_path):
    _, _, content_type = _save_screenshot(tmp_path, "screenshot.jpg", b"unrecognised")
    assert content_type == "image/jpeg"


def test_save_screenshot_uploads_the_whole_file(tmp_path):
    # Sniffing the header must not leave the file positioned past it.
    screenshot = tmp_path / "screenshot.png"
    screenshot.write_bytes(PNG_BYTES)
    uploaded = []

    class _ReadingSession(_RecordingSession):
        def request(self, **kwargs):
            uploaded.append(kwargs["files"]["screenshot"][1].read())
            return super().request(**kwargs)

    ScreenshotRequests(_client(_ReadingSession({"_id": "abc"}))).save_screenshot({
        "buildId": "bbb",
        "view": "some-view",
        "timestamp": "2026-01-01T00:00:00Z",
        "filePath": str(screenshot),
    })

    assert uploaded == [PNG_BYTES]


def test_find_uploaded_image_sends_image_content_type(tmp_path):
    template = tmp_path / "template.jpeg"
    template.write_bytes(JPEG_BYTES)
    session = _RecordingSession()

    ScreenshotRequests(_client(session)).find_uploaded_image_in_screenshot("aaa", str(template))

    assert session.calls[0]["files"]["template"][2] == "image/jpeg"
