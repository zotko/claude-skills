# Claude Skills Collection

Custom skills for Claude Code that extend its capabilities with specialized workflows and tools.

## Available Skills

### py-to-notebook

Convert Python files to Jupyter notebooks with automatic import organization and cell splitting.

**Features:**
- Splits code into cells using `# %%` markers
- Automatically organizes all imports into the first cell
- Pure Python standard library - no external dependencies
- Handles single or multiple file conversions

**Installation:**

```bash
# Download and install the skill
curl -L https://github.com/zotko/claude-skills/raw/main/py-to-notebook.skill -o ~/.claude/skills/py-to-notebook.skill
```

Or manually:
1. Download [py-to-notebook.skill](py-to-notebook.skill)
2. Copy to `~/.claude/skills/`
3. Restart Claude Code

**Usage:**

Simply ask Claude to convert Python files:
- "Convert script.py to a Jupyter notebook"
- "Turn my analysis.py into a .ipynb file"
- "Make a notebook from this Python file"

## Repository Structure

```
claude-skills/
├── README.md                    # This file
├── py-to-notebook/              # Skill source files
│   ├── SKILL.md                 # Skill definition and instructions
│   └── scripts/
│       └── py_to_notebook.py    # Conversion script
└── py-to-notebook.skill         # Packaged skill (ready to install)
```

## Creating Your Own Skills

This repository follows the official Claude Code skill structure. Each skill contains:

- **SKILL.md**: Defines the skill with YAML frontmatter (name, description) and markdown instructions
- **scripts/**: Executable code for deterministic operations
- **references/**: Documentation loaded into context as needed
- **assets/**: Files used in outputs (templates, images, etc.)

Skills are packaged into `.skill` files (ZIP archives) for distribution.

## Contributing

Feel free to submit issues or pull requests to improve existing skills or add new ones.

## License

MIT
