#!/usr/bin/env python3
"""Quick test script for note manager functionality."""

from datetime import datetime, timedelta
from pathlib import Path
from notetui.notes import NoteManager


def test_note_manager():
    """Test the note manager."""
    print("Testing NoteTUI NoteManager...")

    # Create a temporary test directory
    test_dir = Path.home() / "notes_test"
    nm = NoteManager(test_dir)

    # Test date
    test_date = datetime(2025, 11, 21)

    print(f"\n1. Test note path generation:")
    path = nm.get_note_path(test_date)
    print(f"   Path: {path}")
    print(f"   Expected: {test_dir}/21-Nov-2025.md")
    assert path == test_dir / "21-Nov-2025.md", "Path generation failed!"
    print("   ✓ Path generation works!")

    print(f"\n2. Test default content:")
    content = nm.get_note_content(test_date)
    print(f"   Content: {repr(content)}")
    assert "Friday" in content, "Default content missing day name!"
    assert "21 November 2025" in content, "Default content missing date!"
    print("   ✓ Default content works!")

    print(f"\n3. Test save and load:")
    test_content = "# Test Note\n\nThis is a test.\n"
    nm.save_note_content(test_date, test_content)
    loaded = nm.get_note_content(test_date)
    assert loaded == test_content, "Save/load mismatch!"
    print("   ✓ Save and load works!")

    print(f"\n4. Test navigation:")
    next_day = nm.get_next_day(test_date)
    print(f"   Next day: {next_day.strftime('%Y-%m-%d')}")
    assert next_day == test_date + timedelta(days=1), "Next day failed!"

    prev_day = nm.get_previous_day(test_date)
    print(f"   Prev day: {prev_day.strftime('%Y-%m-%d')}")
    assert prev_day == test_date - timedelta(days=1), "Previous day failed!"

    next_week = nm.get_next_week(test_date)
    print(f"   Next week: {next_week.strftime('%Y-%m-%d')}")
    assert next_week == test_date + timedelta(weeks=1), "Next week failed!"

    prev_week = nm.get_previous_week(test_date)
    print(f"   Prev week: {prev_week.strftime('%Y-%m-%d')}")
    assert prev_week == test_date - timedelta(weeks=1), "Previous week failed!"
    print("   ✓ Navigation works!")

    print(f"\n5. Test file existence check:")
    exists = nm.note_exists(test_date)
    print(f"   Note exists: {exists}")
    assert exists, "File should exist after saving!"
    print("   ✓ File existence check works!")

    # Cleanup
    print(f"\n6. Cleanup test directory...")
    if test_dir.exists():
        for file in test_dir.glob("*.md"):
            file.unlink()
        test_dir.rmdir()
    print("   ✓ Cleanup complete!")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_note_manager()
