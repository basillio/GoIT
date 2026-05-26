# LAUNCH INSTRUCTIONS - Personal Assistant Bot

**Version**: 1.1.0 (with GUI)
**Date**: 2026-05-26
**Status**: Production Ready

---

## Quick Start

### Fastest Way to Launch

```bash
cd D:\Docs\GoIT\Assistant_bot
python main.py
```

Then select your preferred mode:
- **Option 1**: CLI (Command Line Interface)
- **Option 2**: GUI (Graphical User Interface)

---

## Launch Methods

### Method 1: Main Menu (Recommended for First-Time Users)

```bash
python main.py
```

**What happens:**
1. Application displays mode selection menu
2. Choose between CLI and GUI
3. Application launches in selected mode

**Pros:**
- Easy to switch between modes
- Clear menu interface
- Good for exploring both options

---

### Method 2: Direct GUI Launch

```bash
python gui_main.py
```

**What happens:**
1. GUI window opens immediately
2. Tabbed interface with Contacts and Notes
3. Ready to use

**Pros:**
- Fastest way to launch GUI
- No menu selection needed
- Direct access to graphical interface

---

### Method 3: Direct CLI Launch

```bash
python main.py
```

Then select **Option 1** for CLI mode.

**Pros:**
- Traditional command-line experience
- Good for scripting/automation
- Lightweight interface

---

## System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 50 MB minimum
- **Disk Space**: 200 KB for application

### Verify Python Installation

```bash
python --version
```

Should show Python 3.7 or higher.

### Verify Tkinter Installation (for GUI)

```bash
python -m tkinter
```

A small window should appear. If it does, Tkinter is installed.

---

## Step-by-Step Launch Guide

### For GUI Mode

1. **Open Terminal/Command Prompt**
   ```bash
   cd D:\Docs\GoIT\Assistant_bot
   ```

2. **Launch Application**
   ```bash
   python main.py
   ```

3. **Select GUI Mode**
   - Type `2` and press Enter

4. **GUI Window Opens**
   - Contacts tab is displayed by default
   - Use buttons to add/edit/delete contacts
   - Click Notes tab to manage notes

### For CLI Mode

1. **Open Terminal/Command Prompt**
   ```bash
   cd D:\Docs\GoIT\Assistant_bot
   ```

2. **Launch Application**
   ```bash
   python main.py
   ```

3. **Select CLI Mode**
   - Type `1` and press Enter

4. **Menu Appears**
   - Select options 1-13 for various operations
   - Select 0 to exit

---

## GUI Mode Features

### Main Window Layout

```
┌─────────────────────────────────────────────┐
│ Personal Assistant Bot - GUI                │
├─────────────────────────────────────────────┤
│ File  Help                                  │
├─────────────────────────────────────────────┤
│ [📋 Contacts] [📝 Notes]                    │
├─────────────────────────────────────────────┤
│ Search: [_____________] ➕ ✏️ 🗑️ 🎂      │
├─────────────────────────────────────────────┤
│ Name    │ Phone   │ Email    │ Address     │
│ John    │ +1-234  │ john@... │ 123 Main    │
│ Jane    │ +1-567  │ jane@... │ 456 Oak     │
└─────────────────────────────────────────────┘
```

### Contacts Tab Operations

**Add Contact:**
1. Click "➕ Add" button
2. Fill in contact details
3. Click "Save"

**Search Contacts:**
1. Type in search field
2. Results update automatically

**Edit Contact:**
1. Select contact from table
2. Click "✏️ Edit" button
3. Modify fields
4. Click "Save"

**Delete Contact:**
1. Select contact from table
2. Click "🗑️ Delete" button
3. Confirm deletion

**Check Birthdays:**
1. Click "🎂 Birthdays" button
2. Enter number of days
3. View upcoming birthdays

### Notes Tab Operations

**Add Note:**
1. Click "➕ Add" button
2. Enter note text
3. Add tags (optional, comma-separated)
4. Click "Save"

**Search Notes:**
1. Type in search field for text search
2. Type in tags field for tag filtering
3. Results update automatically

**Edit Note:**
1. Select note from table
2. Click "✏️ Edit" button
3. Modify text and/or tags
4. Click "Save"

**Delete Note:**
1. Select note from table
2. Click "🗑️ Delete" button
3. Confirm deletion

---

## CLI Mode Features

### Main Menu

```
==================================================
ПЕРСОНАЛЬНИЙ ПОМІЧНИК
==================================================

📋 КОНТАКТИ:
  1. Додати контакт
  2. Переглянути всі контакти
  3. Пошук контакту
  4. Редагувати контакт
  5. Видалити контакт
  6. Дні народження через N днів

📝 НОТАТКИ:
  7. Додати нотатку
  8. Переглянути всі нотатки
  9. Пошук нотатки
  10. Пошук нотаток за тегами
  11. Сортування нотаток за тегами
  12. Редагувати нотатку
  13. Видалити нотатку

  0. Вихід
==================================================
```

### Menu Navigation

