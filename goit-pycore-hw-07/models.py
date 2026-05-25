from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday_value):
        self.birthday = Birthday(birthday_value)

    def edit_phone(self, old_number, new_number):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return
        raise ValueError(f"Phone {old_number} not found.")

    def __str__(self):
        res = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            res += f", birthday: {self.birthday}"
        return res

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            # Guard condition 1: if no birthday, continue
            if not record.birthday:
                continue

            # Determine birthday date in current year
            birthday_this_year = record.birthday.value.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Guard condition 2: if birthday not within next 7 days, continue
            days_until_birthday = (birthday_this_year - today).days
            if not (0 <= days_until_birthday <= 7):
                continue

            # Calculate congratulation date (weekend adjustment)
            congratulation_date = birthday_this_year
            weekday = congratulation_date.weekday()

            if weekday == 5:    # Saturday
                congratulation_date += timedelta(days=2)
            elif weekday == 6:  # Sunday
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": record.name.value,
                "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
            })

        return upcoming_birthdays
  