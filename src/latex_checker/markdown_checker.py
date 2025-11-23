"""Check and fix LaTeX dollar sign issues in Markdown files."""

import re
from typing import List, Dict


def find_unescaped_dollars(text: str) -> List[Dict]:
    """
    Find unescaped dollar signs in markdown text.

    Args:
        text: Markdown text to check

    Returns:
        List of issues with line number and context
    """
    issues = []
    lines = text.split('\n')
    in_code_block = False

    for line_num, line in enumerate(lines, 1):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks or indented code
        if in_code_block or line.startswith('    ') or line.startswith('\t'):
            continue

        # Remove inline code sections to avoid false positives
        cleaned_line = re.sub(r'`[^`]*`', '', line)

        # Find unescaped dollar signs before numbers or commas
        # Pattern: $ not preceded by backslash, followed by digit or comma+digit
        pattern = r'(?<!\\)\$(?=\d|,\d)'
        matches = list(re.finditer(pattern, cleaned_line))

        for match in matches:
            col = match.start() + 1
            start = max(0, match.start() - 20)
            end = min(len(line), match.end() + 30)
            context = line[start:end]

            issues.append({
                'line': line_num,
                'column': col,
                'context': context,
            })

    return issues


def fix_unescaped_dollars(text: str) -> str:
    """
    Fix unescaped dollar signs in markdown text.

    Args:
        text: Markdown text to fix

    Returns:
        Fixed markdown text with escaped dollar signs
    """
    lines = text.split('\n')
    fixed_lines = []
    in_code_block = False

    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue

        # Skip indented code blocks and lines inside code blocks
        if in_code_block or line.startswith('    ') or line.startswith('\t'):
            fixed_lines.append(line)
            continue

        # Protect inline code sections
        code_sections = []
        def save_code(match):
            code_sections.append(match.group(0))
            return f"__CODE_PLACEHOLDER_{len(code_sections)-1}__"

        line = re.sub(r'`[^`]*`', save_code, line)

        # Replace unescaped dollar signs
        line = re.sub(r'(?<!\\)\$(?=\d|,\d)', r'\\$', line)

        # Restore inline code sections
        for i, code in enumerate(code_sections):
            line = line.replace(f"__CODE_PLACEHOLDER_{i}__", code)

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)
