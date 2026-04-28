"""Check and fix LaTeX dollar sign issues in Jupyter notebooks."""

from typing import List, Dict
from latex_checker.markdown_checker import (
    find_unescaped_dollars,
    fix_unescaped_dollars,
)


def find_unescaped_dollars_in_notebook(notebook: Dict) -> List[Dict]:
    """
    Find unescaped dollar signs in Jupyter notebook markdown cells.

    Args:
        notebook: Parsed notebook dictionary

    Returns:
        List of issues with cell index, line number, and context
    """
    issues = []

    for cell_idx, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue

        # Combine source lines into single text
        source = cell.get("source", [])
        if isinstance(source, list):
            text = "".join(source)
        else:
            text = source

        # Find issues in this cell
        cell_issues = find_unescaped_dollars(text)

        # Add cell information
        for issue in cell_issues:
            issue["cell"] = cell_idx
            issues.append(issue)

    return issues


def fix_unescaped_dollars_in_notebook(notebook: Dict) -> Dict:
    """
    Fix unescaped dollar signs in Jupyter notebook markdown cells.

    Args:
        notebook: Parsed notebook dictionary

    Returns:
        Fixed notebook dictionary
    """
    import copy

    fixed_notebook = copy.deepcopy(notebook)

    for cell in fixed_notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue

        # Get source
        source = cell.get("source", [])
        if isinstance(source, list):
            text = "".join(source)
        else:
            text = source

        # Fix the text
        fixed_text = fix_unescaped_dollars(text)

        # Update source (preserve list format if it was a list)
        if isinstance(source, list):
            # Split back into list maintaining original line breaks
            cell["source"] = [fixed_text]
        else:
            cell["source"] = fixed_text

    return fixed_notebook
