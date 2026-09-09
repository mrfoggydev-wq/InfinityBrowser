"""
Встроенный блокнот:
- Создание/редактирование заметок
- Категории и теги
- Поиск по заметкам
- Экспорт/импорт
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal

class Note:
    """Класс заметки"""
    
    def __init__(self, title: str = "", content: str = "", category: str = "Общие"):
        self.id = str(datetime.now().timestamp())
        self.title = title
        self.content = content
        self.category = category
        self.tags = []
        self.created = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()
        self.pinned = False
        self.color = "#2a2a3e"
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "created": self.created,
            "updated": self.updated,
            "pinned": self.pinned,
            "color": self.color
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        """Создание заметки из словаря"""
        note = cls(data.get("title", ""), data.get("content", ""), data.get("category", "Общие"))
        note.id = data.get("id", str(datetime.now().timestamp()))
        note.tags = data.get("tags", [])
        note.created = data.get("created", datetime.now().isoformat())
        note.updated = data.get("updated", datetime.now().isoformat())
        note.pinned = data.get("pinned", False)
        note.color = data.get("color", "#2a2a3e")
        return note

class NotesManager(QObject):
    """Менеджер заметок"""
    
    # Сигналы
    note_added = pyqtSignal(Note)
    note_updated = pyqtSignal(Note)
    note_deleted = pyqtSignal(str)  # note_id
    notes_loaded = pyqtSignal(list)  # notes
    
    def __init__(self):
        super().__init__()
        
        self.notes: List[Note] = []
        self.categories = set()
        self.all_tags = set()
        self.notes_file = "notes.json"
        
        # Загрузка заметок
        self.load_notes()
    
    def add_note(self, title: str, content: str, category: str = "Общие") -> Note:
        """Добавление заметки"""
        note = Note(title, content, category)
        self.notes.append(note)
        self.categories.add(category)
        
        # Обновляем теги
        self.update_tags(note)
        
        self.save_notes()
        self.note_added.emit(note)
        return note
    
    def update_note(self, note_id: str, title: str = None, content: str = None, 
                   category: str = None, tags: List[str] = None, pinned: bool = None) -> bool:
        """Обновление заметки"""
        for note in self.notes:
            if note.id == note_id:
                if title is not None:
                    note.title = title
                if content is not None:
                    note.content = content
                if category is not None:
                    if category not in self.categories:
                        self.categories.add(category)
                    note.category = category
                if tags is not None:
                    note.tags = tags
                    self.update_tags(note)
                if pinned is not None:
                    note.pinned = pinned
                
                note.updated = datetime.now().isoformat()
                self.save_notes()
                self.note_updated.emit(note)
                return True
        return False
    
    def delete_note(self, note_id: str) -> bool:
        """Удаление заметки"""
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self.save_notes()
                self.note_deleted.emit(note_id)
                return True
        return False
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Получение заметки по ID"""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
    
    def get_notes_by_category(self, category: str) -> List[Note]:
        """Получение заметок по категории"""
        return [note for note in self.notes if note.category == category]
    
    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Получение заметок по тегу"""
        return [note for note in self.notes if tag in note.tags]
    
    def search_notes(self, query: str) -> List[Note]:
        """Поиск заметок"""
        query = query.lower()
        results = []
        
        for note in self.notes:
            if (query in note.title.lower() or 
                query in note.content.lower() or
                query in note.category.lower() or
                any(query in tag.lower() for tag in note.tags)):
                results.append(note)
        
        return results
    
    def get_pinned_notes(self) -> List[Note]:
        """Получение закрепленных заметок"""
        return [note for note in self.notes if note.pinned]
    
    def get_categories(self) -> List[str]:
        """Получение списка категорий"""
        return sorted(list(self.categories))
    
    def get_all_tags(self) -> List[str]:
        """Получение всех тегов"""
        return sorted(list(self.all_tags))
    
    def update_tags(self, note: Note):
        """Обновление глобального списка тегов"""
        self.all_tags.update(note.tags)
    
    def save_notes(self):
        """Сохранение заметок"""
        try:
            data = [note.to_dict() for note in self.notes]
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")
    
    def load_notes(self):
        """Загрузка заметок"""
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.notes = [Note.from_dict(item) for item in data]
                
                # Обновляем категории и теги
                for note in self.notes:
                    self.categories.add(note.category)
                    self.all_tags.update(note.tags)
                
                self.notes_loaded.emit(self.notes)
                
        except FileNotFoundError:
            self.notes = []
        except Exception as e:
            print(f"Ошибка загрузки заметок: {e}")
            self.notes = []
    
    def export_notes(self, filename: str):
        """Экспорт заметок в файл"""
        try:
            data = [note.to_dict() for note in self.notes]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка экспорта заметок: {e}")
            return False
    
    def import_notes(self, filename: str) -> int:
        """Импорт заметок из файла"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                imported = 0
                for item in data:
                    note = Note.from_dict(item)
                    # Проверяем дубликаты
                    if not any(n.id == note.id for n in self.notes):
                        self.notes.append(note)
                        self.categories.add(note.category)
                        self.all_tags.update(note.tags)
                        imported += 1
                
                self.save_notes()
                return imported
                
        except Exception as e:
            print(f"Ошибка импорта заметок: {e}")
            return 0
    
    def get_stats(self) -> Dict:
        """Получение статистики заметок"""
        return {
            "total": len(self.notes),
            "categories": len(self.categories),
            "tags": len(self.all_tags),
            "pinned": len(self.get_pinned_notes())
        }