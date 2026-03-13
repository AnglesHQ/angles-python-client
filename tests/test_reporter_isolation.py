from angles_python_client.reporter import AnglesReporter, angles_reporter


def test_get_instance_returns_singleton():
    a = AnglesReporter.get_instance()
    b = AnglesReporter.get_instance()
    assert a is b
    assert a is angles_reporter


def test_get_instance_with_base_url_returns_fresh_reporters():
    a = AnglesReporter.get_instance_with_base_url("https://angles-a.example/rest/api/v1.0/")
    b = AnglesReporter.get_instance_with_base_url("https://angles-b.example/rest/api/v1.0/")

    assert a is not b
    assert a.http.base_url == "https://angles-a.example/rest/api/v1.0/"
    assert b.http.base_url == "https://angles-b.example/rest/api/v1.0/"


def test_direct_instances_keep_independent_state():
    a = AnglesReporter(base_url="https://angles.example/rest/api/v1.0/")
    b = AnglesReporter(base_url="https://angles.example/rest/api/v1.0/")

    a.set_current_build("build-a")
    b.set_current_build("build-b")

    assert a is not b
    assert a.current_build["_id"] == "build-a"
    assert b.current_build["_id"] == "build-b"
