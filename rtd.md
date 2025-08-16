Read the Docs build information
Build id: 29223477
Project: biorempp
Version: latest
Commit: 248ffc9a810571c76cbdd9da643d3257aa5a3177
Date: 2025-08-16T17:43:29.988850Z
State: finished
Success: True


[rtd-command-info] start-time: 2025-08-16T17:43:30.440364Z, end-time: 2025-08-16T17:43:31.279899Z, duration: 0, exit-code: 0
git clone --depth 1 https://github.com/DougFelipe/biorempp.git .
Cloning into '.'...

[rtd-command-info] start-time: 2025-08-16T17:43:31.336378Z, end-time: 2025-08-16T17:43:31.821861Z, duration: 0, exit-code: 0
git fetch origin --force --prune --prune-tags --depth 50 refs/heads/main:refs/remotes/origin/main
From https://github.com/DougFelipe/biorempp
 * [new tag]         v0.2.0     -> v0.2.0
 * [new tag]         v0.3.0     -> v0.3.0
 * [new tag]         v0.3.1     -> v0.3.1
 * [new tag]         v0.4.0     -> v0.4.0
 * [new tag]         v0.5.0     -> v0.5.0
 * [new tag]         v0.6.0     -> v0.6.0
 * [new tag]         v0.6.1     -> v0.6.1

[rtd-command-info] start-time: 2025-08-16T17:43:31.903002Z, end-time: 2025-08-16T17:43:31.955176Z, duration: 0, exit-code: 0
git checkout --force origin/main
Note: switching to 'origin/main'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 248ffc9 Merge pull request #41 from DougFelipe/development

[rtd-command-info] start-time: 2025-08-16T17:43:32.002618Z, end-time: 2025-08-16T17:43:32.037405Z, duration: 0, exit-code: 0
cat .readthedocs.yml
# =============================================================================
# Read the Docs (RTD) - Configuration v2
# Official docs: https://docs.readthedocs.io/en/stable/config-file/v2.html
# Place this file at the ROOT of your repository as `.readthedocs.yml`
# =============================================================================

# Required: configuration schema version
version: 2

# -----------------------------------------------------------------------------
# Sphinx (documentation generator)
# -----------------------------------------------------------------------------
sphinx:
  # Path to the Sphinx configuration file (conf.py)
  configuration: docs/conf.py

  # Optional: Treat warnings as errors (fails the build if there are warnings)
  # Recommended when docs are stable, to keep quality high.
  fail_on_warning: false

# -----------------------------------------------------------------------------
# Extra output formats in addition to the default HTML
# -----------------------------------------------------------------------------
formats:
  - pdf          # Generates a PDF (via LaTeX) of your documentation
  # - epub       # Uncomment to generate an EPUB file

# -----------------------------------------------------------------------------
# Build environment configuration
# -----------------------------------------------------------------------------
build:
  os: ubuntu-22.04       # OS used for building
  tools:
    python: "3.11"       # Python version for the build

# -----------------------------------------------------------------------------
# How to install dependencies for building the docs
# -----------------------------------------------------------------------------
python:
  install:
    # 1) Install the package itself first (also installs runtime dependencies)
    #    This allows autodoc and imports from the package in the docs.
    - { path: ., method: pip }

    # 2) Documentation-specific dependencies
    #    This should contain what Sphinx and its extensions require
    - requirements: docs/requirements.txt

    # TIP:
    # - If your docs import heavy dependencies (e.g., numpy, pandas) and
    #   builds are slow, you can mock them in `docs/conf.py`:
    #       autodoc_mock_imports = ["numpy", "pandas"]
    # - If you need extras for docs (e.g., biorempp[docs]), replace with:
    #   - { path: ".[docs]", method: pip }

[rtd-command-info] start-time: 2025-08-16T17:43:36.276681Z, end-time: 2025-08-16T17:43:36.328616Z, duration: 0, exit-code: 0
asdf global python 3.11.12


[rtd-command-info] start-time: 2025-08-16T17:43:36.693150Z, end-time: 2025-08-16T17:43:37.394059Z, duration: 0, exit-code: 0
python -mvirtualenv $READTHEDOCS_VIRTUALENV_PATH
created virtual environment CPython3.11.12.final.0-64 in 457ms
  creator CPython3Posix(dest=/home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/docs/.local/share/virtualenv)
    added seed packages: pip==23.1, setuptools==67.6.1, wheel==0.40.0
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

[rtd-command-info] start-time: 2025-08-16T17:43:37.457665Z, end-time: 2025-08-16T17:43:42.191047Z, duration: 4, exit-code: 0
python -m pip install --upgrade --no-cache-dir pip setuptools
Requirement already satisfied: pip in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (23.1)
Collecting pip
  Downloading pip-25.2-py3-none-any.whl (1.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 14.5 MB/s eta 0:00:00
Requirement already satisfied: setuptools in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (67.6.1)
Collecting setuptools
  Downloading setuptools-80.9.0-py3-none-any.whl (1.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 25.3 MB/s eta 0:00:00
Installing collected packages: setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 67.6.1
    Uninstalling setuptools-67.6.1:
      Successfully uninstalled setuptools-67.6.1
  Attempting uninstall: pip
    Found existing installation: pip 23.1
    Uninstalling pip-23.1:
      Successfully uninstalled pip-23.1
Successfully installed pip-25.2 setuptools-80.9.0

[rtd-command-info] start-time: 2025-08-16T17:43:42.237376Z, end-time: 2025-08-16T17:43:45.993755Z, duration: 3, exit-code: 0
python -m pip install --upgrade --no-cache-dir sphinx
Collecting sphinx
  Downloading sphinx-8.2.3-py3-none-any.whl.metadata (7.0 kB)
Collecting sphinxcontrib-applehelp>=1.0.7 (from sphinx)
  Downloading sphinxcontrib_applehelp-2.0.0-py3-none-any.whl.metadata (2.3 kB)
Collecting sphinxcontrib-devhelp>=1.0.6 (from sphinx)
  Downloading sphinxcontrib_devhelp-2.0.0-py3-none-any.whl.metadata (2.3 kB)
Collecting sphinxcontrib-htmlhelp>=2.0.6 (from sphinx)
  Downloading sphinxcontrib_htmlhelp-2.1.0-py3-none-any.whl.metadata (2.3 kB)
Collecting sphinxcontrib-jsmath>=1.0.1 (from sphinx)
  Downloading sphinxcontrib_jsmath-1.0.1-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting sphinxcontrib-qthelp>=1.0.6 (from sphinx)
  Downloading sphinxcontrib_qthelp-2.0.0-py3-none-any.whl.metadata (2.3 kB)
Collecting sphinxcontrib-serializinghtml>=1.1.9 (from sphinx)
  Downloading sphinxcontrib_serializinghtml-2.0.0-py3-none-any.whl.metadata (2.4 kB)
Collecting Jinja2>=3.1 (from sphinx)
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting Pygments>=2.17 (from sphinx)
  Downloading pygments-2.19.2-py3-none-any.whl.metadata (2.5 kB)
Collecting docutils<0.22,>=0.20 (from sphinx)
  Downloading docutils-0.21.2-py3-none-any.whl.metadata (2.8 kB)
Collecting snowballstemmer>=2.2 (from sphinx)
  Downloading snowballstemmer-3.0.1-py3-none-any.whl.metadata (7.9 kB)
Collecting babel>=2.13 (from sphinx)
  Downloading babel-2.17.0-py3-none-any.whl.metadata (2.0 kB)
Collecting alabaster>=0.7.14 (from sphinx)
  Downloading alabaster-1.0.0-py3-none-any.whl.metadata (2.8 kB)
Collecting imagesize>=1.3 (from sphinx)
  Downloading imagesize-1.4.1-py2.py3-none-any.whl.metadata (1.5 kB)
Collecting requests>=2.30.0 (from sphinx)
  Downloading requests-2.32.4-py3-none-any.whl.metadata (4.9 kB)
Collecting roman-numerals-py>=1.0.0 (from sphinx)
  Downloading roman_numerals_py-3.1.0-py3-none-any.whl.metadata (3.6 kB)
Collecting packaging>=23.0 (from sphinx)
  Downloading packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting MarkupSafe>=2.0 (from Jinja2>=3.1->sphinx)
  Downloading MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.0 kB)
Collecting charset_normalizer<4,>=2 (from requests>=2.30.0->sphinx)
  Downloading charset_normalizer-3.4.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (36 kB)
Collecting idna<4,>=2.5 (from requests>=2.30.0->sphinx)
  Downloading idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting urllib3<3,>=1.21.1 (from requests>=2.30.0->sphinx)
  Downloading urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests>=2.30.0->sphinx)
  Downloading certifi-2025.8.3-py3-none-any.whl.metadata (2.4 kB)
