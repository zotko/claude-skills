---
name: py-to-notebook
description: Convert Python (.py) files to Jupyter notebooks (.ipynb) with automatic import organization and cell splitting. Use when users request converting Python files to notebooks, creating .ipynb from .py files, or turning Python scripts into Jupyter format. Handles single or multiple files.
---

# Python to Jupyter Notebook Converter

## Overview

Convert Python files to Jupyter notebooks using the `# %%` cell marker convention. All imports are automatically organized into the first cell.

## Quick Start

Use the conversion script for any Python-to-notebook conversion:

```bash
python scripts/py_to_notebook.py input.py [output.ipynb]
```

Example workflow:
1. User provides a Python file or asks to convert one
2. Run the script: `python scripts/py_to_notebook.py script.py`
3. Returns a `.ipynb` file with the same name

## Conversion Behavior

### Cell Splitting

Code is split into cells based on `# %%` markers:

```python
# First cell (imports automatically moved here)
import numpy as np
from pathlib import Path

# %%
# Second cell
def process_data(x):
    return x * 2

# %%
# Third cell
result = process_data(10)
print(result)
```

If no `# %%` markers are present, all code goes into one cell (after imports).

### Import Organization

All `import` and `from ... import` statements are automatically extracted and placed in the first cell, regardless of where they appear in the original Python file.

### Code Cells Only

All content remains in code cells. Docstrings and comments stay as Python code (not converted to markdown cells).

## Handling Multiple Files

For multiple files:
- Run the script once per file
- Each creates a separate notebook
- Or ask the user if they want files combined into one notebook (requires manual merging)

## Common Examples

**Single file conversion:**
```
User: "Convert script.py to a Jupyter notebook"
→ Run: python scripts/py_to_notebook.py script.py
```

**Specify output name:**
```
User: "Turn analysis.py into notebook.ipynb"
→ Run: python scripts/py_to_notebook.py analysis.py notebook.ipynb
```

**Multiple files:**
```
User: "Convert file1.py and file2.py to notebooks"
→ Run: python scripts/py_to_notebook.py file1.py
→ Run: python scripts/py_to_notebook.py file2.py
```
