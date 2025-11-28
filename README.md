# Claude Skills Collection

Custom skills for Claude Code that extend its capabilities with specialized workflows and tools.

## Available Skills

### notebook-reader

Read Jupyter notebooks efficiently with options to filter by cell type and exclude outputs to minimize token usage.

**Features:**
- Read only code cells or markdown cells
- Exclude outputs to reduce token usage
- Read specific cell ranges
- Get notebook summary without full content
- Pure Python standard library - no external dependencies

**Usage:**

```bash
python scripts/read_notebook.py <notebook.ipynb> [options]
```

Options:
- `--code-only` - Show only code cells
- `--markdown-only` - Show only markdown cells
- `--no-outputs` - Exclude cell outputs
- `--cell-range N M` - Read cells N to M (0-indexed)
- `--summary` - Show notebook summary only

Examples:
```bash
# Get notebook overview
python scripts/read_notebook.py notebook.ipynb --summary

# Read code cells without outputs (minimal tokens)
python scripts/read_notebook.py notebook.ipynb --code-only --no-outputs

# Read first 5 cells
python scripts/read_notebook.py notebook.ipynb --cell-range 0 4
```

## Installation

Add this repository as a plugin in Claude Code:

```
https://github.com/zotko/claude-skills
```

## Repository Structure

```
claude-skills/
├── README.md
├── .claude-plugin/
│   └── marketplace.json
└── notebook-reader/
    ├── SKILL.md
    └── scripts/
        └── read_notebook.py
```

## Creating Your Own Skills

Each skill contains:

- **SKILL.md** - Skill definition with YAML frontmatter (name, description) and instructions
- **scripts/** - Executable code for deterministic operations
- **references/** - Documentation loaded into context as needed
- **assets/** - Files used in outputs (templates, images, etc.)

## License

MIT
