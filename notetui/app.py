"""Main TUI application for note taking."""

from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, TextArea, Label, Static
from textual.reactive import reactive

from notetui.notes import NoteManager
from notetui.calendar import Calendar
from notetui.todolist import TodoList, TodoItem


class NoteTUI(App):
    """A keyboard-driven TUI for daily markdown notes."""

    CSS = """
    Screen {
        background: #0a0e14;
    }

    Header {
        background: #0d1117;
        color: #00ffff;
        text-style: bold;
        border: tall #00d4ff;
    }

    Header .header--title {
        color: #00ffff;
        text-style: bold;
    }

    Header .header--subtitle {
        color: #7b2cbf;
    }

    Header .header--clock {
        color: #ff00ff;
        background: #1a1f2e;
        text-style: bold;
    }

    Footer {
        background: #0d1117;
        color: #00d4ff;
    }

    Footer > .footer--highlight {
        background: #7b2cbf;
        color: #ffffff;
    }

    Footer > .footer--key {
        background: #1a1f2e;
        color: #00ffff;
    }

    #main-container {
        width: 100%;
        height: 100%;
        background: #0a0e14;
    }

    #split-container {
        width: 100%;
        height: 100%;
    }

    #split-container.hide {
        display: none;
    }

    #editor-container {
        width: 2fr;
        height: 100%;
    }

    #todo-container {
        width: 1fr;
        height: 100%;
    }

    #info-bar {
        width: 100%;
        height: 3;
        background: #1a1f2e;
        padding: 0 2;
        color: #00ffff;
        border: tall #00d4ff;
    }

    #calendar-container {
        width: 100%;
        height: 100%;
        display: none;
        background: #0a0e14;
    }

    #calendar-container.show {
        display: block;
    }

    TextArea {
        width: 100%;
        height: 1fr;
        background: #0d1117;
        color: #e0e0e0;
        border: tall #7b2cbf;
    }

    TextArea:focus {
        border: tall #00ffff;
    }

    #status-text {
        text-align: left;
        content-align: left middle;
        color: #00ffff;
        text-style: bold;
    }

    #file-path {
        text-align: right;
        content-align: right middle;
        color: #7b2cbf;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+s", "save", "Save", priority=True),
        Binding("ctrl+n", "next_day", "Next Day", priority=True),
        Binding("ctrl+p", "prev_day", "Prev Day", priority=True),
        Binding("ctrl+f", "next_week", "Next Week", priority=True),
        Binding("ctrl+b", "prev_week", "Prev Week", priority=True),
        Binding("ctrl+t", "today", "Today", priority=True),
        Binding("ctrl+c", "toggle_calendar", "Calendar", priority=True),
        Binding("ctrl+h", "show_help", "Help", priority=True),
        Binding("ctrl+enter", "finish_todo_on_line", "Finish Todo", show=False),
        Binding("tab", "focus_todos", "Focus Todos", show=False),
        Binding("escape", "escape", "Back", show=False),
    ]

    current_date: reactive[datetime] = reactive(datetime.now)
    show_calendar: reactive[bool] = reactive(False)

    def __init__(self, notes_dir: Path | None = None):
        """Initialize the NoteTUI app.

        Args:
            notes_dir: Directory to store notes. Defaults to ~/notes/
        """
        super().__init__()
        self.note_manager = NoteManager(notes_dir)
        self.editor: TextArea | None = None
        self.calendar_widget: Calendar | None = None
        self.todo_list: TodoList | None = None
        self._previous_date: datetime | None = None
        self.current_date = datetime.now()

    def compose(self) -> ComposeResult:
        """Compose the TUI layout."""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            with Horizontal(id="split-container"):
                with Vertical(id="editor-container"):
                    with Horizontal(id="info-bar"):
                        yield Label(self._get_status_text(), id="status-text")
                        yield Label(self._get_file_path(), id="file-path")
                    yield TextArea(
                        self.note_manager.get_note_content(self.current_date),
                        language="markdown",
                        theme="dracula",
                        show_line_numbers=True,
                    )

                with Container(id="todo-container"):
                    yield TodoList(self.note_manager.notes_dir)

            with Container(id="calendar-container"):
                yield Calendar(self.current_date)

        yield Footer()

    def on_mount(self) -> None:
        """Handle mount event."""
        self.title = "NoteTUI - Daily Notes"
        self.sub_title = "Press Ctrl+H for help"
        self.editor = self.query_one(TextArea)
        self.calendar_widget = self.query_one(Calendar)
        self.todo_list = self.query_one(TodoList)
        # Track the initial date
        self._previous_date = self.current_date
        # Move cursor to line 2 on startup
        if self.editor:
            self.editor.move_cursor((1, 0))
        # Scan for todos
        if self.todo_list:
            self.todo_list.scan_notes()

    def watch_current_date(self, new_date: datetime) -> None:
        """React to date changes."""
        if self.editor and self._previous_date:
            # Save to the PREVIOUS date before loading new content
            content = self.editor.text
            self.note_manager.save_note_content(self._previous_date, content)
            # Refresh todo list after saving
            if self.todo_list:
                self.todo_list.scan_notes()

        # Load the new date's content
        if self.editor:
            self.editor.text = self.note_manager.get_note_content(new_date)
            self._update_info_bar()
            # Move cursor to line 2 (index 1, column 0)
            self.editor.move_cursor((1, 0))

        # Remember this date for next time
        self._previous_date = new_date

    def watch_show_calendar(self, show: bool) -> None:
        """React to calendar visibility changes."""
        split_container = self.query_one("#split-container")
        calendar_container = self.query_one("#calendar-container")

        if show:
            split_container.add_class("hide")
            calendar_container.add_class("show")
            if self.calendar_widget:
                # Update calendar to current date and focus it
                self.calendar_widget.selected_date = self.current_date
                self.calendar_widget.display_date = self.current_date
                self.calendar_widget.refresh(recompose=True)
                self.calendar_widget.call_after_refresh(self.calendar_widget.focus_selected_date)
        else:
            calendar_container.remove_class("show")
            split_container.remove_class("hide")
            if self.editor:
                self.editor.focus()

    def _save_current_note(self) -> None:
        """Save the current note content to the current date."""
        if self.editor:
            content = self.editor.text
            self.note_manager.save_note_content(self.current_date, content)
            # Update the previous date tracker
            self._previous_date = self.current_date
            # Refresh todo list after saving
            if self.todo_list:
                self.todo_list.scan_notes()

    def _update_info_bar(self) -> None:
        """Update the information bar."""
        status_label = self.query_one("#status-text", Label)
        file_label = self.query_one("#file-path", Label)

        status_label.update(self._get_status_text())
        file_label.update(self._get_file_path())

    def _get_status_text(self) -> str:
        """Get the status text for the info bar."""
        day_name = self.current_date.strftime("%A")
        date_str = self.current_date.strftime("%d %b %Y")
        exists = "📝" if self.note_manager.note_exists(self.current_date) else "✨"
        return f"{exists} {day_name}, {date_str}"

    def _get_file_path(self) -> str:
        """Get the file path for display."""
        path = self.note_manager.get_note_path(self.current_date)
        return str(path)

    def action_save(self) -> None:
        """Save the current note."""
        self._save_current_note()
        self.notify("Note saved!", severity="information")

    def action_next_day(self) -> None:
        """Navigate to the next day."""
        self.current_date = self.note_manager.get_next_day(self.current_date)
        self.notify(f"→ {self.current_date.strftime('%d %b %Y')}")

    def action_prev_day(self) -> None:
        """Navigate to the previous day."""
        self.current_date = self.note_manager.get_previous_day(self.current_date)
        self.notify(f"← {self.current_date.strftime('%d %b %Y')}")

    def action_next_week(self) -> None:
        """Navigate to the next week."""
        self.current_date = self.note_manager.get_next_week(self.current_date)
        self.notify(f"⇒ {self.current_date.strftime('%d %b %Y')}")

    def action_prev_week(self) -> None:
        """Navigate to the previous week."""
        self.current_date = self.note_manager.get_previous_week(self.current_date)
        self.notify(f"⇐ {self.current_date.strftime('%d %b %Y')}")

    def action_today(self) -> None:
        """Navigate to today."""
        self.current_date = datetime.now()
        self.notify(f"Today: {self.current_date.strftime('%d %b %Y')}")

    def action_toggle_calendar(self) -> None:
        """Toggle calendar view."""
        self.show_calendar = not self.show_calendar

    def action_escape(self) -> None:
        """Handle escape key."""
        if self.show_calendar:
            self.show_calendar = False
        else:
            # Return focus to editor when pressing escape in todo list
            if self.editor:
                self.editor.focus()

    def action_focus_todos(self) -> None:
        """Focus the todo list."""
        if self.todo_list:
            # Try to focus the first todo item
            todo_items = list(self.todo_list.query("TodoItem").results())
            if todo_items:
                # Focus the first focusable todo item
                for item in todo_items:
                    if item.can_focus:
                        item.focus()
                        break

    def action_finish_todo_on_line(self) -> None:
        """Finish the todo on the current cursor line by adding strikethrough."""
        if not self.editor:
            return

        # Get current cursor position
        cursor_row, cursor_col = self.editor.cursor_location

        # Get all lines
        lines = self.editor.text.split('\n')

        # Check if cursor is within valid range
        if 0 <= cursor_row < len(lines):
            line = lines[cursor_row].strip()

            # Check if line is a ## heading
            if line.startswith('##') and not line.startswith('###'):
                # Extract the todo text
                todo_text = line[2:].strip().rstrip('#').strip()

                # Check if already finished (has strikethrough)
                if todo_text.startswith('~~') and todo_text.endswith('~~'):
                    self.notify("Todo already finished!", severity="warning")
                    return

                # Get the original line with indentation
                original_line = lines[cursor_row]
                indent = original_line[:len(original_line) - len(original_line.lstrip())]

                # Replace with strikethrough version
                lines[cursor_row] = f"{indent}## ~~{todo_text}~~"

                # Update editor text
                self.editor.text = '\n'.join(lines)

                # Save and refresh todos
                self._save_current_note()

                self.notify(f"✓ Finished: {todo_text}", severity="information")
            else:
                self.notify("Cursor is not on a ## todo line", severity="warning")

    def action_quit(self) -> None:
        """Quit the application after saving."""
        self._save_current_note()
        self.exit()

    def action_show_help(self) -> None:
        """Show help screen."""
        help_text = """