Downloading sphinx-8.2.3-py3-none-any.whl (3.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 108.9 MB/s  0:00:00
Downloading docutils-0.21.2-py3-none-any.whl (587 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 587.4/587.4 kB 676.8 MB/s  0:00:00
Downloading alabaster-1.0.0-py3-none-any.whl (13 kB)
Downloading babel-2.17.0-py3-none-any.whl (10.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.2/10.2 MB 145.5 MB/s  0:00:00
Downloading imagesize-1.4.1-py2.py3-none-any.whl (8.8 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23 kB)
Downloading packaging-25.0-py3-none-any.whl (66 kB)
Downloading pygments-2.19.2-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 308.5 MB/s  0:00:00
Downloading requests-2.32.4-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (150 kB)
Downloading idna-3.10-py3-none-any.whl (70 kB)
Downloading urllib3-2.5.0-py3-none-any.whl (129 kB)
Downloading certifi-2025.8.3-py3-none-any.whl (161 kB)
Downloading roman_numerals_py-3.1.0-py3-none-any.whl (7.7 kB)
Downloading snowballstemmer-3.0.1-py3-none-any.whl (103 kB)
Downloading sphinxcontrib_applehelp-2.0.0-py3-none-any.whl (119 kB)
Downloading sphinxcontrib_devhelp-2.0.0-py3-none-any.whl (82 kB)
Downloading sphinxcontrib_htmlhelp-2.1.0-py3-none-any.whl (98 kB)
Downloading sphinxcontrib_jsmath-1.0.1-py2.py3-none-any.whl (5.1 kB)
Downloading sphinxcontrib_qthelp-2.0.0-py3-none-any.whl (88 kB)
Downloading sphinxcontrib_serializinghtml-2.0.0-py3-none-any.whl (92 kB)
Installing collected packages: urllib3, sphinxcontrib-serializinghtml, sphinxcontrib-qthelp, sphinxcontrib-jsmath, sphinxcontrib-htmlhelp, sphinxcontrib-devhelp, sphinxcontrib-applehelp, snowballstemmer, roman-numerals-py, Pygments, packaging, MarkupSafe, imagesize, idna, docutils, charset_normalizer, certifi, babel, alabaster, requests, Jinja2, sphinx

Successfully installed Jinja2-3.1.6 MarkupSafe-3.0.2 Pygments-2.19.2 alabaster-1.0.0 babel-2.17.0 certifi-2025.8.3 charset_normalizer-3.4.3 docutils-0.21.2 idna-3.10 imagesize-1.4.1 packaging-25.0 requests-2.32.4 roman-numerals-py-3.1.0 snowballstemmer-3.0.1 sphinx-8.2.3 sphinxcontrib-applehelp-2.0.0 sphinxcontrib-devhelp-2.0.0 sphinxcontrib-htmlhelp-2.1.0 sphinxcontrib-jsmath-1.0.1 sphinxcontrib-qthelp-2.0.0 sphinxcontrib-serializinghtml-2.0.0 urllib3-2.5.0

[rtd-command-info] start-time: 2025-08-16T17:43:46.053060Z, end-time: 2025-08-16T17:43:54.649090Z, duration: 8, exit-code: 0
python -m pip install --upgrade --upgrade-strategy only-if-needed --no-cache-dir .
Processing /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting pandas>=2.0.0 (from biorempp==0.6.1.post1.dev2)
  Downloading pandas-2.3.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (91 kB)
Collecting numpy>=1.21.0 (from biorempp==0.6.1.post1.dev2)
  Downloading numpy-2.3.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (62 kB)
Collecting tqdm (from biorempp==0.6.1.post1.dev2)
  Downloading tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
Collecting click (from biorempp==0.6.1.post1.dev2)
  Downloading click-8.2.1-py3-none-any.whl.metadata (2.5 kB)
Collecting python-dateutil>=2.8.2 (from pandas>=2.0.0->biorempp==0.6.1.post1.dev2)
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas>=2.0.0->biorempp==0.6.1.post1.dev2)
  Downloading pytz-2025.2-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas>=2.0.0->biorempp==0.6.1.post1.dev2)
  Downloading tzdata-2025.2-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas>=2.0.0->biorempp==0.6.1.post1.dev2)
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Downloading numpy-2.3.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.9/16.9 MB 266.0 MB/s  0:00:00
Downloading pandas-2.3.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.4/12.4 MB 355.2 MB/s  0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
Downloading click-8.2.1-py3-none-any.whl (102 kB)
Downloading tqdm-4.67.1-py3-none-any.whl (78 kB)
Building wheels for collected packages: biorempp
  Building wheel for biorempp (pyproject.toml): started
  Building wheel for biorempp (pyproject.toml): finished with status 'done'
  Created wheel for biorempp: filename=biorempp-0.6.1.post1.dev2-py3-none-any.whl size=256028 sha256=49e21403b0cd863c2404b55a5e982c149e09fa88729ad0eec636d0fa1db5bd42
  Stored in directory: /tmp/pip-ephem-wheel-cache-vwy265s6/wheels/55/77/a6/5ba4e0c9cd71b132d11d80d49d298014f559fcfd7075c7fc1e
Successfully built biorempp
Installing collected packages: pytz, tzdata, tqdm, six, numpy, click, python-dateutil, pandas, biorempp

Successfully installed biorempp-0.6.1.post1.dev2 click-8.2.1 numpy-2.3.2 pandas-2.3.1 python-dateutil-2.9.0.post0 pytz-2025.2 six-1.17.0 tqdm-4.67.1 tzdata-2025.2

[rtd-command-info] start-time: 2025-08-16T17:43:54.690047Z, end-time: 2025-08-16T17:43:57.225320Z, duration: 2, exit-code: 0
python -m pip install --exists-action=w --no-cache-dir -r docs/requirements.txt
Requirement already satisfied: click in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from -r docs/requirements.txt (line 1)) (8.2.1)
Collecting myst-parser<3,>=2.0 (from myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading myst_parser-2.0.0-py3-none-any.whl.metadata (5.4 kB)
Requirement already satisfied: numpy>=1.21.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from -r docs/requirements.txt (line 3)) (2.3.2)
Requirement already satisfied: pandas>=2.0.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from -r docs/requirements.txt (line 4)) (2.3.1)
Requirement already satisfied: sphinx<9,>=7.3 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from -r docs/requirements.txt (line 5)) (8.2.3)
Collecting sphinx-autoapi>=3.0.0 (from -r docs/requirements.txt (line 6))
  Downloading sphinx_autoapi-3.6.0-py3-none-any.whl.metadata (4.6 kB)
Collecting sphinx-rtd-theme<4,>=3.0.1 (from -r docs/requirements.txt (line 7))
  Downloading sphinx_rtd_theme-3.0.2-py2.py3-none-any.whl.metadata (4.4 kB)
Requirement already satisfied: tqdm in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from -r docs/requirements.txt (line 8)) (4.67.1)
Collecting docutils<0.21,>=0.16 (from myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading docutils-0.20.1-py3-none-any.whl.metadata (2.8 kB)
Requirement already satisfied: jinja2 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2)) (3.1.6)
Collecting markdown-it-py~=3.0 (from myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading markdown_it_py-3.0.0-py3-none-any.whl.metadata (6.9 kB)
Collecting mdit-py-plugins~=0.4 (from myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading mdit_py_plugins-0.5.0-py3-none-any.whl.metadata (2.8 kB)
Collecting pyyaml (from myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting sphinx<9,>=7.3 (from -r docs/requirements.txt (line 5))
  Downloading sphinx-7.4.7-py3-none-any.whl.metadata (6.1 kB)
Requirement already satisfied: sphinxcontrib-applehelp in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.0.0)
Requirement already satisfied: sphinxcontrib-devhelp in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.0.0)
Requirement already satisfied: sphinxcontrib-jsmath in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (1.0.1)
Requirement already satisfied: sphinxcontrib-htmlhelp>=2.0.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.1.0)
Requirement already satisfied: sphinxcontrib-serializinghtml>=1.1.9 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.0.0)
Requirement already satisfied: sphinxcontrib-qthelp in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.0.0)
Requirement already satisfied: Pygments>=2.17 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.19.2)
Requirement already satisfied: snowballstemmer>=2.2 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (3.0.1)
Requirement already satisfied: babel>=2.13 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.17.0)
Collecting alabaster~=0.7.14 (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5))
  Downloading alabaster-0.7.16-py3-none-any.whl.metadata (2.9 kB)
Requirement already satisfied: imagesize>=1.3 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (1.4.1)
Requirement already satisfied: requests>=2.30.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.32.4)
Requirement already satisfied: packaging>=23.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (25.0)
Collecting sphinxcontrib-jquery<5,>=4 (from sphinx-rtd-theme<4,>=3.0.1->-r docs/requirements.txt (line 7))
  Downloading sphinxcontrib_jquery-4.1-py2.py3-none-any.whl.metadata (2.6 kB)
Collecting mdurl~=0.1 (from markdown-it-py~=3.0->myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Collecting linkify-it-py~=2.0 (from myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading linkify_it_py-2.0.3-py3-none-any.whl.metadata (8.5 kB)
Collecting uc-micro-py (from linkify-it-py~=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2))
  Downloading uc_micro_py-1.0.3-py3-none-any.whl.metadata (2.0 kB)
Requirement already satisfied: python-dateutil>=2.8.2 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from pandas>=2.0.0->-r docs/requirements.txt (line 4)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from pandas>=2.0.0->-r docs/requirements.txt (line 4)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from pandas>=2.0.0->-r docs/requirements.txt (line 4)) (2025.2)
Collecting astroid>=2.7 (from sphinx-autoapi>=3.0.0->-r docs/requirements.txt (line 6))
  Downloading astroid-3.3.11-py3-none-any.whl.metadata (4.4 kB)
