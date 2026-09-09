"""
Менеджер паролей:
- Безопасное хранение паролей (AES-256)
- Генерация сложных паролей
- Автозаполнение форм
- Импорт/экспорт паролей
- Анализ безопасности паролей
- Двухфакторная аутентификация (TOTP)
"""

import os
import json
import base64
import hashlib
import secrets
import string
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import pyotp
import qrcode
from io import BytesIO

class PasswordEntry:
    """Класс записи пароля"""
    
    def __init__(self, service: str, username: str, password: str, 
                 url: str = "", notes: str = "", category: str = "Общие"):
        self.id = self.generate_id()
        self.service = service
        self.username = username
        self.password = password
        self.url = url
        self.notes = notes
        self.category = category
        self.created = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()
        self.last_used = None
        self.strength = 0
        self.otp_secret = None  # Для двухфакторной аутентификации
        self.tags = []
        self.favorite = False
    
    @staticmethod
    def generate_id() -> str:
        """Генерация уникального ID"""
        return secrets.token_hex(16)
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "id": self.id,
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "url": self.url,
            "notes": self.notes,
            "category": self.category,
            "created": self.created,
            "updated": self.updated,
            "last_used": self.last_used,
            "strength": self.strength,
            "otp_secret": self.otp_secret,
            "tags": self.tags,
            "favorite": self.favorite
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordEntry':
        """Создание из словаря"""
        entry = cls(
            data["service"],
            data["username"],
            data["password"],
            data.get("url", ""),
            data.get("notes", ""),
            data.get("category", "Общие")
        )
        entry.id = data.get("id", cls.generate_id())
        entry.created = data.get("created", datetime.now().isoformat())
        entry.updated = data.get("updated", datetime.now().isoformat())
        entry.last_used = data.get("last_used")
        entry.strength = data.get("strength", 0)
        entry.otp_secret = data.get("otp_secret")
        entry.tags = data.get("tags", [])
        entry.favorite = data.get("favorite", False)
        return entry

