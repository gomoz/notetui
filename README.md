# NoteTUI

A keyboard-driven terminal application (TUI) for daily markdown notes.

## What is NoteTUI?

NoteTUI is a terminal-based note-taking application that lets you write daily notes in markdown format. Each day gets its own file, and you can easily navigate between days using keyboard shortcuts.

### Features

- **Daily notes** - Automatic filename based on date (`DD-Mmm-YYYY.md`)
- **Markdown editor** - Syntax highlighting and line numbering
- **Calendar view** - Visual navigation between dates
- **Todo list** - Collects all `##` headings from your notes
- **Keyboard-driven** - Fast navigation without mouse
- **Norwegian language** - Dates and weekdays in Norwegian
- **Auto-save** - Notes are saved automatically when navigating

## Installation

### Requirements

- Python 3.10 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### With uv (recommended)

```bash
# Install directly from GitHub
uv tool install git+https://github.com/gomoz/notetui.git

# Or clone and install locally
git clone https://github.com/gomoz/notetui.git
cd notetui
uv tool install -e .
```

### With pip

```bash
git clone https://github.com/gomoz/notetui.git
cd notetui
pip install .
```

## Usage

Start the application:

```bash
notetui
```

Notes are stored in `~/notes/`.

## Keyboard Shortcuts

### Navigation

| Key | Action |
|-----|--------|
| `Ctrl+N` | Next day |
| `Ctrl+P` | Previous day |
| `Ctrl+F` | Next week |
| `Ctrl+B` | Previous week |
| `Ctrl+T` | Go to today |

### Views

| Key | Action |
|-----|--------|
| `Ctrl+C` | Show/hide calendar |
| `Tab` | Focus todo list |
| `Escape` | Back to editor |

### Editing

| Key | Action |
|-----|--------|
| `Ctrl+S` | Save note |
| `Ctrl+D` | Mark todo as done (in todo list) |
| `Ctrl+Enter` | Mark todo on line as done (in editor) |

### Other

| Key | Action |
|-----|--------|
| `Ctrl+H` | Show help |
| `Ctrl+Q` | Quit |

### In calendar view

| Key | Action |
|-----|--------|
| Arrow keys | Navigate between days |
| `Enter` | Select date |
| `[` / `]` | Previous/next month |

## Todo Feature

All `##` headings in your notes are shown as todos in the side panel:

```markdown
# monday, 01 december 2025

## Buy groceries
Get milk and bread

## Call the doctor
```

- Press `Tab` to focus the todo list
- Press `Enter` to jump to the date for a todo
- Press `Ctrl+D` to mark a todo as done (adds ~~strikethrough~~)

## Technology

- [Textual](https://textual.textualize.io/) - Modern Python TUI framework
- Python 3.10+

## License

MIT License
