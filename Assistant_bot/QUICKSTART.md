# Quick Start Guide

## Installation

1. Ensure Python 3.7+ is installed on your system
2. Navigate to the project directory:
   ```bash
   cd D:\Docs\GoIT\Assistant_bot
   ```

## Running the Application

Start the Personal Assistant Bot:
```bash
python main.py
```

## Menu Options

### Contacts Management (Options 1-6)
1. **Add Contact** - Create a new contact with name, phone, email, address, and birthday
2. **View All Contacts** - Display all saved contacts
3. **Search Contact** - Find contacts by name, phone, or email
4. **Edit Contact** - Update contact information
5. **Delete Contact** - Remove a contact
6. **Birthdays in N Days** - Find contacts with upcoming birthdays

### Notes Management (Options 7-13)
7. **Add Note** - Create a new note with optional tags
8. **View All Notes** - Display all saved notes
9. **Search Note** - Find notes by text content
10. **Search by Tags** - Find notes with specific tags
11. **Sort by Tags** - View notes organized by tags
12. **Edit Note** - Update note content or tags
13. **Delete Note** - Remove a note

## Data Format

### Contact Format
```json
{
  "name": "John Doe",
  "phone": "+1-234-567-8900",
  "email": "john@example.com",
  "address": "123 Main St",
  "birthday": "15.03.1990"
}
```

### Note Format
```json
{
  "id": "unique-uuid",
  "text": "Note content",
  "tags": ["tag1", "tag2"],
  "created_at": "2026-05-25T12:00:00"
}
```

## Validation Rules

### Phone Number
- Minimum 10 digits
- Supports: +, spaces, dashes, parentheses
- Example: +1-234-567-8900, (123) 456-7890

### Email
- Standard email format
- Example: user@example.com

### Birthday
- Format: DD.MM.YYYY
- Example: 25.05.1990

## Testing

Run the test suite to verify all functionality:
```bash
python test_bot.py
```

## File Structure

```
Assistant_bot/
├── main.py              # Application entry point
├── assistant.py         # CLI interface and main logic
├── contacts.py          # Contact management module
├── notes.py             # Notes management module
├── test_bot.py          # Test suite
├── config.json          # Configuration file
├── requirements.txt     # Dependencies (none required)
├── README.md            # Full documentation
├── QUICKSTART.md        # This file
└── data/                # Data storage (auto-created)
    ├── contacts.json    # Contacts database
    └── notes.json       # Notes database
```

## Tips

- All data is automatically saved to JSON files
- Data persists between sessions
- Use tags to organize notes effectively
- Search is case-insensitive
- Birthday reminders help you remember important dates

## Troubleshooting

**Issue: "ModuleNotFoundError"**
- Ensure all Python files are in the same directory
- Check that you're running from the correct directory

**Issue: "UnicodeEncodeError"**
- This is handled automatically on Windows
- If issues persist, ensure Python 3.7+ is installed

**Issue: Data not saving**
- Check that the `data/` directory has write permissions
- Ensure disk space is available

## Features Implemented

✅ Contact management (add, edit, delete, search)
✅ Phone and email validation
✅ Birthday reminders
✅ Notes with tags
✅ Full-text search in notes
✅ Tag-based search and sorting
✅ Persistent JSON storage
✅ Modular architecture
✅ Comprehensive test suite