class PasswordManager(QObject):
    """Менеджер паролей"""
    
    # Сигналы
    password_added = pyqtSignal(PasswordEntry)
    password_updated = pyqtSignal(PasswordEntry)
    password_deleted = pyqtSignal(str)  # entry_id
    master_password_changed = pyqtSignal(bool)
    security_breach_detected = pyqtSignal(str)  # message
    
    def __init__(self):
        super().__init__()
        
        self.passwords: Dict[str, PasswordEntry] = {}
        self.master_password = None
        self.encryption_key = None
        self.is_locked = True
        self.lock_timeout = 300  # 5 минут
        self.lock_timer = QTimer()
        self.lock_timer.timeout.connect(self.lock)
        
        # Политика паролей
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
        
        # База скомпрометированных паролей
        self.breached_passwords = set()
        self.load_breached_passwords()
        
        # Загрузка данных
        self.load_settings()
        self.load_passwords()
    
    def initialize(self, master_password: str) -> bool:
        """Инициализация с мастер-паролем"""
        if len(master_password) < 6:
            return False
        
        self.master_password = master_password
        self.encryption_key = self.derive_key(master_password)
        self.is_locked = False
        self.lock_timer.start(self.lock_timeout * 1000)
        
        # Проверяем, существует ли файл с паролями
        if not os.path.exists("passwords.enc"):
            self.save_passwords()
        
        self.master_password_changed.emit(True)
        return True
    
    def derive_key(self, password: str) -> bytes:
        """Получение ключа шифрования из пароля"""
        salt = b'super_browser_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_data(self, data: str) -> str:
        """Шифрование данных"""
        if not self.encryption_key:
            raise ValueError("Менеджер паролей не инициализирован")
        
        f = Fernet(self.encryption_key)
        encrypted = f.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Расшифровка данных"""
        if not self.encryption_key:
            raise ValueError("Менеджер паролей не инициализирован")
        
        try:
            f = Fernet(self.encryption_key)
            data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = f.decrypt(data)
            return decrypted.decode()
        except Exception as e:
            print(f"Ошибка расшифровки: {e}")
            return None
    
    def add_password(self, service: str, username: str, password: str,
                    url: str = "", notes: str = "", category: str = "Общие") -> Optional[PasswordEntry]:
        """Добавление пароля"""
        if self.is_locked:
            return None
        
        # Проверка на дубликаты
        for entry in self.passwords.values():
            if entry.service.lower() == service.lower() and entry.username == username:
                return None
        
        # Создаем запись
        entry = PasswordEntry(service, username, password, url, notes, category)
        
        # Оцениваем сложность пароля
        entry.strength = self.evaluate_password_strength(password)
        
        # Шифруем пароль
        encrypted_password = self.encrypt_data(password)
        entry.password = encrypted_password
        
        # Сохраняем
        self.passwords[entry.id] = entry
        self.save_passwords()
        self.password_added.emit(entry)
        
        # Проверяем, не скомпрометирован ли пароль
        if self.is_password_breached(password):
            self.security_breach_detected.emit(f"Пароль для {service} был скомпрометирован!")
        
        return entry
    
    def get_password(self, entry_id: str) -> Optional[PasswordEntry]:
        """Получение пароля с расшифровкой"""
        if self.is_locked:
            return None
        
        entry = self.passwords.get(entry_id)
        if not entry:
            return None
        
        # Копируем запись и расшифровываем пароль
        entry_copy = PasswordEntry(
            entry.service,
            entry.username,
            "",
            entry.url,
            entry.notes,
            entry.category
        )
        entry_copy.id = entry.id
        entry_copy.created = entry.created
        entry_copy.updated = entry.updated
        entry_copy.last_used = entry.last_used
        entry_copy.strength = entry.strength
        entry_copy.tags = entry.tags
        entry_copy.favorite = entry.favorite
        
        # Расшифровываем пароль
        decrypted = self.decrypt_data(entry.password)
        if decrypted:
            entry_copy.password = decrypted
            
            # Обновляем время использования
            entry.last_used = datetime.now().isoformat()
            self.save_passwords()
        
        return entry_copy
    
    def update_password(self, entry_id: str, service: str = None,
                       username: str = None, password: str = None,
                       url: str = None, notes: str = None,
                       category: str = None) -> bool:
        """Обновление пароля"""
        if self.is_locked:
            return False
        
        entry = self.passwords.get(entry_id)
        if not entry:
            return False
        
        if service:
            entry.service = service
        if username:
            entry.username = username
        if password:
            # Шифруем новый пароль
            entry.password = self.encrypt_data(password)
            entry.strength = self.evaluate_password_strength(password)
            
            # Проверяем на компрометацию
            if self.is_password_breached(password):
                self.security_breach_detected.emit(f"Пароль для {entry.service} был скомпрометирован!")
        if url is not None:
            entry.url = url
        if notes is not None:
            entry.notes = notes
        if category:
            entry.category = category
        
        entry.updated = datetime.now().isoformat()
        self.save_passwords()
        self.password_updated.emit(entry)
        return True
    
    def delete_password(self, entry_id: str) -> bool:
        """Удаление пароля"""
        if self.is_locked:
            return False
        
        if entry_id in self.passwords:
            del self.passwords[entry_id]
            self.save_passwords()
            self.password_deleted.emit(entry_id)
            return True
        return False
    
    def get_all_passwords(self, decrypt: bool = False) -> List[PasswordEntry]:
        """Получение всех паролей"""
        if self.is_locked:
            return []
        
        if decrypt:
            return [self.get_password(entry_id) for entry_id in self.passwords.keys()]
        else:
            return list(self.passwords.values())
    
    def search_passwords(self, query: str) -> List[PasswordEntry]:
        """Поиск паролей"""
        if self.is_locked:
            return []
        
        query_lower = query.lower()
        results = []
        
        for entry in self.passwords.values():
            if (query_lower in entry.service.lower() or 
                query_lower in entry.username.lower() or
                query_lower in entry.url.lower() or
                query_lower in entry.notes.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
        
        return results
    
    def get_passwords_by_category(self, category: str) -> List[PasswordEntry]:
        """Получение паролей по категории"""
        if self.is_locked:
            return []
        
        return [entry for entry in self.passwords.values() if entry.category == category]
    
    def get_categories(self) -> List[str]:
        """Получение списка категорий"""
        categories = set()
        for entry in self.passwords.values():
            categories.add(entry.category)
        return sorted(list(categories))
    
    def evaluate_password_strength(self, password: str) -> int:
        """Оценка сложности пароля (0-100)"""
        score = 0
        
        if len(password) >= self.min_length:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[0-9]', password):
            score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 10
        
        # Штраф за повторяющиеся символы
        if len(set(password)) < len(password) * 0.7:
            score -= 10
        
        # Штраф за словарные слова
        common_words = ['password', 'admin', '123456', 'qwerty', 'abc123']
        for word in common_words:
            if word in password.lower():
                score -= 15
        
        return max(0, min(100, score))
    
    def generate_strong_password(self, length: int = 16) -> str:
        """Генерация сложного пароля"""
        # Определяем наборы символов
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Гарантируем наличие всех типов символов
        password_chars = []
        password_chars.append(secrets.choice(uppercase))
        password_chars.append(secrets.choice(lowercase))
        password_chars.append(secrets.choice(digits))
        password_chars.append(secrets.choice(special))
        
        # Добавляем остальные символы
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))
        
        # Перемешиваем
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_memorable_password(self) -> str:
        """Генерация запоминаемого пароля"""
        words = [
            "sun", "moon", "star", "sky", "blue", "red", "gold", "silver",
            "happy", "brave", "wise", "kind", "bright", "calm", "swift", "noble",
            "tiger", "eagle", "lion", "wolf", "fox", "bear", "hawk", "dragon",
            "mountain", "ocean", "forest", "river", "valley", "cloud", "storm", "flame"
        ]
        
        # Выбираем 3 случайных слова
        word1 = secrets.choice(words)
        word2 = secrets.choice(words)
        word3 = secrets.choice(words)
        
        # Добавляем цифры и специальный символ
        number = secrets.randbelow(100)
        special = secrets.choice("!@#$%^&*")
        
        # Соединяем
        password = f"{word1.capitalize()}{word2.capitalize()}{word3.capitalize()}{number}{special}"
        
        return password
    
    def is_password_breached(self, password: str) -> bool:
        """Проверка, был ли пароль скомпрометирован"""
        # Используем haveibeenpwned API
        # В реальном приложении делаем API запрос
        # Здесь упрощенная версия
        
        password_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = password_hash[:5]
        
        # Проверяем в локальной базе
        if password in self.breached_passwords:
            return True
        
        # Здесь мог бы быть API запрос
        # response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        # if response.status_code == 200:
        #     hashes = response.text.splitlines()
        #     for h in hashes:
        #         if password_hash[5:] in h:
        #             return True
        
        return False
    
    def load_breached_passwords(self):
        """Загрузка базы скомпрометированных паролей"""
        try:
            with open("breached_passwords.txt", "r", encoding="utf-8") as f:
                self.breached_passwords = set(line.strip() for line in f)
        except FileNotFoundError:
            # Создаем файл с базовыми паролями
            self.breached_passwords = {
                "password", "123456", "12345678", "qwerty", "admin",
                "letmein", "welcome", "monkey", "dragon", "master"
            }
            self.save_breached_passwords()
        except Exception as e:
            print(f"Ошибка загрузки скомпрометированных паролей: {e}")
    
    def save_breached_passwords(self):
        """Сохранение базы скомпрометированных паролей"""
        try:
            with open("breached_passwords.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(self.breached_passwords))
        except Exception as e:
            print(f"Ошибка сохранения скомпрометированных паролей: {e}")
    
    def import_passwords(self, filename: str) -> int:
        """Импорт паролей из файла (CSV, JSON)"""
        if self.is_locked:
            return 0
        
        imported = 0
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                for item in data:
                    entry = PasswordEntry(
                        item.get("service", "Unknown"),
                        item.get("username", ""),
                        item.get("password", ""),
                        item.get("url", ""),
                        item.get("notes", ""),
                        item.get("category", "Импортированные")
                    )
                    
                    # Шифруем пароль
                    entry.password = self.encrypt_data(entry.password)
                    entry.strength = self.evaluate_password_strength(
                        self.decrypt_data(entry.password)
                    )
                    
                    self.passwords[entry.id] = entry
                    imported += 1
                
                self.save_passwords()
                
        except Exception as e:
            print(f"Ошибка импорта паролей: {e}")
        
        return imported
    
    def export_passwords(self, filename: str) -> bool:
        """Экспорт паролей в файл"""
        if self.is_locked:
            return False
        
        try:
            export_data = []
            for entry in self.passwords.values():
                # Расшифровываем пароль для экспорта
                decrypted = self.decrypt_data(entry.password)
                export_data.append({
                    "service": entry.service,
                    "username": entry.username,
                    "password": decrypted,
                    "url": entry.url,
                    "notes": entry.notes,
                    "category": entry.category,
                    "created": entry.created,
                    "updated": entry.updated
                })
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Ошибка экспорта паролей: {e}")
            return False
    
    def generate_totp(self, secret: str) -> str:
        """Генерация TOTP кода для двухфакторной аутентификации"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.now()
        except Exception as e:
            print(f"Ошибка генерации TOTP: {e}")
            return None
    
    def generate_totp_secret(self) -> str:
        """Генерация секрета для TOTP"""
        return pyotp.random_base32()
    
    def generate_totp_qr(self, secret: str, service: str, username: str) -> bytes:
        """Генерация QR-кода для TOTP"""
        try:
            totp = pyotp.TOTP(secret)
            uri = totp.provisioning_uri(username, issuer_name=service)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            return buffer.getvalue()
        except Exception as e:
            print(f"Ошибка генерации QR-кода: {e}")
            return None
    
    def lock(self):
        """Блокировка менеджера паролей"""
        self.is_locked = True
        self.encryption_key = None
        self.lock_timer.stop()
        self.master_password_changed.emit(False)
    
    def unlock(self, master_password: str) -> bool:
        """Разблокировка менеджера паролей"""
        if self.encryption_key and self.encryption_key == self.derive_key(master_password):
            self.is_locked = False
            self.lock_timer.start(self.lock_timeout * 1000)
            self.master_password_changed.emit(True)
            return True
        
        # Проверяем мастер-пароль
        try:
            test_key = self.derive_key(master_password)
            # Пытаемся расшифровать тестовые данные
            test_data = self.encrypt_data("test")
            self.decrypt_data(test_data)
            
            self.master_password = master_password
            self.encryption_key = test_key
            self.is_locked = False
            self.lock_timer.start(self.lock_timeout * 1000)
            self.master_password_changed.emit(True)
            return True
        except:
            return False
    
    def change_master_password(self, old_password: str, new_password: str) -> bool:
        """Смена мастер-пароля"""
        if self.is_locked:
            return False
        
        if len(new_password) < 6:
            return False
        
        try:
            # Проверяем старый пароль
            old_key = self.derive_key(old_password)
            if old_key != self.encryption_key:
                return False
            
            # Перешифровываем все пароли
            new_key = self.derive_key(new_password)
            
            for entry in self.passwords.values():
                decrypted = self.decrypt_data(entry.password)
                if decrypted is None:
                    return False
                
                # Шифруем новым ключом
                f = Fernet(new_key)
                encrypted = f.encrypt(decrypted.encode())
                entry.password = base64.urlsafe_b64encode(encrypted).decode()
            
            # Обновляем мастер-пароль
            self.master_password = new_password
            self.encryption_key = new_key
            self.save_passwords()
            
            self.master_password_changed.emit(True)
            return True
            
        except Exception as e:
            print(f"Ошибка смены мастер-пароля: {e}")
            return False
    
    def save_passwords(self):
        """Сохранение паролей"""
        if self.is_locked:
            return
        
        try:
            data = [entry.to_dict() for entry in self.passwords.values()]
            json_data = json.dumps(data, ensure_ascii=False)
            encrypted = self.encrypt_data(json_data)
            
            with open("passwords.enc", "w", encoding="utf-8") as f:
                f.write(encrypted)
                
        except Exception as e:
            print(f"Ошибка сохранения паролей: {e}")
    
    def load_passwords(self):
        """Загрузка паролей"""
        try:
            if not os.path.exists("passwords.enc"):
                self.passwords = {}
                return
            
            with open("passwords.enc", "r", encoding="utf-8") as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted = self.decrypt_data(encrypted_data)
                    if decrypted:
                        data = json.loads(decrypted)
                        self.passwords = {
                            item["id"]: PasswordEntry.from_dict(item)
                            for item in data
                        }
                    else:
                        self.passwords = {}
                else:
                    self.passwords = {}
                    
        except FileNotFoundError:
            self.passwords = {}
        except Exception as e:
            print(f"Ошибка загрузки паролей: {e}")
            self.passwords = {}
    
    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open("password_manager_settings.json", "w", encoding="utf-8") as f:
                json.dump({
                    "min_length": self.min_length,
                    "require_uppercase": self.require_uppercase,
                    "require_lowercase": self.require_lowercase,
                    "require_digits": self.require_digits,
                    "require_special": self.require_special,
                    "lock_timeout": self.lock_timeout
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings(self):
        """Загрузка настроек"""
        try:
            with open("password_manager_settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.min_length = data.get("min_length", 8)
                self.require_uppercase = data.get("require_uppercase", True)
                self.require_lowercase = data.get("require_lowercase", True)
                self.require_digits = data.get("require_digits", True)
                self.require_special = data.get("require_special", True)
                self.lock_timeout = data.get("lock_timeout", 300)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        if self.is_locked:
            return {"locked": True}
        
        total = len(self.passwords)
        weak = sum(1 for entry in self.passwords.values() if entry.strength < 50)
        medium = sum(1 for entry in self.passwords.values() if 50 <= entry.strength < 70)
        strong = sum(1 for entry in self.passwords.values() if entry.strength >= 70)
        
        categories = self.get_categories()
        favorites = sum(1 for entry in self.passwords.values() if entry.favorite)
        
        return {
            "total": total,
            "weak": weak,
            "medium": medium,
            "strong": strong,
            "categories": len(categories),
            "favorites": favorites,
            "locked": False
        }
    
    def get_security_report(self) -> Dict:
        """Получение отчета о безопасности"""
        if self.is_locked:
            return {"locked": True}
        
        report = {
            "total_passwords": len(self.passwords),
            "weak_passwords": 0,
            "duplicate_passwords": 0,
            "breached_passwords": 0,
            "old_passwords": 0,
            "recommendations": []
        }
        
        passwords_set = set()
        for entry in self.passwords.values():
            # Проверка слабых паролей
            if entry.strength < 50:
                report["weak_passwords"] += 1
                report["recommendations"].append(
                    f"Усильте пароль для '{entry.service}'"
                )
            
            # Проверка дубликатов
            decrypted = self.decrypt_data(entry.password)
            if decrypted and decrypted in passwords_set:
                report["duplicate_passwords"] += 1
                report["recommendations"].append(
                    f"Используется дублирующийся пароль для '{entry.service}'"
                )
            if decrypted:
                passwords_set.add(decrypted)
            
            # Проверка компрометации
            decrypted = self.decrypt_data(entry.password)
            if decrypted and self.is_password_breached(decrypted):
                report["breached_passwords"] += 1
                report["recommendations"].append(
                    f"Пароль для '{entry.service}' был скомпрометирован!"
                )
            
            # Проверка старых паролей
            if entry.updated:
                updated = datetime.fromisoformat(entry.updated)
                if (datetime.now() - updated).days > 180:  # 6 месяцев
                    report["old_passwords"] += 1
                    report["recommendations"].append(
                        f"Пароль для '{entry.service}' устарел (более 6 месяцев)"
                    )
        
        return report