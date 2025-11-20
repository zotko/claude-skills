#!/usr/bin/env python3
"""
Convert Python (.py) files to Jupyter notebooks (.ipynb).

Splits code into cells based on # %% markers.
Organizes all imports into the first cell.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


def extract_imports_and_code(code: str) -> Tuple[List[str], str]:
    """
    Extract import statements from code and return them separately.

    Returns:
        (imports, remaining_code)
    """
    lines = code.split('\n')
    imports = []
    other_lines = []

    for line in lines:
        stripped = line.strip()
        # Match import statements
        if stripped.startswith('import ') or stripped.startswith('from '):
            imports.append(line)
        else:
            other_lines.append(line)

    return imports, '\n'.join(other_lines)


def split_cells(code: str) -> List[str]:
    """
    Split code into cells based on # %% markers.

    Returns list of cell contents.
    """
    # Split by # %% marker (with optional whitespace and comments after)
    cells = re.split(r'^# %%.*$', code, flags=re.MULTILINE)

    # Remove empty cells and strip whitespace
    cells = [cell.strip() for cell in cells if cell.strip()]

    return cells


def create_notebook(cells: List[str]) -> dict:
    """
    Create Jupyter notebook structure from cell contents.

    Returns notebook JSON structure.
    """
    notebook_cells = []

    for cell_content in cells:
        notebook_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": cell_content.split('\n')
        })

    notebook = {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    return notebook


def convert_py_to_notebook(py_file: Path, output_file: Path = None) -> Path:
    """
    Convert a Python file to a Jupyter notebook.

    Args:
        py_file: Path to input .py file
        output_file: Path to output .ipynb file (optional, defaults to same name)

    Returns:
        Path to created notebook file
    """
    # Read Python file
    code = py_file.read_text()

    # Extract imports
    imports, remaining_code = extract_imports_and_code(code)

    # Split remaining code into cells
    cells = split_cells(remaining_code)

    # Prepend imports cell if there are any imports
    if imports:
        import_cell = '\n'.join(imports)
        cells.insert(0, import_cell)

    # Create notebook structure
    notebook = create_notebook(cells)

    # Determine output file path
    if output_file is None:
        output_file = py_file.with_suffix('.ipynb')

    # Write notebook
    with open(output_file, 'w') as f:
        json.dump(notebook, f, indent=2)

    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: py_to_notebook.py <input.py> [output.ipynb]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not input_file.exists():
        print(f"Error: File {input_file} not found")
        sys.exit(1)

    result = convert_py_to_notebook(input_file, output_file)
    print(f"✅ Created notebook: {result}")


if __name__ == "__main__":
    main()
