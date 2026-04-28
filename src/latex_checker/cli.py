"""Command-line interface for latex-checker."""

import argparse
import json
import sys
from pathlib import Path
from typing import List

import nbformat

from latex_checker.markdown_checker import (
    find_unescaped_dollars,
    fix_unescaped_dollars,
)
from latex_checker.notebook_checker import (
    find_unescaped_dollars_in_notebook,
    fix_unescaped_dollars_in_notebook,
)


def check_file(file_path: Path) -> List:
    """Check a single file for issues."""
    if file_path.suffix == ".ipynb":
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)
        issues = find_unescaped_dollars_in_notebook(notebook)
        for issue in issues:
            issue["file"] = str(file_path)
        return issues
    else:  # Markdown file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        issues = find_unescaped_dollars(text)
        for issue in issues:
            issue["file"] = str(file_path)
        return issues


def fix_file(file_path: Path) -> int:
    """Fix a single file. Returns number of fixes made."""
    if file_path.suffix == ".ipynb":
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        issues_before = len(find_unescaped_dollars_in_notebook(notebook))
        fixed_notebook = fix_unescaped_dollars_in_notebook(notebook)

        if issues_before > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(fixed_notebook, f, indent=1, ensure_ascii=False)

        return issues_before
    else:  # Markdown file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        issues_before = len(find_unescaped_dollars(text))
        fixed_text = fix_unescaped_dollars(text)

        if issues_before > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_text)

        return issues_before


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Check and fix LaTeX dollar sign issues in Markdown and Jupyter notebooks"
    )
    parser.add_argument("path", type=Path, help="File or directory to check")
    parser.add_argument(
        "--fix", action="store_true", help="Automatically fix issues"
    )
    parser.add_argument(
        "--ignore-notebooks", action="store_true", help="Skip .ipynb files"
    )

    args = parser.parse_args()

    # Collect files to check
    if args.path.is_file():
        files = [args.path]
    elif args.path.is_dir():
        patterns = ["**/*.md"]
        if not args.ignore_notebooks:
            patterns.append("**/*.ipynb")

        files = []
        for pattern in patterns:
            files.extend(args.path.glob(pattern))
    else:
        print(f"Error: {args.path} is not a valid file or directory")
        sys.exit(1)

    # Filter out build directories
    files = [
        f for f in files if "_build" not in str(f) and ".venv" not in str(f)
    ]

    total_issues = 0
    total_fixes = 0

    # Process files
    for file_path in files:
        if args.fix:
            fixes = fix_file(file_path)
            if fixes > 0:
                print(f"✓ Fixed {fixes} issue(s) in {file_path}")
                total_fixes += fixes
        else:
            issues = check_file(file_path)
            if issues:
                print(f"\n{'=' * 80}")
                print(f"File: {file_path}")
                print(f"Found {len(issues)} issue(s)")
                print("=" * 80)

                for issue in issues[:5]:  # Show first 5
                    print(f"\nLine {issue['line']}, Column {issue['column']}:")
                    print(f"  Context: ...{issue['context']}...")
                    print(f"  Suggestion: Replace $ with \\$")

                if len(issues) > 5:
                    print(f"\n... and {len(issues) - 5} more issue(s)")

                total_issues += len(issues)

    # Print summary
    print(f"\n{'=' * 80}")

    if args.fix:
        print(f"Total files processed: {len(files)}")
        print(f"Total fixes made: {total_fixes}")
        if total_fixes > 0:
            print("✓ All dollar signs have been escaped!")
        else:
            print("✓ No issues found!")
    else:
        print(f"Total files checked: {len(files)}")
        print(f"Total issues found: {total_issues}")
        if total_issues > 0:
            print("\nRun with --fix to automatically escape dollar signs")
            sys.exit(1)
        else:
            print("\n✓ No unescaped dollar signs found!")

    print("=" * 80)
    sys.exit(0)


if __name__ == "__main__":
    main()
