from angles_python_client.http import AnglesHttpClient
from angles_python_client.requests import ScreenshotRequests
from angles_python_client.models import CompareOptions

from test_screenshot_find import _RecordingSession


def _requests(session):
    http = AnglesHttpClient(base_url="https://angles.example/rest/api/v1.0/", session=session)
    return ScreenshotRequests(http)


def test_compare_screenshots_builds_params():
    session = _RecordingSession({"algorithm": "ssim", "ssim": 0.99})
    requests_client = _requests(session)

    options = CompareOptions(algorithm="ssim", threshold=0.2, regions=True)
    result = requests_client.compare_screenshots("aaa", "bbb", options)

    call = session.calls[0]
    assert call["url"].endswith("screenshot/aaa/compare/bbb")
    assert call["params"] == {"algorithm": "ssim", "threshold": 0.2, "regions": "true"}
    assert result["algorithm"] == "ssim"


def test_compare_options_are_optional():
    session = _RecordingSession()
    requests_client = _requests(session)

    requests_client.compare_screenshots("aaa", "bbb")

    assert session.calls[0]["params"] is None


def test_baseline_compare_passes_algorithm_and_cache():
    session = _RecordingSession()
    requests_client = _requests(session)

    requests_client.get_baseline_compare_image("aaa", cache=True, options=CompareOptions(algorithm="ssim"))

    call = session.calls[0]
    assert call["url"].endswith("screenshot/aaa/baseline/compare/image/")
    assert call["params"] == {"useCache": "true", "algorithm": "ssim"}
