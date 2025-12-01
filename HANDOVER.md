# NoteTUI - Project Handover Document

## Project Overview

**NoteTUI** is a keyboard-driven Terminal User Interface (TUI) for daily markdown note-taking, built with Python and the Textual framework.

### Core Concept
- **Daily notes**: One markdown file per day (format: `DD-MMM-YYYY.md`, e.g., `21-Nov-2025.md`)
- **Location**: `~/notes/` directory
- **Design**: Futuristic/cyberpunk aesthetic with neon cyan and purple colors
- **Navigation**: 100% keyboard-driven, no mouse required

---

## Features Implemented

### 1. Daily Note Management
- **Auto-creation**: Creates daily note files automatically with date heading
- **Navigation**:
  - `Ctrl+N` / `Ctrl+P` - Next/Previous day
  - `Ctrl+F` / `Ctrl+B` - Next/Previous week
  - `Ctrl+T` - Jump to today
- **Auto-save**: Press `Ctrl+S` to save current note
- **Smart cursor**: Always starts on line 2 (below date heading)

### 2. Calendar View
- **Toggle**: `Ctrl+C` to show/hide calendar
- **Navigation**: Arrow keys to move between dates
- **Month switching**: `[` and `]` for previous/next month
- **Selection**: `Enter` to jump to selected date
- **Auto-focus**: Highlights current date when opened

### 3. Split-Pane Todo List
- **Layout**: Editor (left, 2/3 width) + Todo list (right, 1/3 width)
- **Auto-scanning**: Finds all `##` headings across all notes
- **Real-time updates**: Updates when notes are saved or changed
- **Date tracking**: Shows which date each todo is from

### 4. Todo Management

#### Creating Todos
Write any line starting with `##` in your notes:
```markdown
##Buy groceries
## Call dentist
```

#### Completing Todos
**Two methods:**

1. **From Editor** (on the `##` line):
   - `Ctrl+Enter` → Adds strikethrough: `## ~~Task~~`

2. **From Todo List**:
   - `Tab` → Focus todo list
   - `↑/↓` → Navigate todos
   - `Ctrl+D` → Mark as done
   - `Enter` → Jump to that todo's date

#### Finished Todos
- Marked with strikethrough: `## ~~Completed task~~`
- Automatically hidden from todo list
- Preserved in notes for history

### 5. Keyboard Navigation

#### Editor ↔ Todo List
- `Tab` → Switch from editor to first todo
- `Escape` → Return to editor from todo list

#### Todo List Navigation
- `↑/↓` → Navigate between todos
- `Enter` → Jump to todo's date
- `Ctrl+D` → Mark todo as done
- Visual feedback: Purple background with cyan border when focused

### 6. Visual Design
- **Theme**: Cyberpunk/futuristic
- **Colors**:
  - Background: `#0a0e14` (dark)
  - Primary: `#00ffff` (neon cyan)
  - Accent: `#7b2cbf` (purple)
  - Highlight: `#ff00ff` (magenta)
- **Syntax highlighting**: Markdown with Dracula theme
- **Borders**: Heavy neon cyan borders for focused elements

---

## Technical Architecture

### Framework
**Textual** (Python TUI framework)
- Version: `>=0.86.0`
- Why chosen: Best text editing support, active maintenance, CSS-like styling

### Project Structure
```
notetui/
├── notetui/
│   ├── __init__.py
│   ├── app.py          # Main application & UI layout
│   ├── notes.py        # File management & date handling
│   ├── calendar.py     # Calendar widget
│   └── todolist.py     # Todo list widget & scanning
├── pyproject.toml      # Dependencies & entry point
├── run.sh             # Launch script
└── HANDOVER.md        # This document
```

### Key Files

#### `app.py` (Main Application)
- **Class**: `NoteTUI(App)`
- **Responsibilities**:
  - Overall layout (split pane, calendar overlay)
  - Keyboard bindings and actions
  - Date navigation logic
  - Coordination between components
  - Cursor positioning (always line 2)
- **Key reactive properties**:
  - `current_date` - Triggers note loading when changed
  - `show_calendar` - Controls calendar visibility

#### `notes.py` (File Manager)
- **Class**: `NoteManager`
- **Responsibilities**:
  - Creating/reading/writing note files
  - Date formatting (`DD-MMM-YYYY.md`)
  - Default content generation (date heading)
- **Key methods**:
  - `get_note_path(date)` - Returns `Path` for date
  - `get_note_content(date)` - Reads or creates note
  - `save_note_content(date, content)` - Saves note

