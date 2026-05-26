# Developer Guide

## Architecture Overview

The Personal Assistant Bot follows a modular, layered architecture:

```
┌─────────────────────────────────────┐
│      CLI Interface (assistant.py)   │
│      - User interaction             │
│      - Menu handling                │
│      - Input/output formatting      │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────┐
│ ContactBook │  │  NoteBook   │
│ (contacts.py)  │  (notes.py)  │
│ - CRUD ops  │  │ - CRUD ops  │
│ - Validation│  │ - Search    │
│ - Storage   │  │ - Tags      │
└──────┬──────┘  └──────┬──────┘
       │                │
       └────────┬───────┘
                │
        ┌───────▼────────┐
        │  JSON Storage  │
        │  (data/ dir)   │
        └────────────────┘
```

## Code Organization

### contacts.py
- **Contact class**: Data model for a single contact
- **ContactBook class**: Business logic for contact operations
- Responsibilities:
  - Load/save contacts from/to JSON
  - Validate phone and email
  - Search and filter contacts
  - Calculate birthday dates

### notes.py
- **Note class**: Data model for a single note
- **NoteBook class**: Business logic for note operations
- Responsibilities:
  - Load/save notes from/to JSON
  - Manage tags
  - Search and filter notes
  - Sort notes by tags

### assistant.py
- **AssistantBot class**: Main application controller
- Responsibilities:
  - Display menu
  - Handle user input
  - Call appropriate business logic
  - Format and display results

### main.py
- Entry point
- Initializes and runs AssistantBot

## Adding New Features

### Example: Add Contact Categories

1. **Update Contact class** (contacts.py):
```python
class Contact:
    def __init__(self, name, phone=None, email=None, address=None, 
                 birthday=None, category=None):
        # ... existing code ...
        self.category = category
```

2. **Update ContactBook** (contacts.py):
```python
def search_by_category(self, category):
    results = []
    for contact in self.contacts.values():
        if contact.category and contact.category.lower() == category.lower():
            results.append(contact)
    return results
```

3. **Update AssistantBot** (assistant.py):
```python
def search_by_category(self):
    print("\n🔍 SEARCH BY CATEGORY")
    category = input("Enter category: ").strip()
    results = self.contact_book.search_by_category(category)
    # Display results...
```

4. **Add menu option** in `display_menu()` and `run()` method

5. **Add tests** in test_bot.py

## Extending Search Functionality

### Current Search Capabilities
- Contacts: by name, phone, email
- Notes: by text content, by tags

### Possible Extensions
- Advanced filters (date range, multiple criteria)
- Regex pattern matching
- Fuzzy search
- Search history

### Implementation Pattern
```python
def advanced_search(self, criteria):
    """
    criteria: dict with search parameters
    Returns: list of matching items
    """
    results = []
    for item in self.items.values():
        if self._matches_criteria(item, criteria):
            results.append(item)
    return results

def _matches_criteria(self, item, criteria):
    # Implement matching logic
    pass
```

## Database Migration

### Current: JSON Storage
- Pros: Simple, human-readable, no dependencies
- Cons: Not scalable, no indexing, concurrent access issues

### Future: SQLite
```python
import sqlite3

class ContactBookSQL:
    def __init__(self, db_path="data/assistant.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                birthday TEXT
            )
        ''')
        self.conn.commit()
```

## Testing Guidelines

### Test Structure
```python
def test_feature():
    # Setup
    obj = SomeClass()
    
    # Execute
    result = obj.some_method()
    
    # Assert
    assert result == expected_value
```

### Test Coverage Areas
1. **Happy Path**: Normal operation with valid input
2. **Validation**: Invalid input handling
3. **Edge Cases**: Boundary conditions
4. **Error Handling**: Exception scenarios
5. **Data Persistence**: Save/load operations

### Running Tests
```bash
python test_bot.py
```

### Adding New Tests
```python
def test_new_feature():
    print("\n✓ Test: New Feature")
    try:
        # Test implementation
        assert condition
        print("  Test passed")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
```

## Performance Considerations

### Current Implementation
- **Load Time**: O(1) - loads entire JSON file on startup
- **Search Time**: O(n) - linear search through all items
- **Memory**: All data in memory

