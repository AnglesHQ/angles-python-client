import pytest

from angles_python_client.reporter import AnglesReporter


class _RecordingAttachmentRequests:
    def __init__(self):
        self.uploads = []

    def _stored(self, build_id, file_name):
        attachment_id = f"attachment-{len(self.uploads) + 1}"
        self.uploads.append((build_id, file_name))
        return {"_id": attachment_id, "originalName": file_name, "kind": "log"}

    def upload_test_attachment(self, build_id, file_path, file_name=None):
        return self._stored(build_id, file_name or file_path.rsplit("/", 1)[-1])

    def upload_test_attachment_data(self, build_id, data, file_name):
        return self._stored(build_id, file_name)


class _RecordingExecutionRequests:
    def __init__(self):
        self.saved = []

    def save_execution(self, execution):
        self.saved.append(execution)
        return {"_id": "execution-id"}


def _reporter():
    reporter = AnglesReporter(base_url="https://angles.example/rest/api/v1.0/")
    reporter.attachments = _RecordingAttachmentRequests()
    reporter.executions = _RecordingExecutionRequests()
    reporter.set_current_build("build-id")
    return reporter


def test_attach_file_adds_the_id_to_the_current_test():
    reporter = _reporter()
    reporter.start_test("test-one", "suite-one")

    first = reporter.attach_file("/tmp/videos/checkout.webm")
    second = reporter.attach_data("one\ntwo\n", "console.log")
    reporter.save_test()

    saved = reporter.executions.saved[0]
    assert saved.attachments == [first["_id"], second["_id"]]
    assert reporter.attachments.uploads == [("build-id", "checkout.webm"), ("build-id", "console.log")]


def test_attach_to_last_step_adds_the_id_to_that_step_only():
    reporter = _reporter()
    reporter.start_test("test-one", "suite-one")
    reporter.add_action("Pay")
    reporter.pass_step("Open page", "200", "200", "")
    reporter.fail_step("Confirmation", "Order confirmed", "Declined", "")

    html = reporter.attach_data_to_last_step("<html></html>", "page.html")
    png = reporter.attach_file_to_last_step("/tmp/failure.png")

    steps = reporter.current_action.steps
    assert steps[0].attachments is None
    assert steps[1].attachments == [html["_id"], png["_id"]]
    assert reporter.current_execution.attachments is None


def test_attachments_are_serialised_with_the_execution():
    from angles_python_client._serialize import jsonable

    reporter = _reporter()
    reporter.start_test("test-one", "suite-one")
    reporter.info("collecting")
    reporter.attach_data_to_last_step("x", "page.html")
    reporter.attach_file("/tmp/trace.zip")

    body = jsonable(reporter.current_execution)
    assert body["attachments"] == ["attachment-2"]
    assert body["actions"][0]["steps"][0]["attachments"] == ["attachment-1"]


def test_attachments_survive_batch_mode():
    reporter = _reporter()
    reporter.set_batch_mode(True)
    reporter.start_test("test-one", "suite-one")
    reporter.attach_file("/tmp/network.har")
    reporter.save_test()

    assert reporter._batched_executions[0].attachments == ["attachment-1"]


def test_attaching_needs_a_started_test():
    reporter = _reporter()
    with pytest.raises(RuntimeError, match="start_test"):
        reporter.attach_file("/tmp/console.log")
    assert reporter.attachments.uploads == []


def test_attaching_to_a_step_needs_a_step():
    reporter = _reporter()
    reporter.start_test("test-one", "suite-one")
    with pytest.raises(RuntimeError, match="add a step"):
        reporter.attach_file_to_last_step("/tmp/console.log")
    assert reporter.attachments.uploads == []
