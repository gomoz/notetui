"""Calendar widget for date selection."""

import calendar
import locale
from datetime import datetime, date
from textual.app import ComposeResult
from textual.containers import Container, Grid
from textual.widget import Widget
from textual.widgets import Button, Label, Static
from textual.reactive import reactive
from textual.message import Message
from textual import events

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


class Calendar(Container):
    """A calendar widget for selecting dates."""

    DEFAULT_CSS = """
    Calendar {
        width: 100%;
        height: auto;
        background: #0a0e14;
        border: heavy #00ffff;
        padding: 1;
    }

    Calendar #month-year {
        text-align: center;
        width: 100%;
        color: #00ffff;
        text-style: bold;
        background: #1a1f2e;
        border: tall #7b2cbf;
        padding: 1;
    }

    Calendar .calendar-grid {
        grid-size: 7 8;
        grid-gutter: 1;
        width: 100%;
        height: auto;
        padding: 1;
        background: #0d1117;
    }

    Calendar .day-header {
        text-align: center;
        color: #7b2cbf;
        text-style: bold;
        background: #1a1f2e;
    }

    Calendar .day-button {
        width: 100%;
        height: 3;
        min-width: 0;
        border: round #1a1f2e;
        background: #0d1117;
        color: #00d4ff;
    }

    Calendar .day-button:hover {
        background: #1a1f2e;
        color: #00ffff;
        border: round #00d4ff;
    }

    Calendar .day-button:focus {
        background: #7b2cbf;
        color: #ffffff;
        text-style: bold;
        border: heavy #ff00ff;
    }

    Calendar .day-button.today {
        background: #00d4ff;
        color: #0a0e14;
        text-style: bold;
        border: round #00ffff;
    }

    Calendar .day-button.selected {
        background: #00ffff;
        color: #0a0e14;
        text-style: bold;
        border: heavy #00d4ff;
    }

    Calendar .day-button.empty {
        background: transparent;
        border: none;
    }
    """

    selected_date: reactive[datetime] = reactive(datetime.now)
    can_focus = True

    class DateSelected(Message):
        """Message sent when a date is selected."""

        def __init__(self, selected_date: datetime) -> None:
            self.date = selected_date
            super().__init__()

    def __init__(self, initial_date: datetime | None = None, **kwargs) -> None:
        """Initialize the calendar.

        Args:
            initial_date: Initial date to display. Defaults to today.
        """
        super().__init__(**kwargs)
        self.selected_date = initial_date or datetime.now()
        self.display_date = self.selected_date
        self._day_buttons = []  # Store button references

    def compose(self) -> ComposeResult:
        """Compose the calendar widget."""
        yield Label(
            self.display_date.strftime("%B %Y"),
            id="month-year",
        )
        with Grid(classes="calendar-grid"):
            # Day headers
            for day in ["Ma", "Ti", "On", "To", "Fr", "Lø", "Sø"]:
                yield Static(day, classes="day-header")

            # Calendar days
            cal = calendar.monthcalendar(
                self.display_date.year, self.display_date.month
            )
            today = date.today()

            for week in cal:
                for day in week:
                    if day == 0:
                        yield Button("", classes="day-button empty", disabled=True)
                    else:
                        day_date = date(
                            self.display_date.year, self.display_date.month, day
                        )
                        classes = "day-button"

                        if day_date == today:
                            classes += " today"
                        if day_date == self.selected_date.date():
                            classes += " selected"

                        yield Button(
                            str(day),
                            classes=classes,
                            id=f"day-{day}",
                        )

    def on_mount(self) -> None:
        """Focus the selected day when mounted."""
        selected_day = self.selected_date.day
        try:
            button = self.query_one(f"#day-{selected_day}", Button)
            button.focus()
        except:
            # If selected day doesn't exist in this month, focus first available day
            buttons = self.query(".day-button").results()
            for btn in buttons:
                if not btn.disabled:
                    btn.focus()
                    break

    def on_button_press(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id and event.button.id.startswith("day-"):
            day = int(event.button.id.split("-")[1])
            selected = datetime(
                self.display_date.year,
                self.display_date.month,
                day,
                self.selected_date.hour,
                self.selected_date.minute,
            )
            self.selected_date = selected
            self.post_message(self.DateSelected(selected))

    def _key_left(self) -> None:
        """Move focus to previous day."""
        self.screen.focus_previous()

    def _key_right(self) -> None:
        """Move focus to next day."""
        self.screen.focus_next()

    def _key_up(self) -> None:
        """Move focus up one week."""
        focused = self.screen.focused
        if focused and isinstance(focused, Button):
            buttons = [b for b in self.query(".day-button").results() if not b.disabled]
            try:
                idx = buttons.index(focused)
                new_idx = max(0, idx - 7)
                buttons[new_idx].focus()
            except (ValueError, IndexError):
                pass

    def _key_down(self) -> None:
        """Move focus down one week."""
        focused = self.screen.focused
        if focused and isinstance(focused, Button):
            buttons = [b for b in self.query(".day-button").results() if not b.disabled]
            try:
                idx = buttons.index(focused)
                new_idx = min(len(buttons) - 1, idx + 7)
                buttons[new_idx].focus()
            except (ValueError, IndexError):
                pass

    def _key_enter(self) -> None:
        """Select the focused day."""
        focused = self.screen.focused
        if focused and isinstance(focused, Button):
            if focused.id and focused.id.startswith("day-"):
                day = int(focused.id.split("-")[1])
                selected = datetime(
                    self.display_date.year,
                    self.display_date.month,
                    day,
                    self.selected_date.hour,
                    self.selected_date.minute,
                )
                self.selected_date = selected
                self.post_message(self.DateSelected(selected))

    def _key_right_square_bracket(self) -> None:
        """Move to next month with ]."""
        self.next_month()

    def _key_left_square_bracket(self) -> None:
        """Move to previous month with [."""
        self.previous_month()

    def next_month(self) -> None:
        """Move to the next month."""
        month = self.display_date.month
        year = self.display_date.year

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        self.display_date = datetime(year, month, 1)
        self.refresh(recompose=True)
        # Focus first day of new month
        self.call_after_refresh(self._focus_first_day)

    def previous_month(self) -> None:
        """Move to the previous month."""
        month = self.display_date.month
        year = self.display_date.year

        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

        self.display_date = datetime(year, month, 1)
        self.refresh(recompose=True)
        # Focus first day of new month
        self.call_after_refresh(self._focus_first_day)

    def _focus_first_day(self) -> None:
        """Focus the first available day button."""
        buttons = self.query(".day-button").results()
        for btn in buttons:
            if not btn.disabled:
                btn.focus()
                break

    def focus_selected_date(self) -> None:
        """Focus on the currently selected date."""
        selected_day = self.selected_date.day
        try:
            button = self.query_one(f"#day-{selected_day}", Button)
            button.focus()
        except:
            # If selected day doesn't exist in this month, focus first available day
            self._focus_first_day()
