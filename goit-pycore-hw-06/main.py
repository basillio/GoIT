from models import AddressBook, Record

def main():
    # 1. Create address book
    book = AddressBook()

    # 2. Create record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    # 3. Create record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # 4. Display result
    print("--- All records ---")
    for name, record in book.data.items():
        print(record)

    # 5. Edit John's phone
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")

    print("\n--- After edit John ---")
    print(john)

    # Search for specific phone (add output to screen)
    found_phone = john.find_phone("5555555555")
    print(f"Found phone for John: {found_phone}")

    # 6. Delete Jane
    book.delete("Jane")

    print("\n--- Final list ---")
    for name, record in book.data.items():
        print(record)

if __name__ == "__main__":
    main()