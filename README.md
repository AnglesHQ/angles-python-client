# angles-python-client

A small Python client for the **Angles Dashboard** REST API, which allows python test frameworks to publish their automated test results.

## Install (local / editable)

```bash
pip install -e .
```

## Quick usage (singleton reporter)

Use `angles_reporter` when you want one simple process-wide reporter. This mirrors the original JS-style convenience usage and remains backward compatible.

```python
from angles_python_client import angles_reporter
from angles_python_client.models import Artifact, ScreenshotPlatform, Platform

angles_reporter.set_base_url("http://127.0.0.1:3000/rest/api/v1.0/")

build = angles_reporter.start_build(
    name="TestRunName",
    team="Team",
    environment="Environment",
    component="Component",
    phase="optional-phase",
)

angles_reporter.add_artifacts([
    Artifact(groupId="angles-ui", artifactId="anglesHQ", version="1.0.0")
])

angles_reporter.start_test(title="test1", suite="suite1")
angles_reporter.add_action("My first action")

platform = ScreenshotPlatform(
    platformName="Android",
    platformVersion="10",
    browserName="Chrome",
    browserVersion="89.0",
    deviceName="Samsung Galaxy S9",
)

screenshot = angles_reporter.save_screenshot_with_platform(
    file_path="/path/to/screenshot.png",
    view="view_1",
    tags=["smoke", "home"],
    platform=platform,
)

angles_reporter.info_with_screenshot("Checking my view on android", screenshot.get("_id"))

angles_reporter.pass_step("Assertion", expected="true", actual="true", info="Just doing an assertion")
angles_reporter.fail_step("Assertion", expected="true", actual="false", info="Just doing an assertion")

execution = angles_reporter.save_test()
```


## Independent reporters for isolated state

Create `AnglesReporter(...)` instances directly when you need more than one live reporter at once, for example when publishing multiple builds or environments in parallel. Each instance keeps its own `current_build`, `current_execution`, and `current_action` state.

```python
from angles_python_client import AnglesReporter

reporter_gib = AnglesReporter(base_url="https://angles-api.example/rest/api/v1.0/")
reporter_games_dev = AnglesReporter(base_url="https://angles-api.example/rest/api/v1.0/")

reporter_gib.start_build(
    name="[suite] test-suite integration",
    team="some-team",
    environment="integration",
    component="some-component",
)

reporter_games_dev.start_build(
    name="[suite] test-suite dev",
    team="some-team",
    environment="dev",
    component="some-component",
)
```

`AnglesReporter.get_instance()` and the module-level `angles_reporter` still return the shared convenience singleton.

`AnglesReporter.get_instance_with_base_url(...)` is kept for backward compatibility, but it now returns a fresh reporter bound to that base URL instead of reusing shared mutable reporting state.

## Direct requests usage

```python
from angles_python_client import AnglesHttpClient
from angles_python_client.requests import BuildRequests

http = AnglesHttpClient(base_url="http://127.0.0.1:3000/rest/api/v1.0/")
builds = BuildRequests(http)
build = builds.get_build("your-build-id")
```


### Publish a release to PyPI

1. Bump `project.version` in `pyproject.toml`
2. Push a tag like `v1.0.1`:

   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

The workflow `.github/workflows/publish.yml` will build and publish to PyPI.

### Publish to TestPyPI first (optional)

- Push a tag like `test-v1.0.1`, or run the `Publish to TestPyPI` workflow manually.
- Install from TestPyPI to validate:

  ```bash
  python -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple angles-python-client
  ```

### Build locally (manual)

```bash
python -m pip install -U pip build twine
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```


## Versioning

This project uses a standard `pyproject.toml` `version = "X.Y.Z"` field.

### Bump version locally (and create a tag)

```bash
pip install -U bump2version
bump2version patch   # or minor / major
git push --follow-tags
```

### Bump via GitHub Actions (and publish)

Run the **Bump version and tag** workflow (Actions tab) and choose:

- `target=pypi` → creates a tag like `v1.0.1` (triggers the PyPI publish workflow)
- `target=testpypi` → creates a tag like `test-v1.0.1` (triggers the TestPyPI publish workflow)


## Auto-release on main/master

This repo includes an **optional** workflow: `.github/workflows/release-on-main.yml`.

When enabled (it is committed by default), **every push to `main` or `master`** will:

1. Read the current `project.version` from `pyproject.toml`
2. Create and push a git tag `vX.Y.Z` (if it doesn't already exist)
3. Build and publish to PyPI (Trusted Publishing)
4. Bump the version **patch** for the next release and push that commit back to the default branch

To avoid loops, the post-bump commit includes `[skip release]` and the workflow ignores commits containing that marker.
