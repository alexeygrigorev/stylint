# How I Automated My Python Releases

I published my first Python library in early 2021. Since then I have released 24 packages on PyPI and used them in my own projects. I used to publish manually, but after I started working with coding agents in 2025, I created libraries more often. Repeating the release setup stopped making sense, so I automated it.

I still begin with a problem rather than a package. When a small utility might be useful in another project, I first discuss the idea with ChatGPT and check whether an existing library already solves it. That research gives me a short description of what the package should do. Only after that do I create a repository and choose a name.

Naming takes longer than it appears. The name needs to be short, fit the project, and be available on PyPI. I ask an agent for options and check each one through PyPI’s metadata endpoint. A 404 means the name is available; a 200 means it is taken. Heru came from the idea of one tool ruling the agents, while Quse is short for quota use. I usually spend about ten minutes before settling on a name that works for both the repository and the package.

The first repository is deliberately small. I make it public because I want people to see and use the code, and public repositories receive a larger GitHub Actions quota. My usual layout uses Hatch with hatchling as the build backend and uv for tooling. It contains the package directory, a version file starting at 0.0.1, tests, pyproject.toml, a Makefile, README, and lock file. A command-line package also gets a project script entry point.

For a manual release I configure Test PyPI and PyPI with separate API tokens in .pypirc. I build with Hatch, upload to Test PyPI, check that installation works, and then upload to the real index. This flow is simple enough to document in a README, but I prefer not to depend on credentials on whichever computer I happen to use.

My release workflow therefore runs in GitHub Actions. I bump the version, commit it, create a tag beginning with v, and push that tag. The workflow builds the package with uv, checks that the package version matches the tag, and publishes through the official PyPI action. The token is stored as the PYPI_API_TOKEN repository secret. The machine that creates the tag does not need the publishing token.

I turned the repeated setup into three skills: init-library creates the skeleton, setup-pypi-ci adds the workflow, and release bumps the version and watches the action. The same pattern works for crates.io, npm, or binary artifacts when CI is configured for the registry. I keep the skills in my agents repository so Codex, Claude Code, and OpenCode can use the same process.