Requirement already satisfied: MarkupSafe>=2.0 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from jinja2->myst-parser<3,>=2.0->myst-parser[linkify]<3,>=2.0->-r docs/requirements.txt (line 2)) (3.0.2)
Requirement already satisfied: six>=1.5 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas>=2.0.0->-r docs/requirements.txt (line 4)) (1.17.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from requests>=2.30.0->sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (3.4.3)
Requirement already satisfied: idna<4,>=2.5 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from requests>=2.30.0->sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (3.10)
Requirement already satisfied: urllib3<3,>=1.21.1 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from requests>=2.30.0->sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /home/docs/checkouts/readthedocs.org/user_builds/biorempp/envs/latest/lib/python3.11/site-packages (from requests>=2.30.0->sphinx<9,>=7.3->-r docs/requirements.txt (line 5)) (2025.8.3)
Downloading myst_parser-2.0.0-py3-none-any.whl (77 kB)
Downloading sphinx-7.4.7-py3-none-any.whl (3.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.4/3.4 MB 112.6 MB/s  0:00:00
Downloading sphinx_rtd_theme-3.0.2-py2.py3-none-any.whl (7.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.7/7.7 MB 243.3 MB/s  0:00:00
Downloading alabaster-0.7.16-py3-none-any.whl (13 kB)
Downloading docutils-0.20.1-py3-none-any.whl (572 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 572.7/572.7 kB 667.6 MB/s  0:00:00
Downloading markdown_it_py-3.0.0-py3-none-any.whl (87 kB)
Downloading mdit_py_plugins-0.5.0-py3-none-any.whl (57 kB)
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Downloading linkify_it_py-2.0.3-py3-none-any.whl (19 kB)
Downloading sphinxcontrib_jquery-4.1-py2.py3-none-any.whl (121 kB)
Downloading sphinx_autoapi-3.6.0-py3-none-any.whl (35 kB)
Downloading astroid-3.3.11-py3-none-any.whl (275 kB)
Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 763.0/763.0 kB 682.7 MB/s  0:00:00
Downloading uc_micro_py-1.0.3-py3-none-any.whl (6.2 kB)
Installing collected packages: uc-micro-py, pyyaml, mdurl, docutils, astroid, alabaster, sphinx, markdown-it-py, linkify-it-py, sphinxcontrib-jquery, sphinx-autoapi, mdit-py-plugins, sphinx-rtd-theme, myst-parser
  Attempting uninstall: docutils
    Found existing installation: docutils 0.21.2
    Uninstalling docutils-0.21.2:
      Successfully uninstalled docutils-0.21.2
  Attempting uninstall: alabaster
    Found existing installation: alabaster 1.0.0
    Uninstalling alabaster-1.0.0:
      Successfully uninstalled alabaster-1.0.0
  Attempting uninstall: sphinx
    Found existing installation: Sphinx 8.2.3
    Uninstalling Sphinx-8.2.3:
      Successfully uninstalled Sphinx-8.2.3

Successfully installed alabaster-0.7.16 astroid-3.3.11 docutils-0.20.1 linkify-it-py-2.0.3 markdown-it-py-3.0.0 mdit-py-plugins-0.5.0 mdurl-0.1.2 myst-parser-2.0.0 pyyaml-6.0.2 sphinx-7.4.7 sphinx-autoapi-3.6.0 sphinx-rtd-theme-3.0.2 sphinxcontrib-jquery-4.1 uc-micro-py-1.0.3

[rtd-command-info] start-time: 2025-08-16T17:43:57.301456Z, end-time: 2025-08-16T17:43:57.337621Z, duration: 0, exit-code: 0
cat docs/conf.py
# Configuration file for the Sphinx documentation builder.
# BioRemPP documentation configuration

import os
import sys
from pathlib import Path

# Add the project source to the path
docs_dir = Path(__file__).parent
project_dir = docs_dir.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

# Debug: Print path information for RTD debugging
if os.environ.get('READTHEDOCS', None) == 'True':
    print(f"RTD Build - Project dir: {project_dir}", file=sys.stderr)
    print(f"RTD Build - Source dir: {src_dir}", file=sys.stderr)
    print(f"RTD Build - Python path includes: {str(src_dir) in sys.path}", file=sys.stderr)

# -- Project information -----------------------------------------------------
project = 'BioRemPP'
copyright = '2025, Douglas Felipe'
author = 'Douglas Felipe'

# Try to get version from package
try:
    from importlib.metadata import version
    release = version("biorempp")
except Exception:
    release = "0.1.0-dev"

version = release.split('+')[0]  # Short version

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "linkify",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Source parsers
source_suffix = ['.rst', '.md']

# Master document
master_doc = 'index'
root_doc = 'index'

# Exclude patterns
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '.venv',
    'temp_md',
    'outputs'
]

# Templates
templates_path = ['_templates']

# Internationalization
language = 'en'

# Mock imports for documentation
autodoc_mock_imports = [
    'numpy', 'pandas', 'scipy', 'matplotlib', 'sklearn',
    'tqdm', 'click', 'dash', 'plotly'
]

# Autodoc configuration for better docstring extraction
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Suppress specific warnings
suppress_warnings = [
    'myst.header',
    'myst.xref_missing',
    'myst.iref_ambiguous',
    'autodoc.import_object',
]

# Nitpicky mode configuration
nitpicky = False
nitpick_ignore = [
    ('py:class', 'optional'),
    ('py:class', 'callable'),
    ('py:class', 'pd.DataFrame'),
    ('py:class', 'default=None'),
    ('py:class', 'default "INFO"'),
    ('py:class', 'default True'),
    ('py:class', 'default "detailed"'),
]

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Extension configuration -------------------------------------------------
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'
autosummary_generate = True
autosummary_generate_overwrite = True
autodoc_preserve_defaults = True

# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'pandas': ('https://pandas.pydata.org/docs', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
}

# Print configuration loaded
print(f"Sphinx configuration loaded for {project} {version}", file=sys.stderr)

[rtd-command-info] start-time: 2025-08-16T17:43:57.390853Z, end-time: 2025-08-16T17:44:00.209933Z, duration: 2, exit-code: 0
python -m sphinx -T -b html -d _build/doctrees -D language=en . $READTHEDOCS_OUTPUT/html
Running Sphinx v7.4.7
RTD Build - Project dir: /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest
RTD Build - Source dir: /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/src
RTD Build - Python path includes: True
Sphinx configuration loaded for BioRemPP 0.6.1.post1.dev2
loading translations [en]... done
making output directory... done
Converting `source_suffix = ['.rst', '.md']` to `source_suffix = {'.rst': 'restructuredtext', '.md': 'restructuredtext'}`.
myst v2.0.0: MdParserConfig(commonmark_only=False, gfm_only=False, enable_extensions={'colon_fence', 'html_image', 'dollarmath', 'smartquotes', 'linkify', 'substitution', 'deflist', 'tasklist'}, disable_syntax=[], all_links_external=False, url_schemes=('http', 'https', 'mailto', 'ftp'), ref_domains=None, fence_as_directive=set(), number_code_blocks=[], title_to_header=False, heading_anchors=0, heading_slug_func=None, html_meta={}, footnote_transition=True, words_per_minute=200, substitutions={}, linkify_fuzzy_links=True, dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', enable_checkboxes=False, suppress_warnings=[], highlight_code_blocks=True)
[autosummary] generating autosummary for: API_Reference.md, DOCUMENTATION_BUILD_REPORT.md, DOCUMENTATION_GUIDE.md, Test_Suite_Documentation.md, authors.md, changelog.md, contributing.md, index.md, license.md, overview.md, readme.md
loading intersphinx inventory 'python' from https://docs.python.org/3/objects.inv...
loading intersphinx inventory 'numpy' from https://numpy.org/doc/stable/objects.inv...
loading intersphinx inventory 'pandas' from https://pandas.pydata.org/docs/objects.inv...
loading intersphinx inventory 'matplotlib' from https://matplotlib.org/stable/objects.inv...
building [mo]: targets for 0 po files that are out of date
writing output...
building [html]: targets for 11 source files that are out of date
updating environment: [new config] 11 added, 0 changed, 0 removed
reading sources... [  9%] API_Reference
reading sources... [ 18%] DOCUMENTATION_BUILD_REPORT
reading sources... [ 27%] DOCUMENTATION_GUIDE
reading sources... [ 36%] Test_Suite_Documentation
reading sources... [ 45%] authors
reading sources... [ 55%] changelog
reading sources... [ 64%] contributing
reading sources... [ 73%] index
reading sources... [ 82%] license
reading sources... [ 91%] overview
reading sources... [100%] readme

/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/DOCUMENTATION_BUILD_REPORT.md:8: ERROR: Document or section may not begin with a transition.
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/index.md:29: WARNING: toctree contains reference to nonexisting document 'api/modules'
looking for now-outdated files... none found
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/index.md:37: WARNING: toctree contains reference to nonexisting document 'CONTRIBUTING'
pickling environment... done
checking consistency... /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/DOCUMENTATION_BUILD_REPORT.md: WARNING: document isn't included in any toctree
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/DOCUMENTATION_GUIDE.md: WARNING: document isn't included in any toctree
done
preparing documents... /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/contributing.md: WARNING: document isn't included in any toctree
done
copying assets...
copying static files... done
copying extra files... done
copying assets: done
writing output... [  9%] API_Reference
writing output... [ 18%] DOCUMENTATION_BUILD_REPORT
writing output... [ 27%] DOCUMENTATION_GUIDE
writing output... [ 36%] Test_Suite_Documentation
writing output... [ 45%] authors
writing output... [ 55%] changelog
writing output... [ 64%] contributing
writing output... [ 73%] index
writing output... [ 82%] license
writing output... [ 91%] overview
writing output... [100%] readme

/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:848: WARNING: Pygments lexer name 'nextflow' is not known
generating indices... genindex done
highlighting module code...
writing additional pages... search done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded, 7 warnings.

The HTML pages are in ../_readthedocs/html.

[rtd-command-info] start-time: 2025-08-16T17:44:00.248808Z, end-time: 2025-08-16T17:44:01.753661Z, duration: 1, exit-code: 0
python -m sphinx -T -b latex -d _build/doctrees -D language=en . $READTHEDOCS_OUTPUT/pdf
Running Sphinx v7.4.7
RTD Build - Project dir: /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest
RTD Build - Source dir: /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/src
RTD Build - Python path includes: True
Sphinx configuration loaded for BioRemPP 0.6.1.post1.dev2
loading translations [en]... done
making output directory... done
Converting `source_suffix = ['.rst', '.md']` to `source_suffix = {'.rst': 'restructuredtext', '.md': 'restructuredtext'}`.
loading pickled environment... done
myst v2.0.0: MdParserConfig(commonmark_only=False, gfm_only=False, enable_extensions={'substitution', 'linkify', 'deflist', 'dollarmath', 'tasklist', 'smartquotes', 'html_image', 'colon_fence'}, disable_syntax=[], all_links_external=False, url_schemes=('http', 'https', 'mailto', 'ftp'), ref_domains=None, fence_as_directive=set(), number_code_blocks=[], title_to_header=False, heading_anchors=0, heading_slug_func=None, html_meta={}, footnote_transition=True, words_per_minute=200, substitutions={}, linkify_fuzzy_links=True, dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', enable_checkboxes=False, suppress_warnings=[], highlight_code_blocks=True)
[autosummary] generating autosummary for: API_Reference.md, DOCUMENTATION_BUILD_REPORT.md, DOCUMENTATION_GUIDE.md, Test_Suite_Documentation.md, authors.md, changelog.md, contributing.md, index.md, license.md, overview.md, readme.md
building [mo]: targets for 0 po files that are out of date
writing output...
building [latex]: all documents
updating environment: 0 added, 1 changed, 0 removed
reading sources... [100%] index

/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/index.md:29: WARNING: toctree contains reference to nonexisting document 'api/modules'
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/index.md:37: WARNING: toctree contains reference to nonexisting document 'CONTRIBUTING'
looking for now-outdated files... none found
pickling environment... done
checking consistency... /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/DOCUMENTATION_BUILD_REPORT.md: WARNING: document isn't included in any toctree
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/DOCUMENTATION_GUIDE.md: WARNING: document isn't included in any toctree
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/contributing.md: WARNING: document isn't included in any toctree
done
copying TeX support files... copying TeX support files...
done
processing biorempp.tex... index readme overview API_Reference Test_Suite_Documentation authors changelog license
resolving references...
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:3: WARNING: a suitable image for latex builder not found: ['image/svg+xml'] (https://img.shields.io/badge/python-3.8%2B-blue.svg)
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:3: WARNING: a suitable image for latex builder not found: ['image/svg+xml'] (https://img.shields.io/badge/license-MIT-green.svg)
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:3: WARNING: a suitable image for latex builder not found: ['image/svg+xml'] (https://img.shields.io/badge/github-DougFelipe%2Fbiorempp-blue.svg)
/home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:3: WARNING: a suitable image for latex builder not found: ['image/svg+xml'] (https://deepwiki.com/badge.svg)
done
writing... /home/docs/checkouts/readthedocs.org/user_builds/biorempp/checkouts/latest/docs/readme.md:848: WARNING: Pygments lexer name 'nextflow' is not known
done
build succeeded, 10 warnings.

The LaTeX files are in ../_readthedocs/pdf.
Run 'make' in that directory to run these through (pdf)latex
(use `make latexpdf' here to do that automatically).

[rtd-command-info] start-time: 2025-08-16T17:44:01.810444Z, end-time: 2025-08-16T17:44:01.849467Z, duration: 0, exit-code: 0
cat latexmkrc
$latex = 'latex ' . $ENV{'LATEXOPTS'} . ' %O %S';
$pdflatex = 'pdflatex ' . $ENV{'LATEXOPTS'} . ' %O %S';
$lualatex = 'lualatex ' . $ENV{'LATEXOPTS'} . ' %O %S';
$xelatex = 'xelatex --no-pdf ' . $ENV{'LATEXOPTS'} . ' %O %S';
$makeindex = 'makeindex -s python.ist %O -o %D %S';
add_cus_dep( "glo", "gls", 0, "makeglo" );
sub makeglo {
 return system( "makeindex -s gglo.ist -o '$_[0].gls' '$_[0].glo'" );
}

[rtd-command-info] start-time: 2025-08-16T17:44:01.900502Z, end-time: 2025-08-16T17:44:06.038093Z, duration: 4, exit-code: 0
latexmk -r latexmkrc -pdf -f -dvi- -ps- -jobname=biorempp -interaction=nonstopmode
Use of uninitialized value in concatenation (.) or string at (eval 10) line 1.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 2.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 3.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 4.
Subroutine makeglo redefined at (eval 11) line 7.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 1.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 2.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 3.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 4.
Rc files read:
  /etc/LatexMk
  latexmkrc
  latexmkrc
Latexmk: This is Latexmk, John Collins, 20 November 2021, version: 4.76.
Rule 'pdflatex': File changes, etc:
   Changed files, or newly in use since previous run(s):
      'biorempp.tex'
------------
Run number 1 of rule 'pdflatex'
------------
------------
Running 'pdflatex   -interaction=nonstopmode -recorder --jobname="biorempp"  "biorempp.tex"'
------------
Latexmk: applying rule 'pdflatex'...
This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2022/dev/Debian) (preloaded format=pdflatex)
 restricted \write18 enabled.
entering extended mode
(./biorempp.tex
LaTeX2e <2021-11-15> patch level 1
L3 programming layer <2022-01-21> (./sphinxmanual.cls
Document Class: sphinxmanual 2019/12/01 v2.3.0 Document class (Sphinx manual)
(/usr/share/texlive/texmf-dist/tex/latex/base/report.cls
Document Class: report 2021/10/04 v1.4n Standard LaTeX document class
(/usr/share/texlive/texmf-dist/tex/latex/base/size10.clo)))
(/usr/share/texlive/texmf-dist/tex/latex/base/inputenc.sty)
(/usr/share/texlive/texmf-dist/tex/latex/cmap/cmap.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/fontenc.sty<<t1.cmap>>)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsmath.sty
For additional information on amsmath, use the `?' option.
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amstext.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsgen.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsbsy.sty)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsopn.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amssymb.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amsfonts.sty))
(/usr/share/texlive/texmf-dist/tex/generic/babel/babel.sty
(/usr/share/texlive/texmf-dist/tex/generic/babel/txtbabel.def)
(/usr/share/texlive/texmf-dist/tex/generic/babel-english/english.ldf))
(/usr/share/texmf/tex/latex/tex-gyre/tgtermes.sty
(/usr/share/texlive/texmf-dist/tex/latex/kvoptions/kvoptions.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/keyval.sty)
(/usr/share/texlive/texmf-dist/tex/generic/ltxcmds/ltxcmds.sty)
(/usr/share/texlive/texmf-dist/tex/generic/kvsetkeys/kvsetkeys.sty)))
(/usr/share/texmf/tex/latex/tex-gyre/tgheros.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fncychap/fncychap.sty) (./sphinx.sty
(/usr/share/texlive/texmf-dist/tex/latex/xcolor/xcolor.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/color.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-def/pdftex.def))
(./sphinxoptionshyperref.sty) (./sphinxoptionsgeometry.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/textcomp.sty)
(/usr/share/texlive/texmf-dist/tex/latex/float/float.sty)
(/usr/share/texlive/texmf-dist/tex/latex/wrapfig/wrapfig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/capt-of/capt-of.sty)
(/usr/share/texlive/texmf-dist/tex/latex/tools/multicol.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphicx.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphics.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/trig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/graphics.cfg)))
(./sphinxlatexgraphics.sty) (./sphinxpackageboxes.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/p2e-pdftex.def))
(/usr/share/texlive/texmf-dist/tex/latex/ellipse/ellipse.sty))
(./sphinxlatexadmonitions.sty
(/usr/share/texlive/texmf-dist/tex/latex/framed/framed.sty))
(./sphinxlatexliterals.sty
(/usr/share/texlive/texmf-dist/tex/latex/fancyvrb/fancyvrb.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/alltt.sty)
(/usr/share/texlive/texmf-dist/tex/latex/upquote/upquote.sty)
(/usr/share/texlive/texmf-dist/tex/latex/needspace/needspace.sty))
(./sphinxlatexshadowbox.sty) (./sphinxlatexcontainers.sty)
(./sphinxhighlight.sty) (./sphinxlatextables.sty
(/usr/share/texlive/texmf-dist/tex/latex/tabulary/tabulary.sty
(/usr/share/texlive/texmf-dist/tex/latex/tools/array.sty))
(/usr/share/texlive/texmf-dist/tex/latex/tools/longtable.sty)
(/usr/share/texlive/texmf-dist/tex/latex/varwidth/varwidth.sty)
(/usr/share/texlive/texmf-dist/tex/latex/colortbl/colortbl.sty)
(/usr/share/texlive/texmf-dist/tex/latex/booktabs/booktabs.sty))
(./sphinxlatexnumfig.sty) (./sphinxlatexlists.sty) (./sphinxpackagefootnote.sty
) (./sphinxlatexindbibtoc.sty
(/usr/share/texlive/texmf-dist/tex/latex/base/makeidx.sty))
(./sphinxlatexstylepage.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip-2001-04-09.sty))
(/usr/share/texlive/texmf-dist/tex/latex/fancyhdr/fancyhdr.sty))
(./sphinxlatexstyleheadings.sty
(/usr/share/texlive/texmf-dist/tex/latex/titlesec/titlesec.sty))
(./sphinxlatexstyletext.sty) (./sphinxlatexobjects.sty))
(/usr/share/texlive/texmf-dist/tex/latex/geometry/geometry.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/ifvtex.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/iftex.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref.sty
(/usr/share/texlive/texmf-dist/tex/generic/pdftexcmds/pdftexcmds.sty
(/usr/share/texlive/texmf-dist/tex/generic/infwarerr/infwarerr.sty))
(/usr/share/texlive/texmf-dist/tex/generic/kvdefinekeys/kvdefinekeys.sty)
(/usr/share/texlive/texmf-dist/tex/generic/pdfescape/pdfescape.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hycolor/hycolor.sty)
(/usr/share/texlive/texmf-dist/tex/latex/letltxmacro/letltxmacro.sty)
(/usr/share/texlive/texmf-dist/tex/latex/auxhook/auxhook.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/pd1enc.def)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref-langpatches.def)
(/usr/share/texlive/texmf-dist/tex/generic/intcalc/intcalc.sty)
(/usr/share/texlive/texmf-dist/tex/generic/etexcmds/etexcmds.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/puenc.def)
(/usr/share/texlive/texmf-dist/tex/latex/url/url.sty)
(/usr/share/texlive/texmf-dist/tex/generic/bitset/bitset.sty
(/usr/share/texlive/texmf-dist/tex/generic/bigintcalc/bigintcalc.sty))
(/usr/share/texlive/texmf-dist/tex/latex/base/atbegshi-ltx.sty))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hpdftex.def
(/usr/share/texlive/texmf-dist/tex/latex/base/atveryend-ltx.sty)
(/usr/share/texlive/texmf-dist/tex/latex/rerunfilecheck/rerunfilecheck.sty
(/usr/share/texlive/texmf-dist/tex/generic/uniquecounter/uniquecounter.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/oberdiek/hypcap.sty)
(./sphinxmessages.sty)
Writing index file biorempp.idx
(/usr/share/texmf/tex/latex/tex-gyre/t1qtm.fd)
(/usr/share/texlive/texmf-dist/tex/latex/l3backend/l3backend-pdftex.def)
(./biorempp.aux)
(/usr/share/texlive/texmf-dist/tex/context/base/mkii/supp-pdf.mkii
[Loading MPS to PDF converter (version 2006.09.02).]
) (/usr/share/texlive/texmf-dist/tex/latex/epstopdf-pkg/epstopdf-base.sty
(/usr/share/texlive/texmf-dist/tex/latex/latexconfig/epstopdf-sys.cfg))
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5.sty
(/usr/share/texlive/texmf-dist/tex/latex/l3kernel/expl3.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/l3keys2e/l3keys2e.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/xparse/xparse.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-generic-help
er.sty
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-mapping.def)
))
*geometry* driver: auto-detecting
*geometry* detected driver: pdftex
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/nameref.sty
(/usr/share/texlive/texmf-dist/tex/latex/refcount/refcount.sty)
(/usr/share/texlive/texmf-dist/tex/generic/gettitlestring/gettitlestring.sty))
(/usr/share/texmf/tex/latex/tex-gyre/t1qhv.fd)<<ot1.cmap>><<oml.cmap>><<oms.cma
p>><<omx.cmap>> (/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsa.fd)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsb.fd) [1{/var/lib/texmf/fo
nts/map/pdftex/updmap/pdftex.map}] [2] [1] [2] [1] [2]
Chapter 1.
(/usr/share/texmf/tex/latex/tex-gyre/ts1qtm.fd) [3] [4]
Chapter 2.
Runaway argument?
{\sphinxincludegraphics {{/home/docs/checkouts/readthedocs.org/user_b\ETC.
! Paragraph ended before \sphinxhref was complete.
<to be read again>
                   \par
l.138


LaTeX Warning: Hyper reference `overview::doc' on page 5 undefined on input lin
e 145.


LaTeX Warning: Hyper reference `readme:database-specifications' on page 5 undef
ined on input line 149.


LaTeX Warning: Hyper reference `readme:installation' on page 5 undefined on inp
ut line 153.


LaTeX Warning: Hyper reference `readme:command-line-interface' on page 5 undefi
ned on input line 157.


LaTeX Warning: Hyper reference `readme:input-data-format' on page 5 undefined o
n input line 161.


LaTeX Warning: Hyper reference `readme:output-data-format' on page 5 undefined
on input line 165.


LaTeX Warning: Hyper reference `readme:usage-examples' on page 5 undefined on i
nput line 169.


LaTeX Warning: Hyper reference `readme:python-api' on page 5 undefined on input
 line 173.


LaTeX Warning: Hyper reference `readme:system-architecture' on page 5 undefined
 on input line 177.


LaTeX Warning: Hyper reference `readme:pipeline-integration' on page 5 undefine
d on input line 181.


LaTeX Warning: Hyper reference `readme:troubleshooting' on page 5 undefined on
input line 185.

[5]

! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.236 ✅
          \sphinxstylestrong{Command Pattern Implementation}: Robust CLI arc...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.240 ✅
          \sphinxstylestrong{Multi\sphinxhyphen{}Level Verbosity Control}: C...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.244 ✅
          \sphinxstylestrong{Structured Output Generation}: Standards\sphinx...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.248 ✅
          \sphinxstylestrong{Advanced Error Handling}: Comprehensive excepti...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.252 ✅
          \sphinxstylestrong{Type\sphinxhyphen{}Optimized Processing}: Memor...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.256 ✅
          \sphinxstylestrong{Reproducible Workflows}: Deterministic processi...


Overfull \hbox (8.86438pt too wide) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 Records|

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 File

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/b/n/10 BioRemPP

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.69

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.04

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.02

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.18
[6] [7] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/t1txtt.fd)

! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.571 \sphinxstylestrong{pandas} (≥
                                     2.0.0): High\sphinxhyphen{}performance ...


! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.575 \sphinxstylestrong{numpy} (≥
                                    1.21.0): Fundamental numerical computing...

[8]
Underfull \hbox (badness 10000) in paragraph at lines 802--802
[][][]\T1/txtt/m/n/10 input data/sample_data.

Underfull \hbox (badness 10000) in paragraph at lines 802--802
[]\T1/qtm/m/n/10 di-rec-
[9] [10] [11] [12]

! LaTeX Error: Unicode character 🎉 (U+1F389)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1102 🎉 Processing completed successfully!


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1103 ...ts: 1,247 total matches across databases


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1104    📁 Output Files Generated:


! LaTeX Error: Unicode character ⏱ (U+23F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character 💾 (U+1F4BE)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1110    💾 Total Output Size: 524KB

[13] [14] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/ts1txtt.fd) [15]
[16]

! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1435 ...h\PYGZhy{}level processing orchestration


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1440 ...GZsh{} Data validation and preprocessing


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1443 ...nd\PYGZhy{}line interface implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1446 ...\PYGZsh{} Command Pattern implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1450 ...{} Application core and factory patterns


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1453 ... \PYGZsh{} Utility functions and helpers


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1457 ...       \PYGZsh{} Embedded database files

[17] [18] [19] [20] [21] [22]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1905 ...}not\PYG{+w}{ }found:\PYG{+w}{ }data.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1907 💡\PYG{+w}{ }Solutions:

[23]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1918 ...nput\PYG{+w}{ }format\PYG{+w}{ }detected


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1920 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1932 ...YG{k}{in}\PYG{+w}{ }input\PYG{+w}{ }file


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1934 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1948 ...}\PYGZhy{}\PYGZhy{}all\PYGZhy{}databases


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1950 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1960 ...1}{\PYGZsq{}invalid\PYGZus{}db\PYGZsq{}}


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1963 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1976 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1978 💡\PYG{+w}{ }Solutions:

[24]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1989 ...r}\PYG{+w}{ }output\PYG{+w}{ }generation


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1991 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2005 ...}\PYG{+w}{ }dataset\PYG{+w}{ }processing


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2007 💡\PYG{+w}{ }Solutions:

[25] [26] [27] [28]

LaTeX Warning: Hyper reference `readme:LICENSE.txt' on page 29 undefined on inp
ut line 2409.


! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2465 \subsection{🔧 Solução de Problemas}


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2474 ...not\PYG{+w}{ }found:\PYG{+w}{ }dados.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2476 💡\PYG{+w}{ }Solutions:

[29]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2489 ...Invalid\PYG{+w}{ }input\PYG{+w}{ }format


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2491 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2504 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2506 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character 📧 (U+1F4E7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2529 📧
            \sphinxstylestrong{Email}: \sphinxhref{mailto:suporte@biorempp.o...


! LaTeX Error: Unicode character 🐛 (U+1F41B)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2533 🐛
            \sphinxstylestrong{Issues}: \sphinxhref{https://github.com/DougF...


! LaTeX Error: Unicode character 📖 (U+1F4D6)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2537 📖
            \sphinxstylestrong{Documentação}: \sphinxhref{https://biorempp...


! LaTeX Error: Unicode character 📄 (U+1F4C4)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2546 \subsection{📄 Licença}


LaTeX Warning: Hyper reference `readme:LICENSE' on page 30 undefined on input l
ine 2549.

[30]

! LaTeX Error: Unicode character 🙏 (U+1F64F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2556 \subsection{🙏 Agradecimentos}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2581 \subsection{📊 Estatísticas do Projeto}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2614 ...m insights para remediação ambiental.}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2622 \subsection{🧬 About BioRemPP}


! LaTeX Error: Unicode character 🏗 (U+1F3D7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character 📱 (U+1F4F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2634 ...lintitle{\sphinxupquote{biorempp.app}})}

[31]

! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2651 ...ntitle{\sphinxupquote{biorempp.utils}})}


! LaTeX Error: Unicode character 💻 (U+1F4BB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2676 ...lintitle{\sphinxupquote{biorempp.cli}})}


! LaTeX Error: Unicode character ⚡ (U+26A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2689 ...tle{\sphinxupquote{biorempp.commands}})}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2706 ...nxupquote{biorempp.input\_processing}})}


! LaTeX Error: Unicode character 🔬 (U+1F52C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2723 ...le{\sphinxupquote{biorempp.pipelines}})}


! LaTeX Error: Unicode character 🚀 (U+1F680)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2736 \subsection{🚀 Key Features}

[32]

! LaTeX Error: Unicode character 📋 (U+1F4CB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2819 \subsection{📋 Usage Examples}

[33]

! LaTeX Error: Unicode character 🛠 (U+1F6E0)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character 📚 (U+1F4DA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2897 \subsection{📚 Documentation}


! LaTeX Error: Unicode character 🔗 (U+1F517)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2921 \subsection{🔗 Quick Links}


LaTeX Warning: Hyper reference `overview:api/modules.html' on page 34 undefined
 on input line 2925.


LaTeX Warning: Hyper reference `overview:DOCUMENTATION_GUIDE.html' on page 34 u
ndefined on input line 2929.


LaTeX Warning: Hyper reference `overview:contributing.html' on page 34 undefine
d on input line 2933.


LaTeX Warning: Hyper reference `overview::doc' on page 34 undefined on input li
ne 2955.


LaTeX Warning: Hyper reference `API_Reference:package-structure' on page 34 und
efined on input line 2959.


LaTeX Warning: Hyper reference `API_Reference:core-api' on page 34 undefined on
 input line 2963.


LaTeX Warning: Hyper reference `API_Reference:pipeline-module' on page 34 undef
ined on input line 2967.


LaTeX Warning: Hyper reference `API_Reference:input-processing-module' on page
34 undefined on input line 2971.

[34]

LaTeX Warning: Hyper reference `API_Reference:application-module' on page 35 un
defined on input line 2975.


LaTeX Warning: Hyper reference `API_Reference:cli-module' on page 35 undefined
on input line 2979.


LaTeX Warning: Hyper reference `API_Reference:commands-module' on page 35 undef
ined on input line 2983.


LaTeX Warning: Hyper reference `API_Reference:utils-module' on page 35 undefine
d on input line 2987.


LaTeX Warning: Hyper reference `API_Reference:integration-examples' on page 35
undefined on input line 2991.


LaTeX Warning: Hyper reference `API_Reference:error-handling' on page 35 undefi
ned on input line 2995.


LaTeX Warning: Hyper reference `API_Reference:best-practices' on page 35 undefi
ned on input line 2999.

[35] [36] [37] [38] [39] [40] [41] [42] [43] [44] [45] [46] [47] [48] [49]
[50] [51] [52] [53] [54] [55] [56] [57] [58] [59] [60] [61] [62] [63] [64]
[65] [66] [67] [68] [69] [70] [71] [72] [73] [74] [75] [76]
Chapter 3.

LaTeX Warning: Hyper reference `index:api/modules.rst' on page 77 undefined on
input line 6463.

[77] [78]
Chapter 4.
No file biorempp.ind.
[79] (./biorempp.aux)

LaTeX Warning: There were undefined references.


LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.


Package rerunfilecheck Warning: File `biorempp.out' has changed.
(rerunfilecheck)                Rerun to get outlines right
(rerunfilecheck)                or use package `bookmark'.

 )
(see the transcript file for additional information){/usr/share/texlive/texmf-d
ist/fonts/enc/dvips/base/8r.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ts1.enc}</usr/share/texlive/t
exmf-dist/fonts/type1/public/amsfonts/cm/cmmi5.pfb></usr/share/texlive/texmf-di
st/fonts/type1/public/amsfonts/cm/cmsy10.pfb></usr/share/texlive/texmf-dist/fon
ts/type1/public/amsfonts/cm/cmsy5.pfb></usr/share/texlive/texmf-dist/fonts/type
1/public/amsfonts/symbols/msam10.pfb></usr/share/texmf/fonts/type1/public/tex-g
yre/qhvb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qhvbi.pfb></usr/shar
e/texmf/fonts/type1/public/tex-gyre/qhvr.pfb></usr/share/texmf/fonts/type1/publ
ic/tex-gyre/qtmb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qtmbi.pfb></
usr/share/texmf/fonts/type1/public/tex-gyre/qtmr.pfb></usr/share/texmf/fonts/ty
pe1/public/tex-gyre/qtmri.pfb></usr/share/texlive/texmf-dist/fonts/type1/public
/txfonts/t1xbtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t
1xtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t1xtt.pfb></
usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/tcxtt.pfb></usr/share/t
exlive/texmf-dist/fonts/type1/urw/times/utmr8a.pfb>
Output written on biorempp.pdf (83 pages, 407880 bytes).
Transcript written on biorempp.log.
Latexmk: Index file 'biorempp.idx' was written
Latexmk: Missing input file 'biorempp.ind' (or dependence on it) from following:
  'No file biorempp.ind.'
Latexmk: References changed.
Latexmk: References changed.
Latexmk: Log file says output to 'biorempp.pdf'
Rule 'makeindex biorempp.idx': File changes, etc:
   Changed files, or newly in use since previous run(s):
      'biorempp.idx'
------------
Run number 1 of rule 'makeindex biorempp.idx'
------------
------------
Running 'makeindex -s python.ist  -o "biorempp.ind" "biorempp.idx"'
------------
Latexmk: Examining 'biorempp.log'
=== TeX engine is 'pdfTeX'
Latexmk: applying rule 'makeindex biorempp.idx'...
This is makeindex, version 2.15 [TeX Live 2022/dev] (kpathsea + Thai support).
Scanning style file ./python.ist.......done (7 attributes redefined, 0 ignored).
Scanning input file biorempp.idx...done (0 entries accepted, 0 rejected).
Nothing written in biorempp.ind.
Transcript written in biorempp.ilg.
Rule 'pdflatex': File changes, etc:
   Changed files, or newly in use since previous run(s):
      'biorempp.aux'
      'biorempp.ind'
      'biorempp.out'
------------
Run number 2 of rule 'pdflatex'
------------
Latexmk: applying rule 'pdflatex'...
------------
Running 'pdflatex   -interaction=nonstopmode -recorder --jobname="biorempp"  "biorempp.tex"'
------------
This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2022/dev/Debian) (preloaded format=pdflatex)
 restricted \write18 enabled.
entering extended mode
(./biorempp.tex
LaTeX2e <2021-11-15> patch level 1
L3 programming layer <2022-01-21> (./sphinxmanual.cls
Document Class: sphinxmanual 2019/12/01 v2.3.0 Document class (Sphinx manual)
(/usr/share/texlive/texmf-dist/tex/latex/base/report.cls
Document Class: report 2021/10/04 v1.4n Standard LaTeX document class
(/usr/share/texlive/texmf-dist/tex/latex/base/size10.clo)))
(/usr/share/texlive/texmf-dist/tex/latex/base/inputenc.sty)
(/usr/share/texlive/texmf-dist/tex/latex/cmap/cmap.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/fontenc.sty<<t1.cmap>>)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsmath.sty
For additional information on amsmath, use the `?' option.
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amstext.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsgen.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsbsy.sty)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsopn.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amssymb.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amsfonts.sty))
(/usr/share/texlive/texmf-dist/tex/generic/babel/babel.sty
(/usr/share/texlive/texmf-dist/tex/generic/babel/txtbabel.def)
(/usr/share/texlive/texmf-dist/tex/generic/babel-english/english.ldf))
(/usr/share/texmf/tex/latex/tex-gyre/tgtermes.sty
(/usr/share/texlive/texmf-dist/tex/latex/kvoptions/kvoptions.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/keyval.sty)
(/usr/share/texlive/texmf-dist/tex/generic/ltxcmds/ltxcmds.sty)
(/usr/share/texlive/texmf-dist/tex/generic/kvsetkeys/kvsetkeys.sty)))
(/usr/share/texmf/tex/latex/tex-gyre/tgheros.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fncychap/fncychap.sty) (./sphinx.sty
(/usr/share/texlive/texmf-dist/tex/latex/xcolor/xcolor.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/color.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-def/pdftex.def))
(./sphinxoptionshyperref.sty) (./sphinxoptionsgeometry.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/textcomp.sty)
(/usr/share/texlive/texmf-dist/tex/latex/float/float.sty)
(/usr/share/texlive/texmf-dist/tex/latex/wrapfig/wrapfig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/capt-of/capt-of.sty)
(/usr/share/texlive/texmf-dist/tex/latex/tools/multicol.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphicx.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphics.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/trig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/graphics.cfg)))
(./sphinxlatexgraphics.sty) (./sphinxpackageboxes.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/p2e-pdftex.def))
(/usr/share/texlive/texmf-dist/tex/latex/ellipse/ellipse.sty))
(./sphinxlatexadmonitions.sty
(/usr/share/texlive/texmf-dist/tex/latex/framed/framed.sty))
(./sphinxlatexliterals.sty
(/usr/share/texlive/texmf-dist/tex/latex/fancyvrb/fancyvrb.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/alltt.sty)
(/usr/share/texlive/texmf-dist/tex/latex/upquote/upquote.sty)
(/usr/share/texlive/texmf-dist/tex/latex/needspace/needspace.sty))
(./sphinxlatexshadowbox.sty) (./sphinxlatexcontainers.sty)
(./sphinxhighlight.sty) (./sphinxlatextables.sty
(/usr/share/texlive/texmf-dist/tex/latex/tabulary/tabulary.sty
(/usr/share/texlive/texmf-dist/tex/latex/tools/array.sty))
(/usr/share/texlive/texmf-dist/tex/latex/tools/longtable.sty)
(/usr/share/texlive/texmf-dist/tex/latex/varwidth/varwidth.sty)
(/usr/share/texlive/texmf-dist/tex/latex/colortbl/colortbl.sty)
(/usr/share/texlive/texmf-dist/tex/latex/booktabs/booktabs.sty))
(./sphinxlatexnumfig.sty) (./sphinxlatexlists.sty) (./sphinxpackagefootnote.sty
) (./sphinxlatexindbibtoc.sty
(/usr/share/texlive/texmf-dist/tex/latex/base/makeidx.sty))
(./sphinxlatexstylepage.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip-2001-04-09.sty))
(/usr/share/texlive/texmf-dist/tex/latex/fancyhdr/fancyhdr.sty))
(./sphinxlatexstyleheadings.sty
(/usr/share/texlive/texmf-dist/tex/latex/titlesec/titlesec.sty))
(./sphinxlatexstyletext.sty) (./sphinxlatexobjects.sty))
(/usr/share/texlive/texmf-dist/tex/latex/geometry/geometry.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/ifvtex.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/iftex.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref.sty
(/usr/share/texlive/texmf-dist/tex/generic/pdftexcmds/pdftexcmds.sty
(/usr/share/texlive/texmf-dist/tex/generic/infwarerr/infwarerr.sty))
(/usr/share/texlive/texmf-dist/tex/generic/kvdefinekeys/kvdefinekeys.sty)
(/usr/share/texlive/texmf-dist/tex/generic/pdfescape/pdfescape.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hycolor/hycolor.sty)
(/usr/share/texlive/texmf-dist/tex/latex/letltxmacro/letltxmacro.sty)
(/usr/share/texlive/texmf-dist/tex/latex/auxhook/auxhook.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/pd1enc.def)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref-langpatches.def)
(/usr/share/texlive/texmf-dist/tex/generic/intcalc/intcalc.sty)
(/usr/share/texlive/texmf-dist/tex/generic/etexcmds/etexcmds.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/puenc.def)
(/usr/share/texlive/texmf-dist/tex/latex/url/url.sty)
(/usr/share/texlive/texmf-dist/tex/generic/bitset/bitset.sty
(/usr/share/texlive/texmf-dist/tex/generic/bigintcalc/bigintcalc.sty))
(/usr/share/texlive/texmf-dist/tex/latex/base/atbegshi-ltx.sty))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hpdftex.def
(/usr/share/texlive/texmf-dist/tex/latex/base/atveryend-ltx.sty)
(/usr/share/texlive/texmf-dist/tex/latex/rerunfilecheck/rerunfilecheck.sty
(/usr/share/texlive/texmf-dist/tex/generic/uniquecounter/uniquecounter.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/oberdiek/hypcap.sty)
(./sphinxmessages.sty)
Writing index file biorempp.idx
(/usr/share/texmf/tex/latex/tex-gyre/t1qtm.fd)
(/usr/share/texlive/texmf-dist/tex/latex/l3backend/l3backend-pdftex.def)
(./biorempp.aux)
(/usr/share/texlive/texmf-dist/tex/context/base/mkii/supp-pdf.mkii
[Loading MPS to PDF converter (version 2006.09.02).]
) (/usr/share/texlive/texmf-dist/tex/latex/epstopdf-pkg/epstopdf-base.sty
(/usr/share/texlive/texmf-dist/tex/latex/latexconfig/epstopdf-sys.cfg))
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5.sty
(/usr/share/texlive/texmf-dist/tex/latex/l3kernel/expl3.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/l3keys2e/l3keys2e.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/xparse/xparse.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-generic-help
er.sty
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-mapping.def)
))
*geometry* driver: auto-detecting
*geometry* detected driver: pdftex
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/nameref.sty
(/usr/share/texlive/texmf-dist/tex/latex/refcount/refcount.sty)
(/usr/share/texlive/texmf-dist/tex/generic/gettitlestring/gettitlestring.sty))
(./biorempp.out) (./biorempp.out) (/usr/share/texmf/tex/latex/tex-gyre/t1qhv.fd
)<<ot1.cmap>><<oml.cmap>><<oms.cmap>><<omx.cmap>>
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsa.fd)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsb.fd) [1{/var/lib/texmf/fo
nts/map/pdftex/updmap/pdftex.map}] [2] (./biorempp.toc) [1] [2] [1] [2]
Chapter 1.
(/usr/share/texmf/tex/latex/tex-gyre/ts1qtm.fd) [3] [4]
Chapter 2.
Runaway argument?
{\sphinxincludegraphics {{/home/docs/checkouts/readthedocs.org/user_b\ETC.
! Paragraph ended before \sphinxhref was complete.
<to be read again>
                   \par
l.138

[5]

! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.236 ✅
          \sphinxstylestrong{Command Pattern Implementation}: Robust CLI arc...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.240 ✅
          \sphinxstylestrong{Multi\sphinxhyphen{}Level Verbosity Control}: C...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.244 ✅
          \sphinxstylestrong{Structured Output Generation}: Standards\sphinx...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.248 ✅
          \sphinxstylestrong{Advanced Error Handling}: Comprehensive excepti...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.252 ✅
          \sphinxstylestrong{Type\sphinxhyphen{}Optimized Processing}: Memor...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.256 ✅
          \sphinxstylestrong{Reproducible Workflows}: Deterministic processi...


Overfull \hbox (8.86438pt too wide) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 Records|

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 File

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/b/n/10 BioRemPP

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.69

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.04

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.02

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.18
[6] [7] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/t1txtt.fd)

! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.571 \sphinxstylestrong{pandas} (≥
                                     2.0.0): High\sphinxhyphen{}performance ...


! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.575 \sphinxstylestrong{numpy} (≥
                                    1.21.0): Fundamental numerical computing...

[8]
Underfull \hbox (badness 10000) in paragraph at lines 802--802
[][][]\T1/txtt/m/n/10 input data/sample_data.

Underfull \hbox (badness 10000) in paragraph at lines 802--802
[]\T1/qtm/m/n/10 di-rec-
[9] [10] [11] [12]

! LaTeX Error: Unicode character 🎉 (U+1F389)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1102 🎉 Processing completed successfully!


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1103 ...ts: 1,247 total matches across databases


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1104    📁 Output Files Generated:


! LaTeX Error: Unicode character ⏱ (U+23F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character 💾 (U+1F4BE)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1110    💾 Total Output Size: 524KB

[13] [14] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/ts1txtt.fd) [15]
[16]

! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1435 ...h\PYGZhy{}level processing orchestration


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1440 ...GZsh{} Data validation and preprocessing


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1443 ...nd\PYGZhy{}line interface implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1446 ...\PYGZsh{} Command Pattern implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1450 ...{} Application core and factory patterns


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1453 ... \PYGZsh{} Utility functions and helpers


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1457 ...       \PYGZsh{} Embedded database files

[17] [18] [19] [20] [21] [22]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1905 ...}not\PYG{+w}{ }found:\PYG{+w}{ }data.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1907 💡\PYG{+w}{ }Solutions:

[23]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1918 ...nput\PYG{+w}{ }format\PYG{+w}{ }detected


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1920 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1932 ...YG{k}{in}\PYG{+w}{ }input\PYG{+w}{ }file


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1934 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1948 ...}\PYGZhy{}\PYGZhy{}all\PYGZhy{}databases


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1950 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1960 ...1}{\PYGZsq{}invalid\PYGZus{}db\PYGZsq{}}


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1963 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1976 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1978 💡\PYG{+w}{ }Solutions:

