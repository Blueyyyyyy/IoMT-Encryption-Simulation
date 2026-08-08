# Repository Configuration

This folder documents repository-level configuration files used by the Version 2 IoMT Encryption Simulation project.

## .gitignore

The `.gitignore` file is stored at the root of the repository and tells Git which local or temporary files should not be tracked or uploaded to GitHub.

The current `.gitignore` excludes several categories of files that are not required for reproducing the study:

### Python Cache Files

Python automatically creates temporary bytecode and cache files while scripts are running. These are excluded because they are generated automatically and are not part of the study source code.

Examples include:

- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.pyd`

### Python Virtual Environments

Local Python environments are excluded because they can contain large numbers of machine-specific package files. The required software packages are instead documented in the repository's `requirements.txt` file.

Examples include:

- `.venv/`
- `venv/`
- `env/`
- `ENV/`

### Python Tooling and Testing Caches

Temporary files created by Python development and testing tools are excluded because they are not required for the final study.

Examples include:

- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.coverage`
- `htmlcov/`

### Local Environment and Secret Files

Local `.env` files are excluded because they may contain machine-specific settings or sensitive configuration information.

The `.env.example` file is specifically allowed if one is ever added for documentation purposes.

### Jupyter Temporary Files

Jupyter Notebook checkpoint files are excluded because they are automatically generated temporary copies.

### IDE and Editor Files

Settings created by local development environments are excluded because they are specific to the user's computer and are not required for reproduction.

Examples include:

- `.vscode/`
- `.idea/`
- `*.swp`
- `*.swo`

### Operating-System Files

Files automatically created by Windows and macOS are excluded because they contain local system metadata rather than research data or source code.

Examples include:

- `.DS_Store`
- `Thumbs.db`
- `desktop.ini`

### Temporary and Backup Files

Temporary working files and editor backup files are excluded so that accidental or incomplete files are not committed to the repository.

Examples include:

- `*.tmp`
- `*.temp`
- `*.bak`
- `*~`

## Purpose

The `.gitignore` keeps the repository focused on the files required for the Version 2 study, including the Python scripts, source data, analysis outputs, SPSS files, and documentation.

It also reduces unnecessary files in GitHub and helps prevent local machine settings, temporary files, caches, or potentially sensitive environment files from being committed accidentally.
