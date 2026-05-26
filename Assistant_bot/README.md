# Personal Assistant Bot

A command-line interface (CLI) application for managing contacts and notes with persistent JSON storage.

## Features

### Contacts Management
- Add new contacts with name, phone, email, address, and birthday
- View all contacts
- Search contacts by name, phone, or email
- Edit contact information
- Delete contacts
- Find contacts with birthdays in N days
- Phone and email validation

### Notes Management
- Add text notes with optional tags
- View all notes
- Search notes by text content
- Search notes by tags
- Sort notes by tags
- Edit notes
- Delete notes

## Project Structure

```
Assistant_bot/
├── main.py           # Entry point
├── assistant.py      # Main CLI interface
├── contacts.py       # Contact management module
├── notes.py          # Notes management module
├── data/             # Data storage directory (auto-created)
│   ├── contacts.json # Contacts storage
│   └── notes.json    # Notes storage
└── README.md         # This file
```

## Installation

1. Ensure Python 3.7+ is installed
2. No external dependencies required (uses only standard library)

## Usage

Run the application:
```bash
python main.py
```

The CLI will display a menu with options to:
- Manage contacts (add, view, search, edit, delete, check birthdays)
- Manage notes (add, view, search by text/tags, sort by tags, edit, delete)

## Data Storage

All data is stored in JSON format in the `data/` directory:
- `contacts.json` - Stores all contacts
- `notes.json` - Stores all notes with tags

Data persists between sessions automatically.

## Phone and Email Validation

- **Phone**: Must contain at least 10 digits (supports +, spaces, dashes, parentheses)
- **Email**: Standard email format validation (user@domain.com)

## Birthday Format

Birthdays should be entered in format: `DD.MM.YYYY` (e.g., 25.05.1990)

## Additional Features

- Tags support for notes (comma-separated)
- Birthday reminders (find contacts with birthdays in N days)
- Full text search in notes
- Tag-based search and sorting for notes
