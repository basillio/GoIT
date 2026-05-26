"""
Test script for Personal Assistant Bot
Tests all core functionality without user interaction
"""
import sys
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from contacts import ContactBook
from notes import NoteBook

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')


def test_contacts():
    print("\n" + "="*50)
    print("TESTING CONTACTS MODULE")
    print("="*50)

    # Create test contact book with separate data directory
    test_dir = Path("test_data")
    contact_book = ContactBook(str(test_dir))

    # Test 1: Add valid contact
    print("\n✓ Test 1: Adding valid contact with all fields")
    try:
        result = contact_book.add_contact(
            "John Doe",
            phone="+1-234-567-8900",
            phone2="+1-234-567-8901",
            email="john@example.com",
            email2="john.doe@example.com",
            address="123 Main St",
            birthday="15.03.1990"
        )
        print(f"  {result}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

    # Test 2: Invalid phone validation
    print("\n✓ Test 2: Phone validation (should reject invalid)")
    try:
        contact_book.add_contact("Jane Doe", phone="123")
        print("  ✗ Failed: Should have rejected invalid phone")
        return False
    except ValueError as e:
        print(f"  {e}")

    # Test 3: Invalid phone2 validation
    print("\n✓ Test 3: Phone2 validation (should reject invalid)")
    try:
        contact_book.add_contact("Jane Doe", phone="+1-234-567-8900", phone2="456")
        print("  ✗ Failed: Should have rejected invalid phone2")
        return False
    except ValueError as e:
        print(f"  {e}")

    # Test 4: Invalid email validation
    print("\n✓ Test 4: Email validation (should reject invalid)")
    try:
        contact_book.add_contact("Bob Smith", email="invalid-email")
        print("  ✗ Failed: Should have rejected invalid email")
        return False
    except ValueError as e:
        print(f"  {e}")

    # Test 5: Invalid email2 validation
    print("\n✓ Test 5: Email2 validation (should reject invalid)")
    try:
        contact_book.add_contact("Bob Smith", email="bob@example.com", email2="invalid-email")
        print("  ✗ Failed: Should have rejected invalid email2")
        return False
    except ValueError as e:
        print(f"  {e}")

    # Test 6: Search contact by phone2
    print("\n✓ Test 6: Searching contact by phone2")
    results = contact_book.search_contact("+1-234-567-8901")
    if results and results[0].name == "John Doe":
        print(f"  Found: {results[0].name} by phone2")
    else:
        print("  ✗ Failed: Contact not found by phone2")
        return False

    # Test 7: Search contact by email2
    print("\n✓ Test 7: Searching contact by email2")
    results = contact_book.search_contact("john.doe@example.com")
    if results and results[0].name == "John Doe":
        print(f"  Found: {results[0].name} by email2")
    else:
        print("  ✗ Failed: Contact not found by email2")
        return False

    # Test 8: Edit contact phone2 and email2
    print("\n✓ Test 8: Editing contact phone2 and email2")
    try:
        result = contact_book.edit_contact(
            "John Doe",
            phone2="+1-999-999-9999",
            email2="newemail@example.com"
        )
        print(f"  {result}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

    # Test 9: List all contacts
    print("\n✓ Test 9: Listing all contacts")
    contacts = contact_book.list_all_contacts()
    print(f"  Total contacts: {len(contacts)}")

    # Test 10: Birthday in N days
    print("\n✓ Test 10: Finding birthdays in N days")
    try:
        # Add contact with birthday tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        contact_book.add_contact("Alice", birthday=tomorrow)
        results = contact_book.get_birthdays_in_days(1)
        print(f"  Found {len(results)} contact(s) with birthday in 1 day")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

    # Test 11: Delete contact
    print("\n✓ Test 11: Deleting contact")
    try:
        result = contact_book.delete_contact("Bob Smith")
        print(f"  {result}")
    except ValueError:
        print("  Contact doesn't exist (expected)")

    # Cleanup
    import shutil
    if test_dir.exists():
        shutil.rmtree(test_dir)

    return True


def test_notes():
    print("\n" + "="*50)
    print("TESTING NOTES MODULE")
    print("="*50)

    # Create test note book with separate data directory
    test_dir = Path("test_data")
    note_book = NoteBook(str(test_dir))

    # Test 1: Add note with tags
    print("\n✓ Test 1: Adding note with tags")
    try:
        result = note_book.add_note("Buy groceries", tags=["shopping", "urgent"])
        print(f"  {result}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

    # Test 2: Add note without tags
    print("\n✓ Test 2: Adding note without tags")
    try:
        result = note_book.add_note("Meeting at 3 PM")
        print(f"  {result}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

    # Test 3: Search notes by text
    print("\n✓ Test 3: Searching notes by text")
    results = note_book.search_notes("groceries")
    if results:
        print(f"  Found {len(results)} note(s)")
    else:
        print("  ✗ Failed: Note not found")
        return False

    # Test 4: Search notes by tags
    print("\n✓ Test 4: Searching notes by tags")
    results = note_book.search_by_tags(["shopping"])
    if results:
        print(f"  Found {len(results)} note(s) with tag 'shopping'")
    else:
        print("  ✗ Failed: Notes not found")
        return False

    # Test 5: Sort notes by tags
    print("\n✓ Test 5: Sorting notes by tags")
    sorted_notes = note_book.sort_by_tags()
    print(f"  Found {len(sorted_notes)} tag(s)")
    for tag, notes in sorted_notes.items():
        if notes:
            print(f"    - {tag}: {len(notes)} note(s)")

    # Test 6: Edit note
    print("\n✓ Test 6: Editing note")
    notes = note_book.list_all_notes()
    if notes:
        note_id = notes[0].id
        try:
            result = note_book.edit_note(note_id, text="Updated text", tags=["updated"])
            print(f"  {result}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            return False

    # Test 7: List all notes
    print("\n✓ Test 7: Listing all notes")
    notes = note_book.list_all_notes()
    print(f"  Total notes: {len(notes)}")

    # Test 8: Delete note
    print("\n✓ Test 8: Deleting note")
    if notes:
        try:
            result = note_book.delete_note(notes[0].id)
            print(f"  {result}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            return False

    # Cleanup
    import shutil
    if test_dir.exists():
        shutil.rmtree(test_dir)

    return True


def main():
    print("\n🧪 PERSONAL ASSISTANT BOT - TEST SUITE")
    print("="*50)

    contacts_ok = test_contacts()
    notes_ok = test_notes()

    print("\n" + "="*50)
    print("TEST RESULTS")
    print("="*50)
    print(f"Contacts Module: {'✅ PASSED' if contacts_ok else '❌ FAILED'}")
    print(f"Notes Module: {'✅ PASSED' if notes_ok else '❌ FAILED'}")

    if contacts_ok and notes_ok:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
