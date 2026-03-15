# Contributing

Thanks for contributing!

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
```

## Build locally

```bash
python -m pip install -U build twine
python -m build
python -m twine check dist/*
```

## Release (GitHub Actions + Trusted Publishing)

This repo is set up to publish to **PyPI** when you push a git tag matching `v*` (e.g. `v1.0.1`).

1. Bump `project.version` in `pyproject.toml`
2. Commit and push to `main`
3. Tag and push:

   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

The `Publish to PyPI` workflow will build and publish.

### TestPyPI (optional)

Push a tag `test-v1.0.1` (or trigger the workflow manually) to publish to TestPyPI first.


## Version bumping

You can bump versions in two ways:

### Local

```bash
pip install -U bump2version
bump2version patch   # or minor / major
git push --follow-tags
```

### GitHub Actions (recommended)

Use the **Bump version and tag** workflow with:
- `target=pypi` for a `vX.Y.Z` tag (publishes to PyPI)
- `target=testpypi` for a `test-vX.Y.Z` tag (publishes to TestPyPI)


### Auto-release on main/master (fork-friendly)

If you want *every* push to `main`/`master` to publish and then bump the version, use:

- `.github/workflows/release-on-main.yml`

This workflow:
- tags `vX.Y.Z` if the tag doesn't exist,
- publishes to PyPI,
- then bumps patch and pushes a commit with `[skip release]`.

You can disable this behavior by removing that workflow file or adding `[skip release]` to a commit message.