[24]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1989 ...r}\PYG{+w}{ }output\PYG{+w}{ }generation


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1991 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2005 ...}\PYG{+w}{ }dataset\PYG{+w}{ }processing


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2007 💡\PYG{+w}{ }Solutions:

[25] [26] [27] [28]

LaTeX Warning: Hyper reference `readme:LICENSE.txt' on page 29 undefined on inp
ut line 2409.


! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2465 \subsection{🔧 Solução de Problemas}


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2474 ...not\PYG{+w}{ }found:\PYG{+w}{ }dados.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2476 💡\PYG{+w}{ }Solutions:

[29]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2489 ...Invalid\PYG{+w}{ }input\PYG{+w}{ }format


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2491 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2504 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2506 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character 📧 (U+1F4E7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2529 📧
            \sphinxstylestrong{Email}: \sphinxhref{mailto:suporte@biorempp.o...


! LaTeX Error: Unicode character 🐛 (U+1F41B)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2533 🐛
            \sphinxstylestrong{Issues}: \sphinxhref{https://github.com/DougF...


! LaTeX Error: Unicode character 📖 (U+1F4D6)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2537 📖
            \sphinxstylestrong{Documentação}: \sphinxhref{https://biorempp...


! LaTeX Error: Unicode character 📄 (U+1F4C4)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2546 \subsection{📄 Licença}


LaTeX Warning: Hyper reference `readme:LICENSE' on page 30 undefined on input l
ine 2549.

