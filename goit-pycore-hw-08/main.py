import pickle
from models import AddressBook
from handlers import (
    parse_input, 
    add_contact, 
    change_contact,  
    show_phone,     
    add_birthday, 
    show_birthday, 
    birthdays,
    show_all_contacts   
)

# --- Data serialization functions ---

def save_data(book, filename="addressbook.pkl"):
    """Saves address book object to binary file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Loads data from file. If file is missing, creates new AddressBook."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# --- Main function ---

def main():
    # Load saved book or create new one on first run
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                # Automatically save all accumulated data before exit
                save_data(book)
                print("Good bye!")
                break

            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "phone":
                print(show_phone(args, book))

            case "add-birthday":
                print(add_birthday(args, book))

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(birthdays(args, book))

            case "all":
                print(show_all_contacts(book))

            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
    