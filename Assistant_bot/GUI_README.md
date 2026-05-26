# GUI Mode - Personal Assistant Bot

## Overview

The Personal Assistant Bot now includes a modern graphical user interface (GUI) built with Tkinter. This provides an alternative to the command-line interface with a more intuitive, visual experience.

## Features

### GUI Interface
- **Tabbed Interface**: Separate tabs for Contacts and Notes management
- **Data Grid View**: Display contacts and notes in organized table format
- **Real-time Search**: Filter contacts and notes as you type
- **Tag Filtering**: Search notes by tags
- **Dialog Forms**: Pop-up windows for adding and editing entries
- **Menu Bar**: File and Help menus for easy navigation

### Contacts Tab
- ✅ View all contacts in a data grid
- ✅ Search contacts by name, phone, or email (real-time)
- ✅ Add new contacts with validation
- ✅ Edit existing contacts
- ✅ Delete contacts with confirmation
- ✅ View birthday reminders for upcoming dates

### Notes Tab
- ✅ View all notes in a data grid
- ✅ Search notes by text content (real-time)
- ✅ Filter notes by tags
- ✅ Add new notes with tags
- ✅ Edit notes and tags
- ✅ Delete notes with confirmation

## Running the GUI

### Option 1: Using the Main Menu
```bash
python main.py
```
Then select option `2` for GUI mode.

### Option 2: Direct GUI Launch
```bash
python gui_main.py
```

## GUI Layout

### Main Window
```
┌─────────────────────────────────────────────────────────┐
│ Personal Assistant Bot - GUI                    [_][□][X]│
├─────────────────────────────────────────────────────────┤
│ File  Help                                               │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 📋 Contacts │ 📝 Notes                              │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Search & Actions                                    │ │
│ │ Search: [________________] ➕ ✏️ 🗑️ 🎂             │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Name      │ Phone    │ Email      │ Address │ Birth │ │
│ │ John Doe  │ +1-234.. │ john@ex... │ 123 M.. │ 15.03 │ │
│ │ Jane Smith│ +1-567.. │ jane@ex... │ 456 O.. │ 22.07 │ │
│ │           │          │            │         │       │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Usage Guide

### Adding a Contact
1. Click the **➕ Add** button in the Contacts tab
2. Fill in the contact details:
   - Name (required)
   - Phone (optional, validated)
   - Email (optional, validated)
   - Address (optional)
   - Birthday (optional, format: DD.MM.YYYY)
3. Click **Save**

### Searching Contacts
1. Type in the **Search** field
2. Results update in real-time
3. Search works on: name, phone, email

### Editing a Contact
1. Select a contact from the table
2. Click the **✏️ Edit** button
3. Modify the fields
4. Click **Save**

### Deleting a Contact
1. Select a contact from the table
2. Click the **🗑️ Delete** button
3. Confirm the deletion

### Birthday Reminders
1. Click the **🎂 Birthdays** button
2. Enter the number of days to look ahead
3. View contacts with upcoming birthdays

### Adding a Note
1. Click the **➕ Add** button in the Notes tab
2. Enter the note text
3. Add tags (comma-separated, optional)
4. Click **Save**

### Searching Notes
1. Use the **Search** field for text search
2. Use the **Tags** field to filter by tags
3. Results update in real-time

### Editing a Note
1. Select a note from the table
2. Click the **✏️ Edit** button
3. Modify the text and/or tags
4. Click **Save**

### Deleting a Note
1. Select a note from the table
2. Click the **🗑️ Delete** button
3. Confirm the deletion

## System Requirements

- Python 3.7 or higher
- Tkinter (included with Python on most systems)
- No external dependencies required

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Alt+F4 | Close application |
| Tab | Navigate between fields |
| Enter | Submit form |
| Escape | Close dialog |

## Data Persistence

- All data is automatically saved to JSON files
- Contacts: `data/contacts.json`
- Notes: `data/notes.json`
- Data persists between sessions

## Validation

### Phone Numbers
- Minimum 10 digits
- Supports: +, spaces, dashes, parentheses
- Example: +1-234-567-8900

### Email Addresses
- Standard email format
- Example: user@example.com

### Birthdays
- Format: DD.MM.YYYY
- Example: 25.05.1990

## Troubleshooting

### GUI doesn't start
- Ensure Python 3.7+ is installed
- Check that Tkinter is available: `python -m tkinter`
- Try running from command line to see error messages

### Data not saving
- Check that `data/` directory exists and is writable
- Ensure sufficient disk space
- Check file permissions

### Search not working
- Clear the search field and try again
- Check that data is loaded (refresh the tab)
- Ensure correct spelling

## Comparison: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| Menu-driven | ✅ | ✅ |
| Real-time search | ❌ | ✅ |
| Data grid view | ❌ | ✅ |
| Tabbed interface | ❌ | ✅ |
| Dialog forms | ❌ | ✅ |
| Keyboard navigation | ✅ | ✅ |
| Mouse support | ❌ | ✅ |
| Lightweight | ✅ | ✅ |
| No dependencies | ✅ | ✅ |

## Future Enhancements

- Dark mode theme
- Export to CSV/Excel
- Import from CSV
- Contact groups/categories
- Note categories
- Recurring reminders
- Contact photos
- Note attachments
- Cloud synchronization

## Support

For issues or questions:
1. Check the main README.md
2. Review DEVELOPER_GUIDE.md for technical details
3. Check QUICKSTART.md for general usage

---

**Version**: 1.0.0
**Last Updated**: 2026-05-26
**Status**: Production Ready