[30]

! LaTeX Error: Unicode character 🙏 (U+1F64F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2556 \subsection{🙏 Agradecimentos}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2581 \subsection{📊 Estatísticas do Projeto}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2614 ...m insights para remediação ambiental.}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2622 \subsection{🧬 About BioRemPP}


! LaTeX Error: Unicode character 🏗 (U+1F3D7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character 📱 (U+1F4F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2634 ...lintitle{\sphinxupquote{biorempp.app}})}

[31]

! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2651 ...ntitle{\sphinxupquote{biorempp.utils}})}


! LaTeX Error: Unicode character 💻 (U+1F4BB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2676 ...lintitle{\sphinxupquote{biorempp.cli}})}


! LaTeX Error: Unicode character ⚡ (U+26A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2689 ...tle{\sphinxupquote{biorempp.commands}})}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2706 ...nxupquote{biorempp.input\_processing}})}


! LaTeX Error: Unicode character 🔬 (U+1F52C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2723 ...le{\sphinxupquote{biorempp.pipelines}})}


! LaTeX Error: Unicode character 🚀 (U+1F680)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2736 \subsection{🚀 Key Features}

[32]

! LaTeX Error: Unicode character 📋 (U+1F4CB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2819 \subsection{📋 Usage Examples}

[33]

! LaTeX Error: Unicode character 🛠 (U+1F6E0)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character 📚 (U+1F4DA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2897 \subsection{📚 Documentation}


! LaTeX Error: Unicode character 🔗 (U+1F517)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2921 \subsection{🔗 Quick Links}


LaTeX Warning: Hyper reference `overview:api/modules.html' on page 34 undefined
 on input line 2925.


LaTeX Warning: Hyper reference `overview:DOCUMENTATION_GUIDE.html' on page 34 u
ndefined on input line 2929.


LaTeX Warning: Hyper reference `overview:contributing.html' on page 34 undefine
d on input line 2933.

[34] [35] [36] [37] [38] [39] [40] [41] [42] [43] [44] [45] [46] [47] [48]
[49] [50] [51] [52] [53] [54] [55] [56] [57] [58] [59] [60] [61] [62] [63]
[64] [65] [66] [67] [68] [69] [70] [71] [72] [73] [74] [75] [76]
Chapter 3.

LaTeX Warning: Hyper reference `index:api/modules.rst' on page 77 undefined on
input line 6463.

[77] [78]
Chapter 4.
(./biorempp.ind) [79] (./biorempp.aux)

LaTeX Warning: There were undefined references.

 )
(see the transcript file for additional information){/usr/share/texlive/texmf-d
ist/fonts/enc/dvips/base/8r.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ts1.enc}</usr/share/texlive/t
exmf-dist/fonts/type1/public/amsfonts/cm/cmmi5.pfb></usr/share/texlive/texmf-di
st/fonts/type1/public/amsfonts/cm/cmsy10.pfb></usr/share/texlive/texmf-dist/fon
ts/type1/public/amsfonts/cm/cmsy5.pfb></usr/share/texlive/texmf-dist/fonts/type
1/public/amsfonts/symbols/msam10.pfb></usr/share/texmf/fonts/type1/public/tex-g
yre/qhvb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qhvbi.pfb></usr/shar
e/texmf/fonts/type1/public/tex-gyre/qhvr.pfb></usr/share/texmf/fonts/type1/publ
ic/tex-gyre/qtmb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qtmbi.pfb></
usr/share/texmf/fonts/type1/public/tex-gyre/qtmr.pfb></usr/share/texmf/fonts/ty
pe1/public/tex-gyre/qtmri.pfb></usr/share/texlive/texmf-dist/fonts/type1/public
/txfonts/t1xbtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t
1xtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t1xtt.pfb></
usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/tcxtt.pfb></usr/share/t
exlive/texmf-dist/fonts/type1/urw/times/utmr8a.pfb>
Output written on biorempp.pdf (83 pages, 427752 bytes).
Transcript written on biorempp.log.
Latexmk: Index file 'biorempp.idx' was written
Latexmk: Log file says output to 'biorempp.pdf'
Rule 'pdflatex': File changes, etc:
   Changed files, or newly in use since previous run(s):
      'biorempp.toc'
------------
Run number 3 of rule 'pdflatex'
------------
Latexmk: Examining 'biorempp.log'
=== TeX engine is 'pdfTeX'
Latexmk: applying rule 'pdflatex'...
------------
Running 'pdflatex   -interaction=nonstopmode -recorder --jobname="biorempp"  "biorempp.tex"'
------------
This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2022/dev/Debian) (preloaded format=pdflatex)
 restricted \write18 enabled.
