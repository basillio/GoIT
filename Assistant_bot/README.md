# Personal Assistant Bot

A modern application for managing contacts and notes with both CLI and GUI interfaces. Persistent JSON storage ensures data survives between sessions.

## Features

### Contacts Management
- Add new contacts with name, phone, phone 2, email, email 2, address, and birthday
- View all contacts with all contact fields
- Search contacts by name, phone, phone 2, email, or email 2
- Edit contact information (all fields)
- Delete contacts
- Find contacts with birthdays in N days
- Phone and email validation (both primary and secondary)

### Notes Management
- Add text notes with optional tags
- View all notes
- Search notes by text content
- Search notes by tags
- Sort notes by tags
- Edit notes
- Delete notes

### Interfaces
- **CLI Mode**: Command-line interface with menu system
- **GUI Mode**: Modern graphical interface with Tkinter
  - Tabbed interface (Contacts & Notes)
  - Data grid view with scrollbars
  - Real-time search filtering
  - Dialog forms for operations
  - Menu bar (File, Help)

## Project Structure

```
Assistant_bot/
├── main.py              # Entry point (mode selection)
├── assistant.py         # CLI interface
├── gui.py               # GUI interface (NEW)
├── gui_main.py          # GUI entry point (NEW)
├── contacts.py          # Contact management module
├── notes.py             # Notes management module
├── test_bot.py          # Test suite
├── config.json          # Configuration
├── data/                # Data storage directory (auto-created)
│   ├── contacts.json    # Contacts storage
│   └── notes.json       # Notes storage
└── README.md            # This file
```

## Installation

1. Ensure Python 3.7+ is installed
2. No external dependencies required (uses only standard library)
3. Tkinter is included with Python

## Usage

### Launch Application

**Option 1: Main Menu (Choose CLI or GUI)**
```bash
python main.py
```
Then select:
- Option 1 for CLI mode
- Option 2 for GUI mode

**Option 2: Direct GUI Launch**
```bash
python gui_main.py
```

### CLI Mode

The CLI displays a menu with options to:
- Manage contacts (add, view, search, edit, delete, check birthdays)
- Manage notes (add, view, search by text/tags, sort by tags, edit, delete)

### GUI Mode

The GUI provides:
- **Contacts Tab**: View, search, add, edit, delete contacts; check birthdays
- **Notes Tab**: View, search, filter by tags, add, edit, delete notes
- Real-time search filtering
- Dialog forms for all operations
- Menu bar with File and Help options

## Data Storage

All data is stored in JSON format in the `data/` directory:
- `contacts.json` - Stores all contacts
- `notes.json` - Stores all notes with tags

Data persists between sessions automatically.

## Phone and Email Validation

- **Phone**: Must contain at least 10 digits (supports +, spaces, dashes, parentheses)
- **Phone 2**: Optional secondary phone with same validation rules
- **Email**: Standard email format validation (user@domain.com)
- **Email 2**: Optional secondary email with same validation rules

## Birthday Format

Birthdays should be entered in format: `DD.MM.YYYY` (e.g., 25.05.1990)

## Additional Features

- Dual phone and email fields for each contact (primary and secondary)
- Tags support for notes (comma-separated)
- Birthday reminders (find contacts with birthdays in N days)
- Full text search in notes
- Tag-based search and sorting for notes
- Real-time filtering (GUI mode)
- Data grid view (GUI mode)
- Search across all contact fields (name, both phones, both emails)

## Documentation

- **GUI_README.md** - Complete GUI usage guide
- **QUICKSTART.md** - Quick start guide for both modes
- **DEVELOPER_GUIDE.md** - Technical architecture and extending
- **GUI_SUMMARY.md** - GUI feature summary
