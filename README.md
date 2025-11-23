# latex-checker

Check and fix LaTeX syntax issues in Markdown and Jupyter notebooks.

## Problem

When writing documents with currency values in MyST Markdown or Jupyter Book, dollar signs (`$`) trigger LaTeX math mode, causing rendering issues:

```markdown
Taxpayers earning $25,000 to $34,000...
```

Renders incorrectly as: 25,000(singlefilers)to34,000

## Solution

This tool automatically finds and escapes unescaped dollar signs in markdown and notebook files.

## Installation

```bash
pip install latex-checker
```

Or with uv:

```bash
uv pip install latex-checker
```

## Usage

### Check files

```bash
latex-checker path/to/files/
```

### Auto-fix files

```bash
latex-checker path/to/files/ --fix
```

### Check single file

```bash
latex-checker myfile.md
```

### Ignore notebooks

```bash
latex-checker path/to/files/ --ignore-notebooks
```

## Features

- ✅ Detects unescaped `$` before numbers (e.g., `$25,000`)
- ✅ Preserves already escaped dollar signs (`\$25,000`)
- ✅ Ignores dollar signs in code blocks and inline code
- ✅ Works with both Markdown (`.md`) and Jupyter notebooks (`.ipynb`)
- ✅ Batch processing of directories
- ✅ Auto-fix mode

## Development

Built using Test-Driven Development (TDD) with pytest.

### Setup

```bash
# Clone the repository
git clone https://github.com/PolicyEngine/latex-checker.git
cd latex-checker

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/ -v
```

### Run with coverage

```bash
pytest tests/ --cov=latex_checker --cov-report=html
```

## Related Issue

This tool was created in response to [mystmd#2477](https://github.com/jupyter-book/mystmd/issues/2477) - requesting configuration options to disable or restrict dollar sign math parsing in MyST CLI.

## License

MIT

## Author

Max Ghenis (max@policyengine.org)
