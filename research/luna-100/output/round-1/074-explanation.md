# A Small, Repeatable PyPI Release Workflow

Publishing a Python package has two separate jobs: making a package that can be installed and creating a release process that can be repeated. Keeping those jobs separate makes it easier to test the first version and later move publishing from a laptop to CI.

Start with a clear reason for the library. A small project often begins as a utility for a problem you already have. Before packaging it, check existing libraries and write down what yours should do. Then choose a package name that is usable both on GitHub and PyPI. PyPI exposes package metadata at `/pypi/{name}/json`; a 404 indicates that a name is available, while a 200 means it is already registered.

Create a minimal repository first. A typical layout has the package directory, `__init__.py`, a version file, tests, `pyproject.toml`, a README, and tooling files. Hatch and hatchling can build the package, while uv manages the environment. If the package provides a command, add a project script so installation exposes the CLI.

Before publishing publicly, use Test PyPI. Configure separate API tokens for Test PyPI and PyPI, then build the package and upload it to the test index. Install it and inspect the result. Only after that check should the package go to the production index. The manual commands are straightforward: build, publish to the test repository, then publish normally.

The repeatable version uses a tag. Store the PyPI token as a GitHub secret and create a workflow that runs when a tag beginning with `v` is pushed. The workflow should build the package, verify that the version inside the artifact matches the tag, and publish with the official PyPI action. A release then has a short sequence: update the version, commit, create the tag, and push it.

Version changes need a rule. A bug fix usually receives a patch increment. A larger compatible change or a breaking change receives a minor increment in this workflow. Major versions are uncommon in the author’s practice. The exact policy can differ, but it should be visible and consistent.

The trigger is useful beyond Python. A Rust project can use the same tag event to cross-compile binaries, attach them to a GitHub release, and publish wheels. The commands differ by ecosystem, but CI still performs the build and uses stored credentials. This keeps release behavior independent of the developer’s local configuration.

Once the process is understood, an agent skill can remove repetition. One skill scaffolds the package, another installs tag-triggered publishing, and a release skill bumps versions and observes the workflow. A shared skills repository gives different coding agents the same instructions. Automation is useful here because every step is explicit and the result is easy to inspect.
