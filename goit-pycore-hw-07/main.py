from models import AddressBook
from handlers import (
    parse_input, 
    add_contact, 
    change_contact,  
    show_phone,     
    add_birthday, 
    show_birthday, 
    birthdays
)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue
        
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
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
                if not book.data:
                    print("Address book is empty.")
                else:
                    for record in book.data.values():
                        print(record)
                        
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()