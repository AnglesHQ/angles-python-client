import pytest

from angles_python_client.reporter import AnglesReporter


class _RecordingExecutionRequests:
    def __init__(self):
        self.saved = []

    def save_execution(self, execution):
        self.saved.append(execution)
        return {"_id": "execution-id"}


class _RecordingBuildRequests:
    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def add_executions(self, build_id, executions):
        self.calls.append((build_id, executions))
        if self.error:
            raise self.error
        return {"_id": build_id, "suites": [{"executions": executions}]}


def _reporter_with_stubs(build_requests=None):
    reporter = AnglesReporter(base_url="https://angles.example/rest/api/v1.0/")
    reporter.executions = _RecordingExecutionRequests()
    reporter.builds = build_requests or _RecordingBuildRequests()
    reporter.set_current_build("build-id")
    return reporter


def test_save_test_sends_immediately_by_default():
    reporter = _reporter_with_stubs()
    reporter.start_test("test-one", "suite-one")
    result = reporter.save_test()

    assert result == {"_id": "execution-id"}
    assert len(reporter.executions.saved) == 1
    assert reporter.builds.calls == []


def test_batch_mode_gathers_executions_until_save_all_tests():
    reporter = _reporter_with_stubs()
    reporter.set_batch_mode(True)

    reporter.start_test("test-one", "suite-one")
    assert reporter.save_test() is None
    reporter.start_test("test-two", "suite-two")
    assert reporter.save_test() is None

    # nothing has been sent yet
    assert reporter.executions.saved == []
    assert reporter.builds.calls == []

    updated_build = reporter.save_all_tests()

    assert len(reporter.builds.calls) == 1
    build_id, executions = reporter.builds.calls[0]
    assert build_id == "build-id"
    assert [execution.title for execution in executions] == ["test-one", "test-two"]
    assert updated_build["_id"] == "build-id"
    assert reporter.current_build == updated_build

    # the batch is cleared, so calling again is a no-op
    assert reporter.save_all_tests() == updated_build
    assert len(reporter.builds.calls) == 1


def test_save_all_tests_keeps_executions_on_failure():
    reporter = _reporter_with_stubs(_RecordingBuildRequests(error=RuntimeError("angles is down")))
    reporter.set_batch_mode(True)

    reporter.start_test("test-one", "suite-one")
    reporter.save_test()

    with pytest.raises(RuntimeError, match="angles is down"):
        reporter.save_all_tests()

    # the executions are retained so a retry doesn't lose them
    reporter.builds.error = None
    updated_build = reporter.save_all_tests()
    assert len(reporter.builds.calls) == 2
    assert updated_build["_id"] == "build-id"


def test_save_all_tests_without_build_raises():
    reporter = AnglesReporter(base_url="https://angles.example/rest/api/v1.0/")
    reporter.executions = _RecordingExecutionRequests()
    reporter.set_batch_mode(True)
    reporter.set_current_build("build-id")
    reporter.start_test("test-one", "suite-one")
    reporter.save_test()
    reporter.current_build = None

    with pytest.raises(RuntimeError, match="No current build set"):
        reporter.save_all_tests()


def test_reset_state_clears_batched_executions():
    reporter = _reporter_with_stubs()
    reporter.set_batch_mode(True)
    reporter.start_test("test-one", "suite-one")
    reporter.save_test()

    reporter.reset_state()
    reporter.set_current_build("build-id")

    assert reporter.save_all_tests() == {"_id": "build-id"}
    assert reporter.builds.calls == []
