# The Release Checklist I Use for a Small Python Library

This synthetic style exercise uses a fictional project and invented details.

Last year I published my first Python package by accident. I ran `python setup.py sdist upload`, which was already obsolete, and the package appeared on PyPI without tests or a working description. Removing it wasn't possible, so I learned the release process the hard way.

Since then I've released 19 small packages in a fictional package registry. Most are tiny utilities, but they all follow the same checklist. It keeps releases predictable and makes failures easy to diagnose.

The registry, package names, and timings in this article are invented examples.

In this post, I'll share:

- how I prepare version, changelog, and metadata
- which checks run before the build
- how I build and review artifacts
- how the publish step works
- what I verify after release

## Prepare Release Metadata

I start by deciding the version number. A bug fix with no interface change gets a patch bump. A new function, a new argument, or a changed return type gets a minor bump. A breaking change gets a major bump and an upgrade note.

Then I update the changelog, and each entry has three parts:

1. the visible change
2. the reason for the change
3. the migration or compatibility note

The changelog is user-facing, so I avoid commit hashes at the top. "Add `normalize_labels` to accept uppercase labels" is more useful than "update API module".

I keep metadata in `pyproject.toml` and check name, version, description, and dependencies. I also check supported Python versions and read project URLs as a user would. A wrong repository link makes support harder for months.

## Run Checks Before Building

My local gate uses `make check`, and it runs four jobs in order:

1. `ruff` for lint errors
2. `pytest` for the test suite
3. package import checks
4. documentation example checks

The test suite must pass with the oldest supported Python and the newest supported Python. On a recent utility, that took 34 seconds locally and 1 minute 52 seconds in CI. The extra time is cheaper than answering bug reports from one unsupported runtime.

Import checks catch a specific failure. If a new dependency is imported at module top level, the package can fail on installation even when tests pass in the development environment. A small isolated import test makes that visible.

## Build and Review Artifacts

I build both a wheel and an sdist:

```bash
python -m build
```

The command creates artifacts in `dist/`.

Before uploading, I review them:

```bash
tar -tf dist/package_name-0.4.2.tar.gz | less
unzip -l dist/package_name-0.4.2-py3-none-any.whl
```

I look for tests accidentally included, large files, missing license text, and generated files that shouldn't ship. For one data utility, the wheel contained a 12 MB fixture. The release worked, but users paid for a useless download, so I moved the fixture into a separate development dependency.

I also install the wheel into a clean virtual environment:

```bash
python -m venv .venv-release
.venv-release/bin/python -m pip install dist/package_name-0.4.2-py3-none-any.whl
```

Then I run one command from the package README in that environment. This catches missing dependencies and path assumptions that the development environment hides.

## Publish the Release

The publish step uses a CI job, and it runs only after a tag passes the same checks:

```yaml
jobs:
  release:
    if: startsWith(github.ref, 'refs/tags/v')
```

CI holds a scoped token, so my laptop doesn't store registry credentials. I push the commit and tag, watch the workflow, and don't touch the version while the job runs. If the workflow fails, I delete the tag locally and remotely, fix the problem, and create a new tag.

For a small utility, the CI release usually finishes in 70 seconds. PyPI becomes visible before the documentation site updates. I note that delay in the release issue so I don't chase a missing page.

## Verify After Release

After the registry accepts the package, I run five checks:

1. install from the registry in a clean environment
2. run the README example
3. read the rendered project description
4. confirm the repository and issue links
5. close the release issue with the version and artifact link

I also check that the default branch has the version commit and that the tag points to it. A release isn't done because the upload succeeded. It's done when a new user can install the exact version and run the promised example.

The checklist takes about 25 minutes for a tiny utility. The first release still takes longer, mostly because metadata and CI permissions need review. After that, repetition makes the process boring, and boring is the goal.

I'll share the CI workflow file in a future article. If you want to follow along, don't forget to subscribe.
