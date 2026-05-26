"""
Основний модуль Персонального помічника з CLI інтерфейсом
"""
from contacts import ContactBook
from notes import NoteBook
from pathlib import Path


class AssistantBot:
    def __init__(self, data_dir="data"):
        self.contact_book = ContactBook(data_dir)
        self.note_book = NoteBook(data_dir)
        self.running = True

    def display_menu(self):
        print("\n" + "="*50)
        print("📱 ПЕРСОНАЛЬНИЙ ПОМІЧНИК")
        print("="*50)
        print("\n📋 КОНТАКТИ:")
        print("  1. Додати контакт")
        print("  2. Переглянути всі контакти")
        print("  3. Пошук контакту")
        print("  4. Редагувати контакт")
        print("  5. Видалити контакт")
        print("  6. Дні народження через N днів")
        print("\n📝 НОТАТКИ:")
        print("  7. Додати нотатку")
        print("  8. Переглянути всі нотатки")
        print("  9. Пошук нотатки")
        print("  10. Пошук нотаток за тегами")
        print("  11. Сортування нотаток за тегами")
        print("  12. Редагувати нотатку")
        print("  13. Видалити нотатку")
        print("\n  0. Вихід")
        print("="*50)

    def add_contact(self):
        print("\n➕ ДОДАВАННЯ КОНТАКТУ")
        name = input("Ім'я: ").strip()
        if not name:
            print("❌ Ім'я не може бути порожнім")
            return

        phone = input("Телефон (опціонально): ").strip() or None
        email = input("Email (опціонально): ").strip() or None
        address = input("Адреса (опціонально): ").strip() or None
        birthday = input("День народження у форматі ДД.МM.РРРР (опціонально): ").strip() or None

        try:
            result = self.contact_book.add_contact(name, phone, email, address, birthday)
            print(result)
        except ValueError as e:
            print(str(e))

    def view_all_contacts(self):
        print("\n📋 ВСІ КОНТАКТИ")
        contacts = self.contact_book.list_all_contacts()
        if not contacts:
            print("❌ Контактів не знайдено")
            return

        for i, contact in enumerate(contacts, 1):
            print(f"\n{i}. {contact.name}")
            if contact.phone:
                print(f"   Телефон: {contact.phone}")
            if contact.email:
                print(f"   Email: {contact.email}")
            if contact.address:
                print(f"   Адреса: {contact.address}")
            if contact.birthday:
                print(f"   День народження: {contact.birthday}")

    def search_contact(self):
        print("\n🔍 ПОШУК КОНТАКТУ")
        query = input("Введіть ім'я, телефон або email: ").strip()
        if not query:
            print("❌ Запит не може бути порожнім")
            return

        results = self.contact_book.search_contact(query)
        if not results:
            print("❌ Контактів не знайдено")
            return

        print(f"\n✅ Знайдено {len(results)} контакт(ів):")
        for i, contact in enumerate(results, 1):
            print(f"\n{i}. {contact.name}")
            if contact.phone:
                print(f"   Телефон: {contact.phone}")
            if contact.email:
                print(f"   Email: {contact.email}")
            if contact.address:
                print(f"   Адреса: {contact.address}")
            if contact.birthday:
                print(f"   День народження: {contact.birthday}")

    def edit_contact(self):
        print("\n✏️ РЕДАГУВАННЯ КОНТАКТУ")
        name = input("Ім'я контакту для редагування: ").strip()
        if not name:
            print("❌ Ім'я не може бути порожнім")
            return

        if name not in self.contact_book.contacts:
            print(f"❌ Контакт '{name}' не знайдено")
            return

        contact = self.contact_book.contacts[name]
        print(f"\nТекучі дані контакту '{name}':")
        print(f"  Телефон: {contact.phone or 'не вказано'}")
        print(f"  Email: {contact.email or 'не вказано'}")
        print(f"  Адреса: {contact.address or 'не вказано'}")
        print(f"  День народження: {contact.birthday or 'не вказано'}")

        updates = {}
        if input("\nЗмінити телефон? (y/n): ").lower() == 'y':
            updates['phone'] = input("Новий телефон: ").strip() or None
        if input("Змінити email? (y/n): ").lower() == 'y':
            updates['email'] = input("Новий email: ").strip() or None
        if input("Змінити адресу? (y/n): ").lower() == 'y':
            updates['address'] = input("Нова адреса: ").strip() or None
        if input("Змінити день народження? (y/n): ").lower() == 'y':
            updates['birthday'] = input("Новий день народження (ДД.МM.РРРР): ").strip() or None

        if updates:
            try:
                result = self.contact_book.edit_contact(name, **updates)
                print(result)
            except ValueError as e:
                print(str(e))
        else:
            print("❌ Жодних змін не внесено")

    def delete_contact(self):
        print("\n🗑️ ВИДАЛЕННЯ КОНТАКТУ")
        name = input("Ім'я контакту для видалення: ").strip()
        if not name:
            print("❌ Ім'я не може бути порожнім")
            return

        try:
            result = self.contact_book.delete_contact(name)
            print(result)
        except ValueError as e:
            print(str(e))

    def birthdays_in_days(self):
        print("\n🎂 ДНІ НАРОДЖЕННЯ")
        try:
            days = int(input("Через скільки днів шукати дні народження? "))
            results = self.contact_book.get_birthdays_in_days(days)
            if not results:
                print(f"❌ Контактів з днем народження через {days} днів не знайдено")
                return

            print(f"\n✅ Контакти з днем народження через {days} днів:")
            for contact in results:
                print(f"  • {contact.name} - {contact.birthday}")
        except ValueError:
            print("❌ Введіть коректне число")

    def add_note(self):
        print("\n➕ ДОДАВАННЯ НОТАТКИ")
        text = input("Текст нотатки: ").strip()
        if not text:
            print("❌ Текст не може бути порожнім")
            return

        tags_input = input("Теги (розділені комами, опціонально): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

        try:
            result = self.note_book.add_note(text, tags)
            print(result)
        except ValueError as e:
            print(str(e))

    def view_all_notes(self):
        print("\n📝 ВСІ НОТАТКИ")
        notes = self.note_book.list_all_notes()
        if not notes:
            print("❌ Нотаток не знайдено")
            return

        for i, note in enumerate(notes, 1):
            print(f"\n{i}. ID: {note.id}")
            print(f"   Текст: {note.text}")
            if note.tags:
                print(f"   Теги: {', '.join(note.tags)}")
            print(f"   Створено: {note.created_at}")

    def search_notes(self):
        print("\n🔍 ПОШУК НОТАТКИ")
        query = input("Введіть текст для пошуку: ").strip()
        if not query:
            print("❌ Запит не може бути порожнім")
            return

        results = self.note_book.search_notes(query)
        if not results:
            print("❌ Нотаток не знайдено")
            return

        print(f"\n✅ Знайдено {len(results)} нотатк(и):")
        for i, note in enumerate(results, 1):
            print(f"\n{i}. ID: {note.id}")
            print(f"   Текст: {note.text}")
            if note.tags:
                print(f"   Теги: {', '.join(note.tags)}")

    def search_notes_by_tags(self):
        print("\n🏷️ ПОШУК НОТАТОК ЗА ТЕГАМИ")
        tags_input = input("Введіть теги (розділені комами): ").strip()
        if not tags_input:
            print("❌ Теги не можуть бути порожніми")
            return

        tags = [tag.strip() for tag in tags_input.split(",")]
        results = self.note_book.search_by_tags(tags)
        if not results:
            print("❌ Нотаток з такими тегами не знайдено")
            return

        print(f"\n✅ Знайдено {len(results)} нотатк(и):")
        for i, note in enumerate(results, 1):
            print(f"\n{i}. ID: {note.id}")
            print(f"   Текст: {note.text}")
            if note.tags:
                print(f"   Теги: {', '.join(note.tags)}")

    def sort_notes_by_tags(self):
        print("\n📊 СОРТУВАННЯ НОТАТОК ЗА ТЕГАМИ")
        sorted_notes = self.note_book.sort_by_tags()
        if not sorted_notes:
            print("❌ Нотаток не знайдено")
            return

        for tag, notes in sorted_notes.items():
            if notes:
                print(f"\n🏷️ Тег: {tag}")
                for note in notes:
                    print(f"  • {note.text[:50]}... (ID: {note.id})")

    def edit_note(self):
        print("\n✏️ РЕДАГУВАННЯ НОТАТКИ")
        note_id = input("ID нотатки для редагування: ").strip()
        if not note_id:
            print("❌ ID не може бути порожнім")
            return

        if note_id not in self.note_book.notes:
            print(f"❌ Нотатка з ID '{note_id}' не знайдена")
            return

        note = self.note_book.notes[note_id]
        print(f"\nТекучі дані нотатки:")
        print(f"  Текст: {note.text}")
        print(f"  Теги: {', '.join(note.tags) if note.tags else 'немає'}")

        updates = {}
        if input("\nЗмінити текст? (y/n): ").lower() == 'y':
            updates['text'] = input("Новий текст: ").strip()
        if input("Змінити теги? (y/n): ").lower() == 'y':
            tags_input = input("Нові теги (розділені комами): ").strip()
            updates['tags'] = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

        if updates:
            try:
                result = self.note_book.edit_note(note_id, **updates)
                print(result)
            except ValueError as e:
                print(str(e))
        else:
            print("❌ Жодних змін не внесено")

    def delete_note(self):
        print("\n🗑️ ВИДАЛЕННЯ НОТАТКИ")
        note_id = input("ID нотатки для видалення: ").strip()
        if not note_id:
            print("❌ ID не може бути порожнім")
            return

        try:
            result = self.note_book.delete_note(note_id)
            print(result)
        except ValueError as e:
            print(str(e))

    def run(self):
        print("\n🎉 Ласкаво просимо до Персонального помічника!")
        while self.running:
            self.display_menu()
            choice = input("\nВиберіть опцію: ").strip()

            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.view_all_contacts()
            elif choice == "3":
                self.search_contact()
            elif choice == "4":
                self.edit_contact()
            elif choice == "5":
                self.delete_contact()
            elif choice == "6":
                self.birthdays_in_days()
            elif choice == "7":
                self.add_note()
            elif choice == "8":
                self.view_all_notes()
            elif choice == "9":
                self.search_notes()
            elif choice == "10":
                self.search_notes_by_tags()
            elif choice == "11":
                self.sort_notes_by_tags()
            elif choice == "12":
                self.edit_note()
            elif choice == "13":
                self.delete_note()
            elif choice == "0":
                print("\n👋 До побачення!")
                self.running = False
            else:
                print("❌ Невірна опція. Спробуйте ще раз.")
