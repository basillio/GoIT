# 1. Create decorator for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
    return inner

# 2. Input parsing function
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# 3. Command handling functions with decorators
@input_error
def add_contact(args, contacts):
    # If args is empty or has only 1 element,
    # attempting to unpack name, phone will raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    # If name doesn't exist, we raise KeyError ourselves
    raise KeyError

@input_error
def show_phone(args, contacts):
    # If args is empty, args[0] will raise IndexError
    name = args[0]
    # Access via contacts[name] will raise KeyError if name doesn't exist
    return contacts[name]

def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

# 4. Main bot loop
def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()