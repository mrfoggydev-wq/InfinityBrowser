"""
Управление профилями пользователей:
- Создание/удаление профилей
- Переключение между профилями
- Синхронизация настроек
- Резервное копирование
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from PyQt5.QtCore import QObject, pyqtSignal

class Profile:
    """Класс профиля пользователя"""
    
    def __init__(self, name: str, avatar: str = None):
        self.name = name
        self.avatar = avatar or "👤"
        self.created = datetime.now().isoformat()
        self.last_used = datetime.now().isoformat()
        
        # Настройки профиля
        self.settings = {
            "home_page": "https://www.google.com",
            "theme": "dark",
            "zoom_factor": 1.0,
            "adblock_enabled": True,
            "language": "ru",
            "download_dir": "~/Downloads",
            "startup_pages": [],
            "search_engine": "google"
        }
        
        # Данные профиля
        self.bookmarks = []
        self.history = []
        self.passwords = []
        self.cookies = []
        self.extensions = []
        
        # Путь к профилю
        self.profile_dir = None
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "name": self.name,
            "avatar": self.avatar,
            "created": self.created,
            "last_used": self.last_used,
            "settings": self.settings,
            "bookmarks": self.bookmarks,
            "history": self.history,
            "passwords": self.passwords,
            "cookies": self.cookies,
            "extensions": self.extensions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Profile':
        """Создание профиля из словаря"""
        profile = cls(data["name"], data.get("avatar", "👤"))
        profile.created = data.get("created", datetime.now().isoformat())
        profile.last_used = data.get("last_used", datetime.now().isoformat())
        profile.settings.update(data.get("settings", {}))
        profile.bookmarks = data.get("bookmarks", [])
        profile.history = data.get("history", [])
        profile.passwords = data.get("passwords", [])
        profile.cookies = data.get("cookies", [])
        profile.extensions = data.get("extensions", [])
        return profile

class ProfileManager(QObject):
    """Менеджер профилей"""
    
    # Сигналы
    profile_created = pyqtSignal(Profile)
    profile_deleted = pyqtSignal(str)  # profile_name
    profile_switched = pyqtSignal(Profile)
    profile_updated = pyqtSignal(Profile)
    
    def __init__(self):
        super().__init__()
        
        self.profiles: Dict[str, Profile] = {}
        self.current_profile: Optional[Profile] = None
        self.profiles_dir = "./profiles"
        
        # Создаем директорию для профилей
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Загружаем профили
        self.load_profiles()
        
        # Если нет профилей, создаем дефолтный
        if not self.profiles:
            self.create_profile("Default")
    
    def create_profile(self, name: str, avatar: str = None) -> Profile:
        """Создание нового профиля"""
        if name in self.profiles:
            return None
        
        profile = Profile(name, avatar)
        self.profiles[name] = profile
        
        # Создаем директорию профиля
        profile.profile_dir = os.path.join(self.profiles_dir, name)
        os.makedirs(profile.profile_dir, exist_ok=True)
        
        # Сохраняем профиль
        self.save_profile(profile)
        self.profile_created.emit(profile)
        
        # Делаем текущим
        self.switch_profile(name)
        
        return profile
    
    def delete_profile(self, name: str) -> bool:
        """Удаление профиля"""
        if name not in self.profiles:
            return False
        
        if name == "Default" and len(self.profiles) == 1:
            return False  # Нельзя удалить последний профиль
        
        # Удаляем директорию
        profile_dir = os.path.join(self.profiles_dir, name)
        if os.path.exists(profile_dir):
            shutil.rmtree(profile_dir)
        
        # Удаляем из списка
        del self.profiles[name]
        self.profile_deleted.emit(name)
        
        # Если удалили текущий, переключаемся на другой
        if self.current_profile and self.current_profile.name == name:
            if self.profiles:
                self.switch_profile(next(iter(self.profiles)))
            else:
                self.current_profile = None
        
        return True
    
    def switch_profile(self, name: str) -> bool:
        """Переключение на другой профиль"""
        if name not in self.profiles:
            return False
        
        # Сохраняем текущий профиль
        if self.current_profile:
            self.save_profile(self.current_profile)
        
        # Загружаем новый профиль
        profile = self.profiles[name]
        self.load_profile_data(profile)
        self.current_profile = profile
        
        profile.last_used = datetime.now().isoformat()
        self.profile_switched.emit(profile)
        
        return True
    
    def load_profile_data(self, profile: Profile):
        """Загрузка данных профиля"""
        profile_dir = os.path.join(self.profiles_dir, profile.name)
        
        # Загружаем настройки
        settings_file = os.path.join(profile_dir, "settings.json")
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    profile.settings.update(data)
            except:
                pass
        
        # Загружаем закладки
        bookmarks_file = os.path.join(profile_dir, "bookmarks.json")
        if os.path.exists(bookmarks_file):
            try:
                with open(bookmarks_file, "r", encoding="utf-8") as f:
                    profile.bookmarks = json.load(f)
            except:
                profile.bookmarks = []
        
        # Загружаем историю
        history_file = os.path.join(profile_dir, "history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    profile.history = json.load(f)
            except:
                profile.history = []
        
        # Загружаем пароли
        passwords_file = os.path.join(profile_dir, "passwords.json")
        if os.path.exists(passwords_file):
            try:
                with open(passwords_file, "r", encoding="utf-8") as f:
                    profile.passwords = json.load(f)
            except:
                profile.passwords = []
        
        # Загружаем расширения
        extensions_file = os.path.join(profile_dir, "extensions.json")
        if os.path.exists(extensions_file):
            try:
                with open(extensions_file, "r", encoding="utf-8") as f:
                    profile.extensions = json.load(f)
            except:
                profile.extensions = []
    
    def save_profile(self, profile: Profile):
        """Сохранение данных профиля"""
        profile_dir = os.path.join(self.profiles_dir, profile.name)
        os.makedirs(profile_dir, exist_ok=True)
        
        # Сохраняем настройки
        settings_file = os.path.join(profile_dir, "settings.json")
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(profile.settings, f, ensure_ascii=False, indent=2)
        except:
            pass
        
        # Сохраняем закладки
        bookmarks_file = os.path.join(profile_dir, "bookmarks.json")
        try:
            with open(bookmarks_file, "w", encoding="utf-8") as f:
                json.dump(profile.bookmarks, f, ensure_ascii=False, indent=2)
        except:
            pass
        
        # Сохраняем историю
        history_file = os.path.join(profile_dir, "history.json")
        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(profile.history, f, ensure_ascii=False, indent=2)
        except:
            pass
        
        # Сохраняем пароли
        passwords_file = os.path.join(profile_dir, "passwords.json")
        try:
            with open(passwords_file, "w", encoding="utf-8") as f:
                json.dump(profile.passwords, f, ensure_ascii=False, indent=2)
        except:
            pass
        
        # Сохраняем расширения
        extensions_file = os.path.join(profile_dir, "extensions.json")
        try:
            with open(extensions_file, "w", encoding="utf-8") as f:
                json.dump(profile.extensions, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_profiles(self):
        """Загрузка всех профилей"""
        for item in os.listdir(self.profiles_dir):
            profile_dir = os.path.join(self.profiles_dir, item)
            if os.path.isdir(profile_dir):
                # Загружаем метаданные профиля
                meta_file = os.path.join(profile_dir, "meta.json")
                if os.path.exists(meta_file):
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            profile = Profile.from_dict(data)
                            self.profiles[profile.name] = profile
                            profile.profile_dir = profile_dir
                    except:
                        pass
    
    def export_profile(self, name: str, export_path: str) -> bool:
        """Экспорт профиля"""
        if name not in self.profiles:
            return False
        
        profile = self.profiles[name]
        self.save_profile(profile)
        
        # Создаем архив профиля
        profile_dir = os.path.join(self.profiles_dir, name)
        
        try:
            shutil.make_archive(export_path, 'zip', profile_dir)
            return True
        except Exception as e:
            print(f"Ошибка экспорта профиля: {e}")
            return False
    
    def import_profile(self, import_path: str) -> Optional[Profile]:
        """Импорт профиля"""
        try:
            # Распаковываем архив
            import shutil
            temp_dir = os.path.join(self.profiles_dir, "temp_import")
            shutil.unpack_archive(import_path, temp_dir, 'zip')
            
            # Загружаем метаданные
            meta_file = os.path.join(temp_dir, "meta.json")
            if not os.path.exists(meta_file):
                shutil.rmtree(temp_dir)
                return None
            
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Создаем профиль
            profile = Profile.from_dict(data)
            
            # Проверяем, существует ли уже такой профиль
            if profile.name in self.profiles:
                profile.name = f"{profile.name}_{datetime.now().strftime('%H%M%S')}"
            
            # Перемещаем данные
            profile_dir = os.path.join(self.profiles_dir, profile.name)
            shutil.move(temp_dir, profile_dir)
            profile.profile_dir = profile_dir
            
            # Сохраняем профиль
            self.profiles[profile.name] = profile
            self.profile_created.emit(profile)
            
            return profile
            
        except Exception as e:
            print(f"Ошибка импорта профиля: {e}")
            return None
    
    def get_profile_stats(self, name: str) -> Dict:
        """Получение статистики профиля"""
        if name not in self.profiles:
            return {}
        
        profile = self.profiles[name]
        
        return {
            "name": profile.name,
            "avatar": profile.avatar,
            "created": profile.created,
            "last_used": profile.last_used,
            "bookmarks_count": len(profile.bookmarks),
            "history_count": len(profile.history),
            "passwords_count": len(profile.passwords),
            "extensions_count": len(profile.extensions),
            "settings_count": len(profile.settings)
        }
    
    def get_all_profiles(self) -> List[Profile]:
        """Получение всех профилей"""
        return list(self.profiles.values())
    
    def get_current_profile(self) -> Optional[Profile]:
        """Получение текущего профиля"""
        return self.current_profile
    
    def sync_profile(self, name: str, cloud_provider: str = "google"):
        """Синхронизация профиля с облаком"""
        # Здесь код для синхронизации с облачными сервисами
        pass
    
    def backup_profile(self, name: str) -> str:
        """Создание резервной копии профиля"""
        profile = self.profiles.get(name)
        if not profile:
            return None
        
        backup_dir = os.path.join(self.profiles_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{name}_{timestamp}.zip")
        
        if self.export_profile(name, backup_file.replace('.zip', '')):
            return backup_file
        
        return None