#### `calendar.py` (Calendar Widget)
- **Class**: `Calendar(Container)`
- **Responsibilities**:
  - Rendering month view
  - Keyboard navigation (arrows, `[`, `]`)
  - Date selection
- **Messages**:
  - `DateSelected` - Sent when user presses Enter

#### `todolist.py` (Todo Widget)
- **Classes**:
  - `TodoItem(Static)` - Individual todo (focusable)
  - `TodoList(Container)` - Todo list container
- **Responsibilities**:
  - Scanning all `.md` files for `##` headings
  - Filtering out finished todos (`~~text~~`)
  - Marking todos complete (adding strikethrough)
  - Notifying app when files are updated
- **Messages**:
  - `TodoItem.Selected` - When Enter pressed on todo
  - `TodoList.TodoFileUpdated` - When todo marked complete

### Data Flow

#### Loading a Note
1. User navigates (e.g., `Ctrl+N`)
2. `current_date` reactive property changes
3. `watch_current_date()` triggered:
   - Saves previous note
   - Loads new note content
   - Updates editor text
   - Moves cursor to line 2
   - Refreshes todo list

#### Completing a Todo from Todo List
1. User presses `Ctrl+D` on focused todo
2. `TodoList.mark_todo_complete()`:
   - Updates file with strikethrough
   - Posts `TodoFileUpdated` message
   - Rescans todos
3. App receives `TodoFileUpdated`:
   - Reloads editor if viewing that file
   - Preserves cursor position
4. Todo disappears from list

#### Completing a Todo from Editor
1. User presses `Ctrl+Enter` on `##` line
2. `action_finish_todo_on_line()`:
   - Adds strikethrough to current line
   - Updates editor text
   - Calls `_save_current_note()`
3. Save triggers todo list refresh
4. Todo disappears from list

---

## Installation & Usage

### Requirements
- Python 3.10+
- `uv` (Python package manager) or `pip`

### Installation
```bash
cd /home/gomoz/Prosjekter/notetui
uv sync
# or: pip install -e .
```

### Running
```bash
# Using uv
uv run python -m notetui.app

# Or the convenience script
./run.sh

# Or if installed
notetui
```

### Notes Location
All notes are stored in: `~/notes/`

---

## Keyboard Shortcuts Reference

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Next day |
| `Ctrl+P` | Previous day |
| `Ctrl+F` | Next week (Forward) |
| `Ctrl+B` | Previous week (Back) |
| `Ctrl+T` | Jump to today |
| `Ctrl+C` | Toggle calendar |

### Editing
| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save current note |
| `Ctrl+Enter` | Finish todo on current line |
| `Ctrl+Q` | Quit (saves first) |
| `Ctrl+H` | Show help |

### Todo List
| Shortcut | Action |
|----------|--------|
| `Tab` | Focus first todo |
| `↑/↓` | Navigate todos |
| `Enter` | Jump to todo's date |
| `Ctrl+D` | Mark todo as done |
| `Escape` | Return to editor |

### Calendar
| Shortcut | Action |
|----------|--------|
| `Arrow keys` | Navigate dates |
| `[` / `]` | Previous/Next month |
| `Enter` | Select date |
| `Escape` | Close calendar |

---

## Important Implementation Details

### Date Switching Bug Fix
**Problem**: When switching dates, the wrong date was being saved.

**Solution**: Added `_previous_date` tracking:
- Before loading new date, save to `_previous_date`
- Only then update `current_date`
- This ensures we save to the OLD date before switching

### Editor Reload After Todo Completion
**Problem**: Completing todo from list → file updated → saving overwrites strikethrough.

**Solution**:
- `TodoList` posts `TodoFileUpdated` message when marking complete
- App listens for this message
- Reloads editor content if viewing that file
- Preserves cursor position during reload

### Tab Navigation Fix
**Problem**: Had to press Tab twice to focus todos.

**Solution**:
- Set `VerticalScroll(can_focus=False)` in TodoList
- Now Tab goes directly from editor to first TodoItem

### Cursor Positioning
**Always line 2** because line 1 has the date heading:
- On app startup: `editor.move_cursor((1, 0))`
- On date change: After loading content
- On todo jump: Before focusing editor

---

## Code Style & Patterns

### Reactive Properties
Textual's reactive properties auto-update UI:
```python
current_date: reactive[datetime] = reactive(datetime.now)

def watch_current_date(self, new_date: datetime) -> None:
    # Called automatically when current_date changes
    self.editor.text = self.note_manager.get_note_content(new_date)
```

