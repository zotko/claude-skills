---
name: notebook-reader
description: "Reads Jupyter notebooks (.ipynb) with options to filter by cell type (code/markdown only), exclude outputs, or read specific cell ranges."
---

# Notebook Reader

A skill for reading Jupyter notebooks (.ipynb) with minimal token usage by extracting only the relevant content.

## When to Use

Use this skill when you need to:
- Read a Jupyter notebook with reduced token usage
- View only code cells or only markdown cells
- Read notebook content without execution outputs
- Get a compact overview of notebook structure

## Usage

Run the notebook reader script:

```bash
python scripts/read_notebook.py <notebook_path> [options]
```

### Options

- `--code-only`: Show only code cells
- `--markdown-only`: Show only markdown cells
- `--no-outputs`: Exclude cell outputs (default: outputs included)
- `--cell-range START END`: Read only cells in range (0-indexed)
- `--summary`: Show notebook summary (cell counts, kernel info) without content

### Examples

Read entire notebook without outputs:
```bash
python scripts/read_notebook.py notebook.ipynb --no-outputs
```

Read only code cells:
```bash
python scripts/read_notebook.py notebook.ipynb --code-only --no-outputs
```

Get notebook summary:
```bash
python scripts/read_notebook.py notebook.ipynb --summary
```

Read specific cell range:
```bash
python scripts/read_notebook.py notebook.ipynb --cell-range 0 5
```

## Output Format

The script outputs cells in a readable format:

```
# Cell 1 [code]
import pandas as pd
df = pd.read_csv('data.csv')

# Cell 2 [markdown]
## Data Analysis
This notebook analyzes...

# Cell 3 [code]
df.head()

--- Output ---
   col1  col2
0     1     2
```
