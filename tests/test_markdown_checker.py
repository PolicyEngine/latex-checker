"""Tests for markdown dollar sign checking."""

import pytest
from latex_checker.markdown_checker import (
    find_unescaped_dollars,
    fix_unescaped_dollars,
)


class TestFindUnescapedDollars:
    """Test finding unescaped dollar signs in markdown."""

    def test_finds_simple_currency(self):
        """Should find dollar signs before numbers."""
        text = "The price is $25,000"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 1
        assert issues[0]["line"] == 1
        assert "$25,000" in issues[0]["context"]

    def test_finds_multiple_currencies(self):
        """Should find multiple dollar signs in one line."""
        text = "Range from $0 to $200,000 in $500 increments"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 3

    def test_ignores_escaped_dollars(self):
        """Should not flag already escaped dollar signs."""
        text = "The price is \\$25,000"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 0

    def test_ignores_inline_code(self):
        """Should not flag dollar signs in inline code."""
        text = "Use `$25,000` in your code"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 0

    def test_ignores_code_blocks(self):
        """Should not flag dollar signs in code blocks."""
        text = "```python\nprice = $25000\n```"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 0

    def test_ignores_indented_code(self):
        """Should not flag dollar signs in indented code blocks."""
        text = "    price = $25000"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 0

    def test_finds_comma_separated_amounts(self):
        """Should find dollar signs before comma-separated numbers."""
        text = "The total is $1,234,567"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 1

    def test_multiline_text(self):
        """Should find issues across multiple lines."""
        text = "Line 1 has $100\nLine 2 has $200\nLine 3 has $300"
        issues = find_unescaped_dollars(text)
        assert len(issues) == 3
        assert issues[0]["line"] == 1
        assert issues[1]["line"] == 2
        assert issues[2]["line"] == 3


class TestFixUnescapedDollars:
    """Test fixing unescaped dollar signs in markdown."""

    def test_fixes_simple_currency(self):
        """Should escape dollar signs before numbers."""
        text = "The price is $25,000"
        fixed = fix_unescaped_dollars(text)
        assert fixed == "The price is \\$25,000"

    def test_fixes_multiple_currencies(self):
        """Should escape all unescaped dollar signs."""
        text = "Range from $0 to $200,000"
        fixed = fix_unescaped_dollars(text)
        assert fixed == "Range from \\$0 to \\$200,000"

    def test_preserves_escaped_dollars(self):
        """Should not double-escape already escaped dollars."""
        text = "Already escaped \\$25,000"
        fixed = fix_unescaped_dollars(text)
        assert fixed == "Already escaped \\$25,000"

    def test_preserves_inline_code(self):
        """Should not modify inline code."""
        text = "Use `$25,000` in code"
        fixed = fix_unescaped_dollars(text)
        assert fixed == "Use `$25,000` in code"

    def test_preserves_code_blocks(self):
        """Should not modify code blocks."""
        text = "```\nprice = $25000\n```"
        fixed = fix_unescaped_dollars(text)
        assert "```\nprice = $25000\n```" in fixed

    def test_mixed_content(self):
        """Should fix text but preserve code."""
        text = "Price $100 in text but `$100` in code"
        fixed = fix_unescaped_dollars(text)
        assert "\\$100 in text" in fixed
        assert "`$100` in code" in fixed