entering extended mode
(./biorempp.tex
LaTeX2e <2021-11-15> patch level 1
L3 programming layer <2022-01-21> (./sphinxmanual.cls
Document Class: sphinxmanual 2019/12/01 v2.3.0 Document class (Sphinx manual)
(/usr/share/texlive/texmf-dist/tex/latex/base/report.cls
Document Class: report 2021/10/04 v1.4n Standard LaTeX document class
(/usr/share/texlive/texmf-dist/tex/latex/base/size10.clo)))
(/usr/share/texlive/texmf-dist/tex/latex/base/inputenc.sty)
(/usr/share/texlive/texmf-dist/tex/latex/cmap/cmap.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/fontenc.sty<<t1.cmap>>)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsmath.sty
For additional information on amsmath, use the `?' option.
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amstext.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsgen.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsbsy.sty)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsopn.sty))
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amssymb.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/amsfonts.sty))
(/usr/share/texlive/texmf-dist/tex/generic/babel/babel.sty
(/usr/share/texlive/texmf-dist/tex/generic/babel/txtbabel.def)
(/usr/share/texlive/texmf-dist/tex/generic/babel-english/english.ldf))
(/usr/share/texmf/tex/latex/tex-gyre/tgtermes.sty
(/usr/share/texlive/texmf-dist/tex/latex/kvoptions/kvoptions.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/keyval.sty)
(/usr/share/texlive/texmf-dist/tex/generic/ltxcmds/ltxcmds.sty)
(/usr/share/texlive/texmf-dist/tex/generic/kvsetkeys/kvsetkeys.sty)))
(/usr/share/texmf/tex/latex/tex-gyre/tgheros.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fncychap/fncychap.sty) (./sphinx.sty
(/usr/share/texlive/texmf-dist/tex/latex/xcolor/xcolor.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/color.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-def/pdftex.def))
(./sphinxoptionshyperref.sty) (./sphinxoptionsgeometry.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/textcomp.sty)
(/usr/share/texlive/texmf-dist/tex/latex/float/float.sty)
(/usr/share/texlive/texmf-dist/tex/latex/wrapfig/wrapfig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/capt-of/capt-of.sty)
(/usr/share/texlive/texmf-dist/tex/latex/tools/multicol.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphicx.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/graphics.sty
(/usr/share/texlive/texmf-dist/tex/latex/graphics/trig.sty)
(/usr/share/texlive/texmf-dist/tex/latex/graphics-cfg/graphics.cfg)))
(./sphinxlatexgraphics.sty) (./sphinxpackageboxes.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.sty
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/pict2e.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/pict2e/p2e-pdftex.def))
(/usr/share/texlive/texmf-dist/tex/latex/ellipse/ellipse.sty))
(./sphinxlatexadmonitions.sty
(/usr/share/texlive/texmf-dist/tex/latex/framed/framed.sty))
(./sphinxlatexliterals.sty
(/usr/share/texlive/texmf-dist/tex/latex/fancyvrb/fancyvrb.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/alltt.sty)
(/usr/share/texlive/texmf-dist/tex/latex/upquote/upquote.sty)
(/usr/share/texlive/texmf-dist/tex/latex/needspace/needspace.sty))
(./sphinxlatexshadowbox.sty) (./sphinxlatexcontainers.sty)
(./sphinxhighlight.sty) (./sphinxlatextables.sty
(/usr/share/texlive/texmf-dist/tex/latex/tabulary/tabulary.sty
(/usr/share/texlive/texmf-dist/tex/latex/tools/array.sty))
(/usr/share/texlive/texmf-dist/tex/latex/tools/longtable.sty)
(/usr/share/texlive/texmf-dist/tex/latex/varwidth/varwidth.sty)
(/usr/share/texlive/texmf-dist/tex/latex/colortbl/colortbl.sty)
(/usr/share/texlive/texmf-dist/tex/latex/booktabs/booktabs.sty))
(./sphinxlatexnumfig.sty) (./sphinxlatexlists.sty) (./sphinxpackagefootnote.sty
) (./sphinxlatexindbibtoc.sty
(/usr/share/texlive/texmf-dist/tex/latex/base/makeidx.sty))
(./sphinxlatexstylepage.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip.sty
(/usr/share/texlive/texmf-dist/tex/latex/parskip/parskip-2001-04-09.sty))
(/usr/share/texlive/texmf-dist/tex/latex/fancyhdr/fancyhdr.sty))
(./sphinxlatexstyleheadings.sty
(/usr/share/texlive/texmf-dist/tex/latex/titlesec/titlesec.sty))
(./sphinxlatexstyletext.sty) (./sphinxlatexobjects.sty))
(/usr/share/texlive/texmf-dist/tex/latex/geometry/geometry.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/ifvtex.sty
(/usr/share/texlive/texmf-dist/tex/generic/iftex/iftex.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref.sty
(/usr/share/texlive/texmf-dist/tex/generic/pdftexcmds/pdftexcmds.sty
(/usr/share/texlive/texmf-dist/tex/generic/infwarerr/infwarerr.sty))
(/usr/share/texlive/texmf-dist/tex/generic/kvdefinekeys/kvdefinekeys.sty)
(/usr/share/texlive/texmf-dist/tex/generic/pdfescape/pdfescape.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hycolor/hycolor.sty)
(/usr/share/texlive/texmf-dist/tex/latex/letltxmacro/letltxmacro.sty)
(/usr/share/texlive/texmf-dist/tex/latex/auxhook/auxhook.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/pd1enc.def)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hyperref-langpatches.def)
(/usr/share/texlive/texmf-dist/tex/generic/intcalc/intcalc.sty)
(/usr/share/texlive/texmf-dist/tex/generic/etexcmds/etexcmds.sty)
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/puenc.def)
(/usr/share/texlive/texmf-dist/tex/latex/url/url.sty)
(/usr/share/texlive/texmf-dist/tex/generic/bitset/bitset.sty
(/usr/share/texlive/texmf-dist/tex/generic/bigintcalc/bigintcalc.sty))
(/usr/share/texlive/texmf-dist/tex/latex/base/atbegshi-ltx.sty))
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/hpdftex.def
(/usr/share/texlive/texmf-dist/tex/latex/base/atveryend-ltx.sty)
(/usr/share/texlive/texmf-dist/tex/latex/rerunfilecheck/rerunfilecheck.sty
(/usr/share/texlive/texmf-dist/tex/generic/uniquecounter/uniquecounter.sty)))
(/usr/share/texlive/texmf-dist/tex/latex/oberdiek/hypcap.sty)
(./sphinxmessages.sty)
Writing index file biorempp.idx
(/usr/share/texmf/tex/latex/tex-gyre/t1qtm.fd)
(/usr/share/texlive/texmf-dist/tex/latex/l3backend/l3backend-pdftex.def)
(./biorempp.aux)
(/usr/share/texlive/texmf-dist/tex/context/base/mkii/supp-pdf.mkii
[Loading MPS to PDF converter (version 2006.09.02).]
) (/usr/share/texlive/texmf-dist/tex/latex/epstopdf-pkg/epstopdf-base.sty
(/usr/share/texlive/texmf-dist/tex/latex/latexconfig/epstopdf-sys.cfg))
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5.sty
(/usr/share/texlive/texmf-dist/tex/latex/l3kernel/expl3.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/l3keys2e/l3keys2e.sty)
(/usr/share/texlive/texmf-dist/tex/latex/l3packages/xparse/xparse.sty)
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-generic-help
er.sty
(/usr/share/texlive/texmf-dist/tex/latex/fontawesome5/fontawesome5-mapping.def)
))
*geometry* driver: auto-detecting
*geometry* detected driver: pdftex
(/usr/share/texlive/texmf-dist/tex/latex/hyperref/nameref.sty
(/usr/share/texlive/texmf-dist/tex/latex/refcount/refcount.sty)
(/usr/share/texlive/texmf-dist/tex/generic/gettitlestring/gettitlestring.sty))
(./biorempp.out) (./biorempp.out) (/usr/share/texmf/tex/latex/tex-gyre/t1qhv.fd
)<<ot1.cmap>><<oml.cmap>><<oms.cmap>><<omx.cmap>>
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsa.fd)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsb.fd) [1{/var/lib/texmf/fo
nts/map/pdftex/updmap/pdftex.map}] [2] (./biorempp.toc) [1] [2] [1] [2]
Chapter 1.
(/usr/share/texmf/tex/latex/tex-gyre/ts1qtm.fd) [3] [4]
Chapter 2.
Runaway argument?
{\sphinxincludegraphics {{/home/docs/checkouts/readthedocs.org/user_b\ETC.
! Paragraph ended before \sphinxhref was complete.
<to be read again>
                   \par
l.138

[5]

! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.236 ✅
          \sphinxstylestrong{Command Pattern Implementation}: Robust CLI arc...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.240 ✅
          \sphinxstylestrong{Multi\sphinxhyphen{}Level Verbosity Control}: C...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.244 ✅
          \sphinxstylestrong{Structured Output Generation}: Standards\sphinx...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.248 ✅
          \sphinxstylestrong{Advanced Error Handling}: Comprehensive excepti...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.252 ✅
          \sphinxstylestrong{Type\sphinxhyphen{}Optimized Processing}: Memor...


! LaTeX Error: Unicode character ✅ (U+2705)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.256 ✅
          \sphinxstylestrong{Reproducible Workflows}: Deterministic processi...


Overfull \hbox (8.86438pt too wide) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 Records|

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qhv/m/n/10 File

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/b/n/10 BioRemPP

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.69

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.04

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.02

Underfull \hbox (badness 10000) in paragraph at lines 358--358
[]\T1/qtm/m/n/10 0.18
[6] [7] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/t1txtt.fd)

! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.571 \sphinxstylestrong{pandas} (≥
                                     2.0.0): High\sphinxhyphen{}performance ...


! LaTeX Error: Unicode character ≥ (U+2265)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.575 \sphinxstylestrong{numpy} (≥
                                    1.21.0): Fundamental numerical computing...

[8]
Underfull \hbox (badness 10000) in paragraph at lines 802--802
[][][]\T1/txtt/m/n/10 input data/sample_data.

Underfull \hbox (badness 10000) in paragraph at lines 802--802
[]\T1/qtm/m/n/10 di-rec-
[9] [10] [11] [12]

! LaTeX Error: Unicode character 🎉 (U+1F389)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1102 🎉 Processing completed successfully!


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1103 ...ts: 1,247 total matches across databases


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1104    📁 Output Files Generated:


! LaTeX Error: Unicode character ⏱ (U+23F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1109    ⏱️  Processing Time: 4.2 seconds


! LaTeX Error: Unicode character 💾 (U+1F4BE)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1110    💾 Total Output Size: 524KB

[13] [14] (/usr/share/texlive/texmf-dist/tex/latex/txfonts/ts1txtt.fd) [15]
[16]

! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1435 ...h\PYGZhy{}level processing orchestration


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1440 ...GZsh{} Data validation and preprocessing


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1443 ...nd\PYGZhy{}line interface implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1446 ...\PYGZsh{} Command Pattern implementation


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1450 ...{} Application core and factory patterns


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1453 ... \PYGZsh{} Utility functions and helpers


! LaTeX Error: Unicode character 📁 (U+1F4C1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1457 ...       \PYGZsh{} Embedded database files

[17] [18] [19] [20] [21] [22]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1905 ...}not\PYG{+w}{ }found:\PYG{+w}{ }data.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1907 💡\PYG{+w}{ }Solutions:

[23]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1918 ...nput\PYG{+w}{ }format\PYG{+w}{ }detected


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1920 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1932 ...YG{k}{in}\PYG{+w}{ }input\PYG{+w}{ }file


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1934 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1948 ...}\PYGZhy{}\PYGZhy{}all\PYGZhy{}databases


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1950 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1960 ...1}{\PYGZsq{}invalid\PYGZus{}db\PYGZsq{}}


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1963 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1976 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1978 💡\PYG{+w}{ }Solutions:

[24]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1989 ...r}\PYG{+w}{ }output\PYG{+w}{ }generation


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.1991 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2005 ...}\PYG{+w}{ }dataset\PYG{+w}{ }processing


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2007 💡\PYG{+w}{ }Solutions:

[25] [26] [27] [28]

LaTeX Warning: Hyper reference `readme:LICENSE.txt' on page 29 undefined on inp
ut line 2409.


! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2465 \subsection{🔧 Solução de Problemas}


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2474 ...not\PYG{+w}{ }found:\PYG{+w}{ }dados.txt


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2476 💡\PYG{+w}{ }Solutions:

[29]

! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2489 ...Invalid\PYG{+w}{ }input\PYG{+w}{ }format


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2491 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character ❌ (U+274C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2504 ...or}\PYG{+w}{ }output\PYG{+w}{ }directory


! LaTeX Error: Unicode character 💡 (U+1F4A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2506 💡\PYG{+w}{ }Solutions:


! LaTeX Error: Unicode character 📧 (U+1F4E7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2529 📧
            \sphinxstylestrong{Email}: \sphinxhref{mailto:suporte@biorempp.o...


! LaTeX Error: Unicode character 🐛 (U+1F41B)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2533 🐛
            \sphinxstylestrong{Issues}: \sphinxhref{https://github.com/DougF...


! LaTeX Error: Unicode character 📖 (U+1F4D6)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2537 📖
            \sphinxstylestrong{Documentação}: \sphinxhref{https://biorempp...


! LaTeX Error: Unicode character 📄 (U+1F4C4)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2546 \subsection{📄 Licença}


LaTeX Warning: Hyper reference `readme:LICENSE' on page 30 undefined on input l
ine 2549.

[30]

! LaTeX Error: Unicode character 🙏 (U+1F64F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2556 \subsection{🙏 Agradecimentos}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2581 \subsection{📊 Estatísticas do Projeto}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2614 ...m insights para remediação ambiental.}


! LaTeX Error: Unicode character 🧬 (U+1F9EC)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2622 \subsection{🧬 About BioRemPP}


! LaTeX Error: Unicode character 🏗 (U+1F3D7)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2628 \subsection{🏗️ Architecture Overview}


! LaTeX Error: Unicode character 📱 (U+1F4F1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2634 ...lintitle{\sphinxupquote{biorempp.app}})}

[31]

! LaTeX Error: Unicode character 🔧 (U+1F527)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2651 ...ntitle{\sphinxupquote{biorempp.utils}})}


! LaTeX Error: Unicode character 💻 (U+1F4BB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2676 ...lintitle{\sphinxupquote{biorempp.cli}})}


! LaTeX Error: Unicode character ⚡ (U+26A1)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2689 ...tle{\sphinxupquote{biorempp.commands}})}


! LaTeX Error: Unicode character 📊 (U+1F4CA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2706 ...nxupquote{biorempp.input\_processing}})}


! LaTeX Error: Unicode character 🔬 (U+1F52C)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2723 ...le{\sphinxupquote{biorempp.pipelines}})}


! LaTeX Error: Unicode character 🚀 (U+1F680)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2736 \subsection{🚀 Key Features}

[32]

! LaTeX Error: Unicode character 📋 (U+1F4CB)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2819 \subsection{📋 Usage Examples}

[33]

! LaTeX Error: Unicode character 🛠 (U+1F6E0)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character ️ (U+FE0F)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2852 \subsection{🛠️ Development}


! LaTeX Error: Unicode character 📚 (U+1F4DA)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2897 \subsection{📚 Documentation}


! LaTeX Error: Unicode character 🔗 (U+1F517)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.2921 \subsection{🔗 Quick Links}


LaTeX Warning: Hyper reference `overview:api/modules.html' on page 34 undefined
 on input line 2925.


LaTeX Warning: Hyper reference `overview:DOCUMENTATION_GUIDE.html' on page 34 u
ndefined on input line 2929.


LaTeX Warning: Hyper reference `overview:contributing.html' on page 34 undefine
d on input line 2933.

[34] [35] [36] [37] [38] [39] [40] [41] [42] [43] [44] [45] [46] [47] [48]
[49] [50] [51] [52] [53] [54] [55] [56] [57] [58] [59] [60] [61] [62] [63]
[64] [65] [66] [67] [68] [69] [70] [71] [72] [73] [74] [75] [76]
Chapter 3.

LaTeX Warning: Hyper reference `index:api/modules.rst' on page 77 undefined on
input line 6463.

[77] [78]
Chapter 4.
(./biorempp.ind) [79] (./biorempp.aux)

LaTeX Warning: There were undefined references.

 )
(see the transcript file for additional information){/usr/share/texlive/texmf-d
ist/fonts/enc/dvips/base/8r.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/tex-gyre/q-ts1.enc}</usr/share/texlive/t
exmf-dist/fonts/type1/public/amsfonts/cm/cmmi5.pfb></usr/share/texlive/texmf-di
st/fonts/type1/public/amsfonts/cm/cmsy10.pfb></usr/share/texlive/texmf-dist/fon
ts/type1/public/amsfonts/cm/cmsy5.pfb></usr/share/texlive/texmf-dist/fonts/type
1/public/amsfonts/symbols/msam10.pfb></usr/share/texmf/fonts/type1/public/tex-g
yre/qhvb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qhvbi.pfb></usr/shar
e/texmf/fonts/type1/public/tex-gyre/qhvr.pfb></usr/share/texmf/fonts/type1/publ
ic/tex-gyre/qtmb.pfb></usr/share/texmf/fonts/type1/public/tex-gyre/qtmbi.pfb></
usr/share/texmf/fonts/type1/public/tex-gyre/qtmr.pfb></usr/share/texmf/fonts/ty
pe1/public/tex-gyre/qtmri.pfb></usr/share/texlive/texmf-dist/fonts/type1/public
/txfonts/t1xbtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t
1xtt.pfb></usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/t1xtt.pfb></
usr/share/texlive/texmf-dist/fonts/type1/public/txfonts/tcxtt.pfb></usr/share/t
exlive/texmf-dist/fonts/type1/urw/times/utmr8a.pfb>
Output written on biorempp.pdf (83 pages, 427752 bytes).
Transcript written on biorempp.log.
Latexmk: Index file 'biorempp.idx' was written
Latexmk: Log file says output to 'biorempp.pdf'
Collected error summary (may duplicate other messages):
  pdflatex: Command for 'pdflatex' gave return code 1
      Refer to 'biorempp.log' for details
Latexmk: Examining 'biorempp.log'
=== TeX engine is 'pdfTeX'
Latexmk: Errors, in force_mode: so I tried finishing targets
