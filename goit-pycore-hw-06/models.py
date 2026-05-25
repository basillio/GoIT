from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field): pass

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old, new):
        # Search for phone object, if not found - raise error
        phone = self.find_phone(old)
        if not phone:
            raise ValueError(f"Phone {old} not found.")
        # Simply create new Phone object (it validates itself)
        idx = self.phones.index(phone)
        self.phones[idx] = Phone(new)

    def find_phone(self, phone_number):
        # returns first found or None
        return next((p for p in self.phones if p.value == phone_number), None)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None) # Deletes if exists, doesn't crash if not