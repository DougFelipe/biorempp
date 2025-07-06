[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
<!-- These are examples of badges you might also want to add to your README. Update the URLs accordingly.
[![Built Status](https://api.cirrus-ci.com/github/<USER>/biorempp.svg?branch=main)](https://cirrus-ci.com/github/<USER>/biorempp)
[![ReadTheDocs](https://readthedocs.org/projects/biorempp/badge/?version=latest)](https://biorempp.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/biorempp/main.svg)](https://coveralls.io/r/<USER>/biorempp)
[![PyPI-Server](https://img.shields.io/pypi/v/biorempp.svg)](https://pypi.org/project/biorempp/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/biorempp.svg)](https://anaconda.org/conda-forge/biorempp)
[![Monthly Downloads](https://pepy.tech/badge/biorempp/month)](https://pepy.tech/project/biorempp)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/biorempp)
-->

# biorempp

> The Bioremediation Potential Profile (BioRemPP) is designed to explore the biotechnological potential of microbial, fungal, and plant genomes for bioremediation purposes

A longer description of your project goes here...

## Installation

In order to set up the necessary environment:

1. review and uncomment what you need in `environment.yml` and create an environment `biorempp` with the help of [conda]:
   ```
   conda env create -f environment.yml
   ```
2. activate the new environment with:
   ```
   conda activate biorempp
   ```

> **_NOTE:_**  The conda environment will have biorempp installed in editable mode.
> Some changes, e.g. in `setup.cfg`, might require you to run `pip install -e .` again.


Optional and needed only once after `git clone`:

3. install several [pre-commit] git hooks with:
   ```bash
   pre-commit install
   # You might also want to run `pre-commit autoupdate`
   ```
   and checkout the configuration under `.pre-commit-config.yaml`.
   The `-n, --no-verify` flag of `git commit` can be used to deactivate pre-commit hooks temporarily.

4. install [nbstripout] git hooks to remove the output cells of committed notebooks with:
   ```bash
   nbstripout --install --attributes notebooks/.gitattributes
   ```
   This is useful to avoid large diffs due to plots in your notebooks.
   A simple `nbstripout --uninstall` will revert these changes.


Then take a look into the `scripts` and `notebooks` folders.

## Dependency Management & Reproducibility

1. Always keep your abstract (unpinned) dependencies updated in `environment.yml` and eventually
   in `setup.cfg` if you want to ship and install your package via `pip` later on.
2. Create concrete dependencies as `environment.lock.yml` for the exact reproduction of your
   environment with:
   ```bash
   conda env export -n biorempp -f environment.lock.yml
   ```
   For multi-OS development, consider using `--no-builds` during the export.
3. Update your current environment with respect to a new `environment.lock.yml` using:
   ```bash
   conda env update -f environment.lock.yml --prune
   ```
## Project Organization

```
├── AUTHORS.md              <- List of developers and maintainers.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Guidelines for contributing to this project.
├── Dockerfile              <- Build a docker container with `docker build .`.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yml         <- The conda environment file for reproducibility.
├── models                  <- Trained and serialized models, model predictions,
│                              or model summaries.
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for
│                              ordering), the creator's initials and a description,
│                              e.g. `1.0-fw-initial-data-exploration`.
├── pyproject.toml          <- Build configuration. Don't change! Use `pip install -e .`
│                              to install for development or to build `tox -e build`.
├── references              <- Data dictionaries, manuals, and all other materials.
├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures             <- Generated plots and figures for reports.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── setup.py                <- [DEPRECATED] Use `python setup.py develop` to install for
│                              development or `python setup.py bdist_wheel` to build.
├── src
│   └── biorempp            <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `pytest`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
├── .isort.cfg              <- Configuration for git hook that sorts imports.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using [PyScaffold] 4.6 and the [dsproject extension] 0.7.2.

[conda]: https://docs.conda.io/
[pre-commit]: https://pre-commit.com/
[Jupyter]: https://jupyter.org/
[nbstripout]: https://github.com/kynan/nbstripout
[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[PyScaffold]: https://pyscaffold.org/
[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject

## Development & Contributing

### 📋 Commit Guidelines

This project follows [Conventional Commits](https://conventionalcommits.org/) specification for automated versioning and changelog generation.

#### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Commit Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Breaking Changes

For breaking changes, add `!` after the type or add `BREAKING CHANGE:` in the footer:

```bash
feat!: redesign API interface

BREAKING CHANGE: The API interface has been completely redesigned
```

#### Examples

```bash
# Feature addition (minor version bump)
feat: add KEGG pathway analysis functionality

# Bug fix (patch version bump)
fix: resolve memory leak in data processing pipeline

# Breaking change (major version bump)
feat!: migrate to new input validation system

# Documentation update (no version bump)
docs: update installation instructions
```

### 🚀 Release Process

This project uses automated semantic versioning powered by [semantic-release](https://semantic-release.gitbook.io/).

#### How Releases Work

1. **Automatic**: Releases are automatically triggered on every push to the `main` branch
2. **Version Calculation**: Based on conventional commit messages since the last release
3. **Changelog**: Automatically generated and updated
4. **GitHub Release**: Created with release notes and distribution files
5. **Tags**: Git tags are automatically created and pushed

#### Version Bumping Rules

| Commit Type | Example | Version Bump |
|-------------|---------|--------------|
| `fix:` | `fix: resolve input validation bug` | Patch (1.0.0 → 1.0.1) |
| `feat:` | `feat: add new analysis pipeline` | Minor (1.0.0 → 1.1.0) |
| `feat!:` or `BREAKING CHANGE:` | `feat!: redesign API` | Major (1.0.0 → 2.0.0) |
| `docs:`, `style:`, `test:` | `docs: update README` | No release |

#### Manual Release

If needed, you can trigger a release manually:

```bash
# Via GitHub Actions (recommended)
gh workflow run release.yml

# Or locally (requires setup)
npm run semantic-release
```

### 🛠 Development Workflow

1. **Fork and Clone**
   ```bash
   git clone https://github.com/DougFelipe/biorempp.git
   cd biorempp
   ```

2. **Setup Environment**
   ```bash
   conda env create -f environment.yml
   conda activate biorempp
   pip install -e .
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

4. **Make Changes and Test**
   ```bash
   # Run tests
   pytest tests/

   # Check code style
   flake8 src/ tests/ --max-line-length=88

   # Run all checks
   tox
   ```

5. **Commit with Conventional Format**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feat/your-feature-name
   # Create PR via GitHub UI
   ```

### 📦 Release Artifacts

Each release automatically generates:

- **Source Distribution** (`.tar.gz`)
- **Wheel Distribution** (`.whl`)
- **GitHub Release** with changelog
- **Updated CHANGELOG.md**
- **Git Tags** following semver

### 🔧 Setup for Maintainers

To enable automated releases, ensure the following secrets are configured in GitHub:

- `GH_TOKEN`: Personal Access Token with `repo` and `write:packages` permissions

For more details, see the [Contributing Guidelines](CONTRIBUTING.md).