# NoteTUI - Keyboard Shortcuts

## Navigation
- **Ctrl+N**: Next day
- **Ctrl+P**: Previous day
- **Ctrl+F**: Next week (Forward)
- **Ctrl+B**: Previous week (Back)
- **Ctrl+T**: Go to today

## Editing
- **Ctrl+S**: Save current note

## Views
- **Ctrl+C**: Toggle calendar view
- **Escape**: Close calendar (when open)

## Other
- **Ctrl+H**: Show this help
- **Ctrl+Q**: Quit application

## In Calendar View
- **Arrow Keys**: Navigate between days
- **Enter**: Select focused date
- **[** / **]**: Previous/Next month
- Click to select a date

---
Notes are saved to: ~/notes/
Format: DD-MMM-YYYY.md (e.g., 21-Nov-2025.md)
"""
        self.notify(help_text, timeout=10, severity="information")

    def on_calendar_date_selected(self, message: Calendar.DateSelected) -> None:
        """Handle date selection from calendar."""
        self.current_date = message.date
        self.show_calendar = False
        self.notify(f"Selected: {message.date.strftime('%d %b %Y')}")

    def on_todo_item_selected(self, message: TodoItem.Selected) -> None:
        """Handle todo item selection - jump to that date."""
        # Parse the date string (format: "DD-MMM-YYYY")
        try:
            selected_date = datetime.strptime(message.date_str, "%d-%b-%Y")
            self.current_date = selected_date
            # Return focus to editor and position cursor on line 2
            if self.editor:
                self.editor.move_cursor((1, 0))
                self.editor.focus()
            self.notify(f"Jumped to: {selected_date.strftime('%d %b %Y')}")
        except ValueError:
            self.notify("Could not parse date", severity="error")

    def on_todo_list_todo_file_updated(self, message: TodoList.TodoFileUpdated) -> None:
        """Handle todo file update - reload editor if viewing that file."""
        # Check if the updated file is the current date's file
        current_file = self.note_manager.get_note_path(self.current_date)
        if message.file_path == current_file and self.editor:
            # Save cursor position
            cursor_pos = self.editor.cursor_location
            # Reload the file content
            self.editor.text = self.note_manager.get_note_content(self.current_date)
            # Restore cursor position
            self.editor.move_cursor(cursor_pos)


def main():
    """Entry point for the application."""
    app = NoteTUI()
    app.run()


if __name__ == "__main__":
    main()
