"""Note manager for handling daily markdown files."""

import locale
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Set Norwegian locale for date formatting
try:
    locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8')
except locale.Error:
    try:
        # Fallback to alternative Norwegian locale names
        locale.setlocale(locale.LC_TIME, 'no_NO.UTF-8')
    except locale.Error:
        # If Norwegian locale is not available, keep default
        pass


class NoteManager:
    """Manages daily note files in ~/notes/."""

    def __init__(self, notes_dir: Optional[Path] = None):
        """Initialize the note manager.

        Args:
            notes_dir: Directory to store notes. Defaults to ~/notes/
        """
        self.notes_dir = notes_dir or Path.home() / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def get_note_path(self, date: datetime) -> Path:
        """Get the file path for a given date.

        Args:
            date: The date for the note

        Returns:
            Path to the note file (e.g., ~/notes/21-Nov-2025.md)
        """
        filename = date.strftime("%d-%b-%Y.md")
        return self.notes_dir / filename

    def get_note_content(self, date: datetime) -> str:
        """Get the content of a note for a given date.

        Args:
            date: The date for the note

        Returns:
            Content of the note file, or empty string if it doesn't exist
        """
        note_path = self.get_note_path(date)
        if note_path.exists():
            return note_path.read_text()
        return self._create_default_content(date)

    def save_note_content(self, date: datetime, content: str) -> None:
        """Save content to a note file.

        Args:
            date: The date for the note
            content: Content to write to the file
        """
        note_path = self.get_note_path(date)
        note_path.write_text(content)

    def _create_default_content(self, date: datetime) -> str:
        """Create default content for a new note.

        Args:
            date: The date for the note

        Returns:
            Default markdown content with date header
        """
        day_name = date.strftime("%A")
        date_str = date.strftime("%d %B %Y")
        return f"# {day_name}, {date_str}\n\n"

    def get_next_day(self, date: datetime) -> datetime:
        """Get the next day from a given date.

        Args:
            date: Current date

        Returns:
            Next day
        """
        return date + timedelta(days=1)

    def get_previous_day(self, date: datetime) -> datetime:
        """Get the previous day from a given date.

        Args:
            date: Current date

        Returns:
            Previous day
        """
        return date - timedelta(days=1)

    def get_next_week(self, date: datetime) -> datetime:
        """Get the same day next week.

        Args:
            date: Current date

        Returns:
            Date one week later
        """
        return date + timedelta(weeks=1)

    def get_previous_week(self, date: datetime) -> datetime:
        """Get the same day previous week.

        Args:
            date: Current date

        Returns:
            Date one week earlier
        """
        return date - timedelta(weeks=1)

    def note_exists(self, date: datetime) -> bool:
        """Check if a note file exists for a given date.

        Args:
            date: The date to check

        Returns:
            True if note file exists, False otherwise
        """
        return self.get_note_path(date).exists()