- Select option by typing number (1-13)
- Follow prompts to enter data
- Type 0 to exit

---

## Troubleshooting

### GUI Won't Start

**Problem**: "No module named 'tkinter'"

**Solution**:
```bash
# Verify Tkinter is installed
python -m tkinter

# If not installed, install it:
# Windows: Usually included with Python
# macOS: brew install python-tk
# Linux: sudo apt-get install python3-tk
```

### Application Won't Launch

**Problem**: "ModuleNotFoundError"

**Solution**:
1. Ensure you're in the correct directory:
   ```bash
   cd D:\Docs\GoIT\Assistant_bot
   ```

2. Verify all files are present:
   ```bash
   ls -la
   ```

3. Check Python version:
   ```bash
   python --version
   ```

### Data Not Saving

**Problem**: Changes don't persist

**Solution**:
1. Check `data/` directory exists
2. Verify write permissions
3. Ensure sufficient disk space
4. Check file permissions on `data/contacts.json` and `data/notes.json`

### Search Not Working

**Problem**: Search returns no results

**Solution**:
1. Clear search field and try again
2. Check spelling
3. Ensure data is loaded (refresh tab)
4. Try searching with partial text

---

## Keyboard Shortcuts

### GUI Mode

| Shortcut | Action |
|----------|--------|
| Alt+F4 | Close application |
| Tab | Navigate between fields |
| Enter | Submit form |
| Escape | Close dialog |

### CLI Mode

| Key | Action |
|-----|--------|
| 0 | Exit application |
| 1-13 | Select menu option |
| Enter | Confirm input |

---

## File Locations

### Application Files
```
D:\Docs\GoIT\Assistant_bot\
├── main.py
├── assistant.py
├── gui.py
├── gui_main.py
├── contacts.py
└── notes.py
```

### Data Files
```
D:\Docs\GoIT\Assistant_bot\data\
├── contacts.json
└── notes.json
```

### Documentation
```
D:\Docs\GoIT\Assistant_bot\
├── README.md
├── GUI_README.md
├── QUICKSTART.md
├── DEVELOPER_GUIDE.md
└── GUI_SUMMARY.md
```

---

## Running Tests

To verify everything is working correctly:

```bash
python test_bot.py
```

Expected output:
```
16/16 tests passing
Contacts Module: PASSED
Notes Module: PASSED
```

---

## Common Tasks

### Add a Contact

**GUI:**
1. Click "➕ Add" in Contacts tab
2. Fill in details
3. Click "Save"

**CLI:**
1. Select option 1
2. Enter contact details
3. Confirm

### Search for a Contact

**GUI:**
1. Type in search field
2. Results update automatically

**CLI:**
1. Select option 3
2. Enter search query
3. View results

### Add a Note with Tags

**GUI:**
1. Click "➕ Add" in Notes tab
2. Enter text
3. Enter tags (comma-separated)
4. Click "Save"

**CLI:**
1. Select option 7
2. Enter note text
3. Enter tags
4. Confirm

### Check Birthday Reminders

**GUI:**
1. Click "🎂 Birthdays" button
2. Enter number of days
3. View results

**CLI:**
1. Select option 6
2. Enter number of days
3. View results

---

## Performance Tips

### For GUI Mode
- Real-time search is fast for up to 1000+ entries
- Data grid scrolls smoothly
- Dialogs open instantly

### For CLI Mode
- Menu navigation is instant
- Search is fast even with large datasets
- No GUI overhead

---

## Data Backup

### Manual Backup

```bash
# Copy data directory
cp -r data/ data_backup/

# Or on Windows
xcopy data data_backup /E
```

### Automatic Backup

Data is automatically saved after each operation to:
- `data/contacts.json`
- `data/notes.json`

---

## Getting Help

### Documentation Files

- **README.md** - Project overview
- **GUI_README.md** - GUI usage guide
- **QUICKSTART.md** - Quick start guide
- **DEVELOPER_GUIDE.md** - Technical details
- **GUI_SUMMARY.md** - GUI features

### In-Application Help

**GUI:**
- Click "Help" menu → "About"

**CLI:**
- Follow on-screen prompts
- Menu options are self-explanatory

---

## Next Steps

1. **Launch the application**:
   ```bash
   python main.py
   ```

2. **Choose your mode**:
   - GUI for visual management
   - CLI for command-line interface

3. **Read the appropriate guide**:
   - GUI_README.md for GUI mode
   - QUICKSTART.md for quick start

4. **Start managing**:
   - Add contacts and notes
   - Use search and filtering
   - Explore all features

---

## Summary

| Task | Command |
|------|---------|
| Launch with menu | `python main.py` |
| Launch GUI directly | `python gui_main.py` |
| Run tests | `python test_bot.py` |
| View help | See documentation files |

---

**Ready to launch?**

```bash
cd D:\Docs\GoIT\Assistant_bot
python main.py
```

Then select your preferred mode and start managing your contacts and notes!

---

**Version**: 1.1.0
**Date**: 2026-05-26
**Status**: Production Ready
