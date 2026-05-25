from models import Record, AddressBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e: return str(e)
        except IndexError: return "Enter user name and the required information."
        except KeyError: return "Contact not found."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday: return f"{name}'s birthday: {record.birthday}"
    raise KeyError

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming: return "No birthdays next week."
    return "\n".join([f"{u['name']}: {u['congratulation_date']}" for u in upcoming])

@input_error
def change_contact(args, book: AddressBook):
    # Per requirements: change [name] [old phone] [new phone]
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        # Call the Record class method you already wrote!
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    # Per requirements: phone [name]
    name = args[0]
    record = book.find(name)
    if record:
        if record.phones:
            # Collect all contact phones into one string
            return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"
        return f"{name} has no phone numbers saved."
    raise KeyError