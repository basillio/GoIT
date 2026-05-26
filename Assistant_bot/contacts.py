"""
Модуль для управління контактами
"""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


class Contact:
    def __init__(self, name, phone=None, email=None, address=None, birthday=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.birthday = birthday

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "birthday": self.birthday,
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            name=data["name"],
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            birthday=data.get("birthday"),
        )

    def __str__(self):
        return f"Ім'я: {self.name}\nТелефон: {self.phone}\nEmail: {self.email}\nАдреса: {self.address}\nДень народження: {self.birthday}"


class ContactBook:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.contacts_file = self.data_dir / "contacts.json"
        self.contacts = self._load_contacts()

    def _load_contacts(self):
        if self.contacts_file.exists():
            with open(self.contacts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {name: Contact.from_dict(contact) for name, contact in data.items()}
        return {}

    def _save_contacts(self):
        with open(self.contacts_file, "w", encoding="utf-8") as f:
            data = {name: contact.to_dict() for name, contact in self.contacts.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def validate_phone(phone):
        """Валідація номера телефону (10+ цифр)"""
        if not phone:
            return True
        pattern = r"^\+?[\d\s\-\(\)]{10,}$"
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_email(email):
        """Валідація email"""
        if not email:
            return True
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def add_contact(self, name, phone=None, email=None, address=None, birthday=None):
        if not self.validate_phone(phone):
            raise ValueError("❌ Некоректний номер телефону")
        if not self.validate_email(email):
            raise ValueError("❌ Некоректний email")

        if name in self.contacts:
            raise ValueError(f"❌ Контакт '{name}' вже існує")

        self.contacts[name] = Contact(name, phone, email, address, birthday)
        self._save_contacts()
        return f"✅ Контакт '{name}' додано"

    def delete_contact(self, name):
        if name not in self.contacts:
            raise ValueError(f"❌ Контакт '{name}' не знайдено")
        del self.contacts[name]
        self._save_contacts()
        return f"✅ Контакт '{name}' видалено"

    def edit_contact(self, name, **kwargs):
        if name not in self.contacts:
            raise ValueError(f"❌ Контакт '{name}' не знайдено")

        contact = self.contacts[name]

        if "phone" in kwargs and not self.validate_phone(kwargs["phone"]):
            raise ValueError("❌ Некоректний номер телефону")
        if "email" in kwargs and not self.validate_email(kwargs["email"]):
            raise ValueError("❌ Некоректний email")

        for key, value in kwargs.items():
            if hasattr(contact, key):
                setattr(contact, key, value)

        self._save_contacts()
        return f"✅ Контакт '{name}' оновлено"

    def search_contact(self, query):
        results = []
        query_lower = query.lower()
        for name, contact in self.contacts.items():
            if (query_lower in name.lower() or
                (contact.phone and query_lower in contact.phone) or
                (contact.email and query_lower in contact.email)):
                results.append(contact)
        return results

    def get_birthdays_in_days(self, days):
        """Отримати контакти з днем народження через задану кількість днів"""
        if not days or days < 0:
            raise ValueError("❌ Кількість днів повинна бути позитивним числом")

        today = datetime.now().date()
        target_date = today + timedelta(days=days)
        results = []

        for contact in self.contacts.values():
            if contact.birthday:
                try:
                    birthday = datetime.strptime(contact.birthday, "%d.%m.%Y").date()
                    birthday_this_year = birthday.replace(year=today.year)

                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                    if birthday_this_year == target_date:
                        results.append(contact)
                except ValueError:
                    pass

        return results

    def list_all_contacts(self):
        return list(self.contacts.values())
