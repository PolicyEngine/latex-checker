"""Tests for Jupyter notebook dollar sign checking."""

import json
import pytest
from latex_checker.notebook_checker import (
    find_unescaped_dollars_in_notebook,
    fix_unescaped_dollars_in_notebook,
)


class TestNotebookChecker:
    """Test finding unescaped dollar signs in notebooks."""

    def test_finds_dollars_in_markdown_cells(self):
        """Should find dollar signs in markdown cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": ["The price is $25,000"],
                }
            ]
        }
        issues = find_unescaped_dollars_in_notebook(notebook)
        assert len(issues) == 1
        assert "$25,000" in issues[0]["context"]

    def test_ignores_code_cells(self):
        """Should not check code cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["price = $25000"],
                }
            ]
        }
        issues = find_unescaped_dollars_in_notebook(notebook)
        assert len(issues) == 0

    def test_finds_across_multiple_cells(self):
        """Should find issues across multiple markdown cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": ["Price $100"],
                },
                {
                    "cell_type": "code",
                    "source": ["# code with $200"],
                },
                {
                    "cell_type": "markdown",
                    "source": ["Another $300"],
                },
            ]
        }
        issues = find_unescaped_dollars_in_notebook(notebook)
        assert len(issues) == 2

    def test_multiline_cell_content(self):
        """Should handle multiline markdown cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": [
                        "Line 1 has $100\n",
                        "Line 2 has $200\n",
                    ],
                }
            ]
        }
        issues = find_unescaped_dollars_in_notebook(notebook)
        assert len(issues) == 2


class TestNotebookFixer:
    """Test fixing unescaped dollar signs in notebooks."""

    def test_fixes_markdown_cells(self):
        """Should escape dollar signs in markdown cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": ["The price is $25,000"],
                }
            ]
        }
        fixed = fix_unescaped_dollars_in_notebook(notebook)
        assert fixed["cells"][0]["source"][0] == "The price is \\$25,000"

    def test_preserves_code_cells(self):
        """Should not modify code cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["price = $25000"],
                }
            ]
        }
        fixed = fix_unescaped_dollars_in_notebook(notebook)
        assert fixed["cells"][0]["source"][0] == "price = $25000"

    def test_fixes_multiple_cells(self):
        """Should fix all markdown cells."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": ["Price $100"],
                },
                {
                    "cell_type": "markdown",
                    "source": ["Cost $200"],
                },
            ]
        }
        fixed = fix_unescaped_dollars_in_notebook(notebook)
        assert "\\$100" in fixed["cells"][0]["source"][0]
        assert "\\$200" in fixed["cells"][1]["source"][0]
