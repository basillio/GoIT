"""
Модуль для управління контактами
"""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


class Contact:
    def __init__(self, name, phone=None, phone2=None, email=None, email2=None, address=None, birthday=None, notes=None, tags=None, color=None):
        self.name = name
        self.phone = phone
        self.phone2 = phone2
        self.email = email
        self.email2 = email2
        self.address = address
        self.birthday = birthday
        self.notes = notes or []
        self.tags = tags or []
        self.color = color

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "phone2": self.phone2,
            "email": self.email,
            "email2": self.email2,
            "address": self.address,
            "birthday": self.birthday,
            "notes": self.notes,
            "tags": self.tags,
            "color": self.color,
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            name=data["name"],
            phone=data.get("phone"),
            phone2=data.get("phone2"),
            email=data.get("email"),
            email2=data.get("email2"),
            address=data.get("address"),
            birthday=data.get("birthday"),
            notes=data.get("notes", []),
            tags=data.get("tags", []),
            color=data.get("color"),
        )

    def __str__(self):
        phones = f"{self.phone}" + (f", {self.phone2}" if self.phone2 else "")
        emails = f"{self.email}" + (f", {self.email2}" if self.email2 else "")
        result = f"Ім'я: {self.name}\nТелефони: {phones}\nEmails: {emails}\nАдреса: {self.address}\nДень народження: {self.birthday}"
        if self.tags:
            result += f"\nТеги: {', '.join(self.tags)}"
        if self.notes:
            result += f"\nНотатки: {'; '.join(self.notes)}"
        if self.color:
            result += f"\nКолір: {self.color}"
        return result


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

    def add_contact(self, name, phone=None, phone2=None, email=None, email2=None, address=None, birthday=None, notes=None, tags=None, color=None):
        if not self.validate_phone(phone):
            raise ValueError("❌ Некоректний номер телефону")
        if phone2 and not self.validate_phone(phone2):
            raise ValueError("❌ Некоректний другий номер телефону")
        if not self.validate_email(email):
            raise ValueError("❌ Некоректний email")
        if email2 and not self.validate_email(email2):
            raise ValueError("❌ Некоректний другий email")

        if name in self.contacts:
            raise ValueError(f"❌ Контакт '{name}' вже існує")

        self.contacts[name] = Contact(name, phone, phone2, email, email2, address, birthday, notes, tags, color)
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
        if "phone2" in kwargs and kwargs["phone2"] and not self.validate_phone(kwargs["phone2"]):
            raise ValueError("❌ Некоректний другий номер телефону")
        if "email" in kwargs and not self.validate_email(kwargs["email"]):
            raise ValueError("❌ Некоректний email")
        if "email2" in kwargs and kwargs["email2"] and not self.validate_email(kwargs["email2"]):
            raise ValueError("❌ Некоректний другий email")

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
                (contact.phone2 and query_lower in contact.phone2) or
                (contact.email and query_lower in contact.email) or
                (contact.email2 and query_lower in contact.email2)):
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
