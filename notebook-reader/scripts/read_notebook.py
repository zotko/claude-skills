#!/usr/bin/env python3
"""
Jupyter Notebook Reader - Efficiently read notebook content with minimal token usage.

Usage:
    python read_notebook.py <notebook_path> [options]

Options:
    --code-only       Show only code cells
    --markdown-only   Show only markdown cells
    --no-outputs      Exclude cell outputs
    --cell-range N M  Read only cells N to M (0-indexed, inclusive)
    --summary         Show notebook summary without content
"""

import argparse
import json
import sys
from pathlib import Path


def read_notebook(path: str) -> dict:
    """Read and parse a Jupyter notebook file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_cell_source(cell: dict) -> str:
    """Extract source content from a cell."""
    source = cell.get('source', [])
    if isinstance(source, list):
        return ''.join(source)
    return source


def get_cell_outputs(cell: dict) -> str:
    """Extract text outputs from a cell."""
    outputs = cell.get('outputs', [])
    if not outputs:
        return ''

    result = []
    for output in outputs:
        output_type = output.get('output_type', '')

        if output_type == 'stream':
            text = output.get('text', [])
            if isinstance(text, list):
                result.append(''.join(text))
            else:
                result.append(text)

        elif output_type in ('execute_result', 'display_data'):
            data = output.get('data', {})
            # Prefer plain text, skip images/html to save tokens
            if 'text/plain' in data:
                text = data['text/plain']
                if isinstance(text, list):
                    result.append(''.join(text))
                else:
                    result.append(text)

        elif output_type == 'error':
            ename = output.get('ename', 'Error')
            evalue = output.get('evalue', '')
            result.append(f"{ename}: {evalue}")

    return '\n'.join(result)


def format_cell(index: int, cell: dict, include_outputs: bool = True) -> str:
    """Format a single cell for display."""
    cell_type = cell.get('cell_type', 'unknown')
    source = get_cell_source(cell)

    if not source.strip():
        return ''

    lines = [f"# Cell {index + 1} [{cell_type}]", source]

    if include_outputs and cell_type == 'code':
        output = get_cell_outputs(cell)
        if output.strip():
            lines.append("\n--- Output ---")
            lines.append(output)

    return '\n'.join(lines)


def get_summary(notebook: dict) -> str:
    """Generate a summary of the notebook."""
    cells = notebook.get('cells', [])
    metadata = notebook.get('metadata', {})

    code_cells = sum(1 for c in cells if c.get('cell_type') == 'code')
    markdown_cells = sum(1 for c in cells if c.get('cell_type') == 'markdown')
    raw_cells = sum(1 for c in cells if c.get('cell_type') == 'raw')

    # Get kernel info
    kernel_info = metadata.get('kernelspec', {})
    kernel_name = kernel_info.get('display_name', kernel_info.get('name', 'Unknown'))

    # Get language
    lang_info = metadata.get('language_info', {})
    language = lang_info.get('name', 'Unknown')

    lines = [
        "# Notebook Summary",
        f"Total cells: {len(cells)}",
        f"  - Code cells: {code_cells}",
        f"  - Markdown cells: {markdown_cells}",
        f"  - Raw cells: {raw_cells}",
        f"Kernel: {kernel_name}",
        f"Language: {language}",
    ]

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Read Jupyter notebooks efficiently')
    parser.add_argument('notebook', help='Path to the notebook file')
    parser.add_argument('--code-only', action='store_true', help='Show only code cells')
    parser.add_argument('--markdown-only', action='store_true', help='Show only markdown cells')
    parser.add_argument('--no-outputs', action='store_true', help='Exclude cell outputs')
    parser.add_argument('--cell-range', nargs=2, type=int, metavar=('START', 'END'),
                        help='Read only cells in range (0-indexed, inclusive)')
    parser.add_argument('--summary', action='store_true', help='Show notebook summary only')

    args = parser.parse_args()

    path = Path(args.notebook)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    if not path.suffix == '.ipynb':
        print(f"Warning: File does not have .ipynb extension", file=sys.stderr)

    try:
        notebook = read_notebook(path)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid notebook format: {e}", file=sys.stderr)
        sys.exit(1)

    if args.summary:
        print(get_summary(notebook))
        return

    cells = notebook.get('cells', [])

    # Apply cell range filter
    if args.cell_range:
        start, end = args.cell_range
        cells = list(enumerate(cells))[start:end + 1]
        cells = [(i, c) for i, c in cells]
    else:
        cells = list(enumerate(cells))

    # Filter by cell type
    if args.code_only:
        cells = [(i, c) for i, c in cells if c.get('cell_type') == 'code']
    elif args.markdown_only:
        cells = [(i, c) for i, c in cells if c.get('cell_type') == 'markdown']

    # Format and print cells
    include_outputs = not args.no_outputs
    output_parts = []

    for index, cell in cells:
        formatted = format_cell(index, cell, include_outputs)
        if formatted:
            output_parts.append(formatted)

    print('\n\n'.join(output_parts))


if __name__ == '__main__':
    main()
