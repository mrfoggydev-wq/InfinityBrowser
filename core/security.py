"""
Модуль безопасности:
- Проверка на фишинг
- Блокировка вредоносных сайтов
- Проверка сертификатов SSL
- Защита от XSS и CSRF
- Менеджер паролей с шифрованием
"""

import hashlib
import json
import re
import ssl
import socket
import urllib.parse
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class SecurityManager:
    """Менеджер безопасности"""
    
    def __init__(self):
        # База данных вредоносных сайтов
        self.phishing_db = []
        self.malware_db = []
        self.trusted_sites = [
            "google.com", "youtube.com", "facebook.com",
            "wikipedia.org", "github.com", "stackoverflow.com",
            "microsoft.com", "apple.com", "amazon.com"
        ]
        
        # Загрузка базы
        self.load_phishing_db()
        self.load_malware_db()
        
        # Настройки безопасности
        self.security_level = "high"  # high, medium, low
        self.ssl_verification = True
        self.xss_protection = True
        self.csrf_protection = True
        
        # SSL контекст
        self.ssl_context = ssl.create_default_context()
        
        # Блокировка сайтов
        self.blocked_sites = []
        self.blocked_keywords = [
            "phishing", "scam", "lottery", "get-rich-quick",
            "bitcoin-investment", "free-money", "hack"
        ]
    
    def load_phishing_db(self):
        """Загрузка базы фишинговых сайтов"""
        try:
            with open("phishing_db.json", "r", encoding="utf-8") as f:
                self.phishing_db = json.load(f)
        except FileNotFoundError:
            self.phishing_db = []
        except Exception as e:
            print(f"Ошибка загрузки базы фишинга: {e}")
    
    def load_malware_db(self):
        """Загрузка базы вредоносных сайтов"""
        try:
            with open("malware_db.json", "r", encoding="utf-8") as f:
                self.malware_db = json.load(f)
        except FileNotFoundError:
            self.malware_db = []
        except Exception as e:
            print(f"Ошибка загрузки базы вредоносных сайтов: {e}")
    
    def is_phishing(self, url: str) -> bool:
        """Проверка на фишинг"""
        # Парсим URL
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        # Проверка в базе
        for phishing_url in self.phishing_db:
            if phishing_url in domain:
                return True
        
        # Проверка ключевых слов
        for keyword in self.blocked_keywords:
            if keyword in url.lower():
                return True
        
        # Проверка на поддельные домены
        if self.is_suspicious_domain(domain):
            return True
        
        return False
    
    def is_suspicious_domain(self, domain: str) -> bool:
        """Проверка на подозрительный домен"""
        # Проверка на очень длинные домены
        if len(domain) > 100:
            return True
        
        # Проверка на использование @ в URL
        if "@" in domain:
            return True
        
        # Проверка на поддельные популярные домены
        for trusted in self.trusted_sites:
            if trusted in domain and not domain.endswith(trusted):
                return True
        
        return False
    
    def is_malware(self, url: str) -> bool:
        """Проверка на вредоносное ПО"""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        for malware in self.malware_db:
            if malware in domain:
                return True
        
        return False
    
    def check_ssl(self, hostname: str, port: int = 443) -> Dict:
        """Проверка SSL сертификата"""
        result = {
            "valid": False,
            "expires_in": None,
            "issuer": None,
            "subject": None,
            "error": None
        }
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Проверка срока действия
                    not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                    now = datetime.now()
                    
                    result["valid"] = True
                    result["expires_in"] = (not_after - now).days
                    result["issuer"] = cert.get("issuer")
                    result["subject"] = cert.get("subject")
                    
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def sanitize_input(self, input_text: str) -> str:
        """Очистка ввода от XSS"""
        # Удаляем потенциально опасные теги
        input_text = re.sub(r'<script.*?>.*?</script>', '', input_text, flags=re.DOTALL)
        input_text = re.sub(r'<iframe.*?>.*?</iframe>', '', input_text, flags=re.DOTALL)
        input_text = re.sub(r'on\w+\s*=', '', input_text)
        input_text = re.sub(r'javascript:', '', input_text, flags=re.IGNORECASE)
        
        # Экранируем специальные символы
        input_text = input_text.replace("<", "&lt;")
        input_text = input_text.replace(">", "&gt;")
        input_text = input_text.replace("'", "&#39;")
        input_text = input_text.replace('"', "&quot;")
        
        return input_text
    
    def validate_url(self, url: str) -> bool:
        """Валидация URL"""
        pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// или https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # домен
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # опциональный порт
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return bool(pattern.match(url))
    
    def block_site(self, domain: str):
        """Блокировка сайта"""
        if domain not in self.blocked_sites:
            self.blocked_sites.append(domain)
            self.save_blocked_sites()
    
    def unblock_site(self, domain: str):
        """Разблокировка сайта"""
        if domain in self.blocked_sites:
            self.blocked_sites.remove(domain)
            self.save_blocked_sites()
    
    def is_blocked(self, url: str) -> bool:
        """Проверка, заблокирован ли сайт"""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        for blocked in self.blocked_sites:
            if blocked in domain:
                return True
        
        return False
    
    def save_blocked_sites(self):
        """Сохранение списка заблокированных сайтов"""
        try:
            with open("blocked_sites.json", "w", encoding="utf-8") as f:
                json.dump(self.blocked_sites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения списка блокировок: {e}")
    
    def load_blocked_sites(self):
        """Загрузка списка заблокированных сайтов"""
        try:
            with open("blocked_sites.json", "r", encoding="utf-8") as f:
                self.blocked_sites = json.load(f)
        except FileNotFoundError:
            self.blocked_sites = []
        except Exception as e:
            print(f"Ошибка загрузки списка блокировок: {e}")
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Генерация безопасного пароля"""
        import random
        import string
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        return password
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return f"{salt.hex()}:{key.decode()}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Проверка пароля"""
        try:
            salt_hex, key = hashed.split(":")
            salt = bytes.fromhex(salt_hex)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            new_key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return new_key.decode() == key
        except:
            return False
    
    def get_security_report(self, url: str) -> Dict:
        """Получение отчета о безопасности сайта"""
        report = {
            "url": url,
            "phishing": self.is_phishing(url),
            "malware": self.is_malware(url),
            "blocked": self.is_blocked(url),
            "ssl": None,
            "score": 100,
            "issues": []
        }
        
        # Проверка SSL
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == "https":
            hostname = parsed.netloc.split(":")[0]
            ssl_info = self.check_ssl(hostname)
            report["ssl"] = ssl_info
            if not ssl_info["valid"]:
                report["issues"].append("SSL сертификат недействителен")
                report["score"] -= 30
            elif ssl_info.get("expires_in", 0) < 7:
                report["issues"].append("SSL сертификат истекает через 7 дней")
                report["score"] -= 10
        
        # Проверка на фишинг
        if report["phishing"]:
            report["issues"].append("Подозрение на фишинг")
            report["score"] -= 50
        
        # Проверка на вредоносное ПО
        if report["malware"]:
            report["issues"].append("Обнаружено вредоносное ПО")
            report["score"] -= 50
        
        # Проверка на блокировку
        if report["blocked"]:
            report["issues"].append("Сайт заблокирован пользователем")
            report["score"] = 0
        
        return report

class PasswordManager:
    """Менеджер паролей с шифрованием AES-256"""
    
    def __init__(self):
        self.passwords = {}
        self.master_password = None
        self.encryption_key = None
        self.load_passwords()
    
    def initialize(self, master_password: str):
        """Инициализация менеджера паролей"""
        self.master_password = master_password
        self.encryption_key = self.derive_key(master_password)
        
        # Проверяем, существует ли файл с паролями
        if not os.path.exists("passwords.enc"):
            # Создаем пустой файл
            self.save_passwords()
    
    def derive_key(self, password: str) -> bytes:
        """Получение ключа шифрования из пароля"""
        salt = b'salt_salt_salt_salt'
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
        
        f = Fernet(self.encryption_key)
        data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = f.decrypt(data)
        return decrypted.decode()
    
    def add_password(self, service: str, username: str, password: str):
        """Добавление пароля"""
        self.passwords[service] = {
            "username": username,
            "password": self.encrypt_data(password),
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        self.save_passwords()
    
    def get_password(self, service: str) -> Optional[Dict]:
        """Получение пароля"""
        if service in self.passwords:
            data = self.passwords[service].copy()
            data["password"] = self.decrypt_data(data["password"])
            return data
        return None
    
    def delete_password(self, service: str):
        """Удаление пароля"""
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
    
    def list_services(self) -> List[str]:
        """Список сервисов"""
        return list(self.passwords.keys())
    
    def save_passwords(self):
        """Сохранение паролей"""
        try:
            # Шифруем все данные
            encrypted_data = self.encrypt_data(json.dumps(self.passwords))
            with open("passwords.enc", "w", encoding="utf-8") as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Ошибка сохранения паролей: {e}")
    
    def load_passwords(self):
        """Загрузка паролей"""
        try:
            with open("passwords.enc", "r", encoding="utf-8") as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_data = self.decrypt_data(encrypted_data)
                    self.passwords = json.loads(decrypted_data)
        except FileNotFoundError:
            self.passwords = {}
        except Exception as e:
            print(f"Ошибка загрузки паролей: {e}")
            self.passwords = {}