### Message Passing
Widgets communicate via messages:
```python
class DateSelected(Message):
    def __init__(self, date: datetime) -> None:
        self.date = date
        super().__init__()

# Sender
self.post_message(self.DateSelected(selected_date))

# Receiver
def on_calendar_date_selected(self, message: Calendar.DateSelected) -> None:
    self.current_date = message.date
```

### CSS-in-Python
Styling uses Textual's CSS:
```python
CSS = """
TextArea {
    background: #0d1117;
    color: #e0e0e0;
    border: tall #7b2cbf;
}

TextArea:focus {
    border: heavy #00ffff;
}
"""
```

---

## Future Enhancements

### 1. Git-Based Sync (Recommended)
**Why**: Cross-device usage (Linux + macBook)

**Implementation Ideas**:
- Auto-commit on quit
- `Ctrl+G` to sync (pull + commit + push)
- Pull on startup
- Conflict detection & warnings

**Benefits**:
- Works offline
- Version history
- Handles conflicts well
- Free (GitHub/GitLab)

### 2. Search Functionality
- `Ctrl+/` to search across all notes
- Find text in current note
- Search by date range

### 3. Tags/Categories
- Support `#tag` syntax
- Filter todos by tag
- Tag-based navigation

### 4. Note Templates
- Different templates for different days
- Weekly review templates
- Meeting note templates

### 5. Export Options
- Export to PDF
- Generate weekly/monthly reports
- HTML export with styling

### 6. Advanced Todo Features
- Priority levels
- Due dates
- Recurring todos
- Checkboxes `- [ ]` support (in addition to `##`)

### 7. Performance Optimization
- Cache note content
- Lazy load todos (only scan when needed)
- Background scanning for large note collections

---

## Known Limitations

1. **No concurrent editing**: If you edit the same note on two devices simultaneously, last save wins (git sync would help)
2. **No undo/redo**: Textual's TextArea doesn't have built-in undo (could be added)
3. **No fuzzy search**: Currently no search functionality
4. **No attachments**: Plain text only (could support markdown image links)
5. **Fixed layout**: Split pane ratio is hardcoded (2fr:1fr)

---

## Troubleshooting

### Notes directory doesn't exist
App creates `~/notes/` automatically on first run.

### Ctrl+F not working in todo list
Changed to `Ctrl+D` because `Ctrl+F` is Next Week.

### Todo doesn't disappear after Ctrl+D
Make sure you're pressing `Ctrl+D` while the todo is focused (purple background).

### Calendar doesn't show
Press `Ctrl+C` to toggle. Make sure you're not in todo list when pressing it.

### Cursor in wrong position
Should always be on line 2. If not, there may be an issue with the move_cursor calls.

---

## Development Commands

```bash
# Run the app
uv run python -m notetui.app

# Install in development mode
pip install -e .

# Update dependencies
uv sync

# Run from package
python -m notetui.app
```

---

## File Format

### Note Structure
```markdown
# Friday, 21 November 2025

Your notes here...

##Todo item 1
##Todo item 2

More notes...

## ~~Completed todo~~
```

### Filename Format
- Pattern: `DD-MMM-YYYY.md`
- Examples:
  - `21-Nov-2025.md`
  - `01-Jan-2024.md`
  - `15-Dec-2025.md`

### Todo Format
- Active: `##Task name` or `## Task name`
- Completed: `## ~~Task name~~`
- The scanner strips leading/trailing `#` characters

---

## Contact & Continuation

This project was built from scratch in a single conversation session using:
- **Framework**: Textual (Python TUI)
- **Approach**: Test-driven development with rapid iteration
- **Design**: User-driven cyberpunk aesthetic

All features were implemented based on user feedback and testing.

### Session Summary
1. Started with basic daily note concept
2. Added calendar navigation
3. Implemented futuristic design
4. Added split-pane todo list
5. Fixed navigation and cursor positioning
6. Implemented dual todo completion methods
7. Fixed editor sync issues

**Total Development Time**: ~1 session
**Lines of Code**: ~800+ across 4 Python files
**Features**: 15+ major features implemented

---

## Version History

### v1.0 (Current)
- Daily note management with keyboard navigation
- Calendar view with date selection
- Split-pane layout with todo list
- Dual todo completion (editor + list)
- Futuristic cyberpunk design
- Auto-save and cursor positioning
- Real-time todo scanning

---

*Last Updated: 21 November 2025*
*Framework: Textual >= 0.86.0*
*Python: 3.10+*
