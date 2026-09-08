# A Repeatable Release Process for Python Libraries

Publishing a library means making a package that someone can install and creating a release process that works when the next version is ready. Keeping these jobs separate lets you test a small first version before moving publishing from a laptop to CI.

## Start with a real problem

Begin with a specific problem you already have. A utility may later become useful in another project as a command-line tool or a small library. Before creating a repository, use a short validation step. Describe the problem, check similar tools, and decide whether packaging the result makes sense. This gives you a brief for the package and can show that the idea already exists elsewhere.

Choose a name after the brief is clear. It should fit the project, be short enough to use, and be available on PyPI. PyPI exposes package metadata at `https://pypi.org/pypi/{name}/json`. A 404 means the name is available. A 200 means someone has already registered it.

Ask an agent for options, check them, and continue if the available name doesn't feel right.

## Publish a minimal first version

Create a public GitHub repository and publish a skeleton before building every feature. Public repositories let people see the code and can receive a larger GitHub Actions quota than private repositories.

The layout can stay small. Use a package directory with `__init__.py` and a version file, then add the test directory and configuration files. I use Hatch with hatchling as the build backend and uv for tooling. A command-line package also needs a project script entry point so installation exposes the command.

Before publishing to the real index, use Test PyPI. Configure separate API tokens for Test PyPI and PyPI in `.pypirc`.

Build with Hatch and upload to the test repository. Install the package and check that it behaves as expected. Only then publish to PyPI. The manual sequence is short enough to document in the README.

## Move the release to CI

CI makes the release independent of the computer that creates it. Bump the version, commit the change, create a tag beginning with `v`, and push the tag. GitHub Actions can build the package with uv, check that the version inside the artifact matches the tag, and publish through the official `pypa/gh-action-pypi-publish` action.

Keep the version rule visible because a bug fix usually gets a patch increment. A larger compatible change or a breaking change gets a minor increment in this workflow. I rarely change the major version, so the exact policy is less important than applying it consistently.

Store `PYPI_API_TOKEN` as a GitHub repository secret. The machine that creates the tag doesn't need the publishing token, and the same trigger can serve other ecosystems. A Rust project can use it to cross-compile binaries and attach them to a GitHub Release. The workflow can also publish artifacts to another registry. CI still performs the build with its stored credentials.

## Remove repeated setup with skills

Once the manual and CI flows work, reusable skills can scaffold the same process. `init-library` creates the package layout, `setup-pypi-ci` adds tag-triggered publishing, and `release` bumps the version and watches the workflow. Keeping these skills in one agents repository gives Codex, Claude Code, and OpenCode the same instructions.

The benefit comes from explicit steps. The package skeleton and test upload have clear places in the process. So do the tag check, repository secret, and release trigger. When those steps are repeatable, creating another small library doesn't require remembering the setup by hand.
