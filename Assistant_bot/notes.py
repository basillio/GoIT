"""
Модуль для управління нотатками
"""
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


class Note:
    def __init__(self, text, tags=None, note_id=None, created_at=None):
        self.id = note_id or str(uuid4())
        self.text = text
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "tags": self.tags,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Note(
            text=data["text"],
            tags=data.get("tags", []),
            note_id=data.get("id"),
            created_at=data.get("created_at"),
        )

    def __str__(self):
        tags_str = f"Теги: {', '.join(self.tags)}" if self.tags else "Теги: немає"
        return f"ID: {self.id}\nТекст: {self.text}\n{tags_str}\nСтворено: {self.created_at}"


class NoteBook:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.notes_file = self.data_dir / "notes.json"
        self.notes = self._load_notes()

    def _load_notes(self):
        if self.notes_file.exists():
            with open(self.notes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {note_id: Note.from_dict(note) for note_id, note in data.items()}
        return {}

    def _save_notes(self):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            data = {note_id: note.to_dict() for note_id, note in self.notes.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_note(self, text, tags=None):
        if not text or not text.strip():
            raise ValueError("❌ Текст нотатки не може бути порожнім")

        note = Note(text, tags or [])
        self.notes[note.id] = note
        self._save_notes()
        return f"✅ Нотатка додана (ID: {note.id})"

    def delete_note(self, note_id):
        if note_id not in self.notes:
            raise ValueError(f"❌ Нотатка з ID '{note_id}' не знайдена")
        del self.notes[note_id]
        self._save_notes()
        return f"✅ Нотатка видалена"

    def edit_note(self, note_id, text=None, tags=None):
        if note_id not in self.notes:
            raise ValueError(f"❌ Нотатка з ID '{note_id}' не знайдена")

        note = self.notes[note_id]
        if text is not None:
            if not text.strip():
                raise ValueError("❌ Текст нотатки не може бути порожнім")
            note.text = text
        if tags is not None:
            note.tags = tags

        self._save_notes()
        return f"✅ Нотатка оновлена"

    def search_notes(self, query):
        results = []
        query_lower = query.lower()
        for note in self.notes.values():
            if query_lower in note.text.lower():
                results.append(note)
        return results

    def search_by_tags(self, tags):
        """Пошук нотаток за тегами"""
        if isinstance(tags, str):
            tags = [tags]
        tags_lower = [tag.lower() for tag in tags]
        results = []
        for note in self.notes.values():
            note_tags_lower = [tag.lower() for tag in note.tags]
            if any(tag in note_tags_lower for tag in tags_lower):
                results.append(note)
        return results

    def sort_by_tags(self, tags=None):
        """Сортування нотаток за тегами"""
        if tags is None:
            tags = set()
            for note in self.notes.values():
                tags.update(note.tags)
            tags = sorted(list(tags))

        sorted_notes = {}
        for tag in tags:
            sorted_notes[tag] = self.search_by_tags([tag])
        return sorted_notes

    def list_all_notes(self):
        return list(self.notes.values())
