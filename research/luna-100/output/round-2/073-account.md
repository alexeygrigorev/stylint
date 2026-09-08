# My Automated Python Release Process

I published my first Python library in early 2021. Since then, I've released 24 packages on PyPI and used them in my own projects. I used to publish everything manually, but after I started working with coding agents in 2025, I created libraries more often. Repeating the same release setup no longer made sense, so I automated it.

I start with a problem rather than a package. Sometimes a small utility becomes useful in another project, either as a command-line tool or as a library. Before creating a repository, I use ChatGPT to understand the problem, check similar tools, and decide whether packaging the result makes sense. This gives me a short description for the next step.

Choosing a name takes longer than it seems. It needs to fit the project and be short enough to use. It also needs to be available on PyPI. PyPI exposes package metadata at `https://pypi.org/pypi/{name}/json`. A 404 means the name is available, while a 200 means someone has already taken it.

I ask an agent for options, check them, and continue if a name is taken or doesn't feel right.

Heru came from the idea of one tool ruling the agents, with a short name connected to The Lord of the Rings. Quse means quota use, and I usually spend about ten minutes on naming. I want the final name to work for both the GitHub repository and the package.

Once the name is set, I create a public GitHub repository and publish a minimal first version. Public repositories let other people see and use the code. They also receive a larger GitHub Actions quota.

My usual Python structure uses Hatch with hatchling as the build backend and uv for tooling. It includes a package directory and a version file starting at 0.0.1.

It also includes tests and the main configuration files. Those are `pyproject.toml`, a Makefile, a README, and a lock file. A command-line package gets a project script entry point as well.

For a manual release, I configure separate API tokens for Test PyPI and PyPI in `.pypirc`. I build with Hatch and upload to Test PyPI. I check that installation works, then publish to the real index.

The release remains simple, but I don't want it to depend on credentials stored on whichever computer I happen to use.

The CI workflow starts with a version bump. I commit the change, create a tag beginning with `v`, and push that tag. GitHub Actions builds the package with uv and checks that the package version matches the tag.

It publishes through the official PyPI action. The `PYPI_API_TOKEN` is stored as a repository secret, so the computer creating the tag doesn't need the publishing token.

I turned the repeated setup into three skills. `init-library` creates the package skeleton, `setup-pypi-ci` adds tag-triggered publishing, and `release` bumps the version and watches the action.

I keep the skills in my agents repository so Codex, Claude Code, and OpenCode can use the same process. The trigger can also work for other registries when their CI workflow is configured around version tags.