### Optimization Strategies
1. **Lazy Loading**: Load data only when needed
2. **Indexing**: Create indexes for frequently searched fields
3. **Caching**: Cache search results
4. **Pagination**: Load data in chunks

### Example: Indexed Search
```python
class ContactBook:
    def __init__(self):
        self.contacts = {}
        self.name_index = {}  # name -> contact mapping
        self.email_index = {}  # email -> contact mapping
    
    def add_contact(self, contact):
        self.contacts[contact.name] = contact
        self.name_index[contact.name.lower()] = contact
        if contact.email:
            self.email_index[contact.email.lower()] = contact
```

## Error Handling Best Practices

### Current Pattern
```python
try:
    result = operation()
    print(f"✅ Success: {result}")
except ValueError as e:
    print(f"❌ {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Enhanced Pattern
```python
class AssistantException(Exception):
    """Base exception for assistant"""
    pass

class ValidationError(AssistantException):
    """Raised when validation fails"""
    pass

class StorageError(AssistantException):
    """Raised when storage operation fails"""
    pass

# Usage
try:
    contact_book.add_contact(...)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    print(f"❌ Invalid input: {e}")
except StorageError as e:
    logger.error(f"Storage failed: {e}")
    print(f"❌ Could not save data: {e}")
```

## Code Style Guidelines

### Naming Conventions
- **Classes**: PascalCase (Contact, ContactBook)
- **Functions/Methods**: snake_case (add_contact, search_notes)
- **Constants**: UPPER_SNAKE_CASE (MAX_PHONE_LENGTH)
- **Private**: _leading_underscore (_load_contacts)

### Documentation
- Module docstring at top of file
- Class docstring describing purpose
- Method docstring for complex logic
- Inline comments for non-obvious code

### Example
```python
"""
Module for managing contacts with validation and persistence.
"""

class ContactBook:
    """Manages contact storage, retrieval, and validation."""
    
    def add_contact(self, name, phone=None, email=None):
        """
        Add a new contact with validation.
        
        Args:
            name: Contact name (required)
            phone: Phone number (optional)
            email: Email address (optional)
            
        Returns:
            str: Success message
            
        Raises:
            ValueError: If validation fails
        """
        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number")
        # Implementation...
```

## Debugging Tips

### Enable Logging
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In code
logger.debug(f"Loading contacts from {self.contacts_file}")
logger.info(f"Added contact: {name}")
logger.warning(f"Invalid phone: {phone}")
logger.error(f"Failed to save: {e}")
```

### Print Debugging
```python
# Temporary debug output
print(f"DEBUG: contacts = {self.contacts}")
print(f"DEBUG: search results = {results}")
```

### Interactive Debugging
```python
import pdb

# Set breakpoint
pdb.set_trace()

# Commands: n (next), s (step), c (continue), p (print), l (list)
```

## Version Control

### Commit Message Format
```
[TYPE] Brief description

Detailed explanation if needed.

- Bullet point 1
- Bullet point 2
```

### Types
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[REFACTOR]` - Code refactoring
- `[TEST]` - Test additions/changes
- `[DOCS]` - Documentation
- `[CHORE]` - Maintenance

### Example
```
[FEAT] Add contact categories

- Add category field to Contact class
- Implement search_by_category method
- Add menu option for category search
- Update tests for new functionality
```

## Deployment Checklist

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] No hardcoded paths or credentials
- [ ] Error handling is comprehensive
- [ ] Performance is acceptable
- [ ] Data backup strategy in place
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] README is current

## Common Issues and Solutions

### Issue: Data not persisting
**Solution**: Check file permissions, ensure data/ directory exists and is writable

### Issue: Slow search with large datasets
**Solution**: Implement indexing or migrate to database

### Issue: Unicode encoding errors
**Solution**: Ensure UTF-8 encoding in file operations

### Issue: Duplicate contacts
**Solution**: Implement uniqueness constraint on name field

## Resources

- Python Documentation: https://docs.python.org/3/
- JSON Format: https://www.json.org/
- Regular Expressions: https://docs.python.org/3/library/re.html
- DateTime: https://docs.python.org/3/library/datetime.html

---

**Last Updated**: 2026-05-25
**Version**: 1.0.0
