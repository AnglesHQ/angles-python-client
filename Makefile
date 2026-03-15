.PHONY: build check bump-patch bump-minor bump-major bump-test-patch bump-test-minor bump-test-major

build:
	python -m pip install -U build
	python -m build

check:
	python -m pip install -U twine
	python -m twine check dist/*

bump-patch:
	python -m pip install -U bump2version
	bump2version patch
	git push --follow-tags

bump-minor:
	python -m pip install -U bump2version
	bump2version minor
	git push --follow-tags

bump-major:
	python -m pip install -U bump2version
	bump2version major
	git push --follow-tags

# For TestPyPI: same version bump, but tag prefix is test-vX.Y.Z
bump-test-patch:
	python -m pip install -U bump2version
	bump2version --tag-name test-v{new_version} patch
	git push --follow-tags

bump-test-minor:
	python -m pip install -U bump2version
	bump2version --tag-name test-v{new_version} minor
	git push --follow-tags

bump-test-major:
	python -m pip install -U bump2version
	bump2version --tag-name test-v{new_version} major
	git push --follow-tags
