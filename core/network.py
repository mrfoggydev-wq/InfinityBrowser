"""
Сетевой менеджер:
- HTTP/HTTPS запросы
- Прокси-сервер (HTTP, SOCKS5)
- VPN-клиент
- Сниффер трафика
- Управление куками
- Кэширование
"""

import json
import requests
import socket
import socks
import urllib.parse
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
import threading
import queue
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class NetworkManager(QObject):
    """Главный сетевой менеджер"""
    
    # Сигналы
    request_sent = pyqtSignal(str, str)  # url, method
    request_received = pyqtSignal(str, int)  # url, status_code
    proxy_changed = pyqtSignal(str, int)  # host, port
    vpn_status_changed = pyqtSignal(bool)  # connected
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        
        # Настройки сети
        self.user_agent = "SuperBrowser/4.0.0"
        self.timeout = 30
        self.max_redirects = 10
        self.verify_ssl = True
        
        # Прокси
        self.proxy_enabled = False
        self.proxy_host = None
        self.proxy_port = None
        self.proxy_type = "http"  # http, socks5
        
        # VPN
        self.vpn_enabled = False
        self.vpn_config = None
        
        # Сниффер
        self.sniffer_enabled = False
        self.sniffer_queue = queue.Queue()
        self.sniffer_thread = None
        
        # Кэш
        self.cache_enabled = True
        self.cache_size = 100  # МБ
        self.cache_dir = "./cache"
        
        # Статистика
        self.stats = {
            "requests_sent": 0,
            "requests_received": 0,
            "bytes_downloaded": 0,
            "bytes_uploaded": 0,
            "failed_requests": 0
        }
        
        # Загрузка настроек
        self.load_settings()
        
        # Создание кэша
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def load_settings(self):
        """Загрузка настроек"""
        self.proxy_enabled = self.settings.value("proxy_enabled", False, type=bool)
        self.proxy_host = self.settings.value("proxy_host", "")
        self.proxy_port = self.settings.value("proxy_port", 8080, type=int)
        self.proxy_type = self.settings.value("proxy_type", "http")
        self.vpn_enabled = self.settings.value("vpn_enabled", False, type=bool)
        self.cache_enabled = self.settings.value("cache_enabled", True, type=bool)
        
        if self.proxy_enabled and self.proxy_host:
            self.set_proxy(self.proxy_host, self.proxy_port, self.proxy_type)
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Универсальный HTTP запрос"""
        self.stats["requests_sent"] += 1
        self.request_sent.emit(url, method)
        
        # Подготовка заголовков
        headers = kwargs.get("headers", {})
        headers["User-Agent"] = self.user_agent
        
        # Настройка прокси
        proxies = None
        if self.proxy_enabled and self.proxy_host:
            proxy_url = f"{self.proxy_type}://{self.proxy_host}:{self.proxy_port}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
        
        try:
            # Отправка запроса
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                proxies=proxies,
                allow_redirects=self.max_redirects > 0,
                **kwargs
            )
            
            # Обновление статистики
            self.stats["requests_received"] += 1
            self.stats["bytes_downloaded"] += len(response.content)
            self.stats["bytes_uploaded"] += len(str(response.request.body or ""))
            
            self.request_received.emit(url, response.status_code)
            
            # Кэширование GET запросов
            if self.cache_enabled and method.upper() == "GET" and response.status_code == 200:
                self.cache_response(url, response)
            
            return response
            
        except Exception as e:
            self.stats["failed_requests"] += 1
            raise
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET запрос с кэшированием"""
        # Проверка кэша
        if self.cache_enabled:
            cached = self.get_cached_response(url)
            if cached:
                return cached
        
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, data=None, json=None, **kwargs) -> requests.Response:
        """POST запрос"""
        return self.request("POST", url, data=data, json=json, **kwargs)
    
    def head(self, url: str, **kwargs) -> requests.Response:
        """HEAD запрос"""
        return self.request("HEAD", url, **kwargs)
    
    def options(self, url: str, **kwargs) -> requests.Response:
        """OPTIONS запрос"""
        return self.request("OPTIONS", url, **kwargs)
    
    def put(self, url: str, data=None, **kwargs) -> requests.Response:
        """PUT запрос"""
        return self.request("PUT", url, data=data, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE запрос"""
        return self.request("DELETE", url, **kwargs)
    
    def set_proxy(self, host: str, port: int, proxy_type: str = "http"):
        """Установка прокси"""
        self.proxy_host = host
        self.proxy_port = port
        self.proxy_type = proxy_type
        self.proxy_enabled = True
        
        self.proxy_changed.emit(host, port)
        self.save_settings()
    
    def disable_proxy(self):
        """Отключение прокси"""
        self.proxy_enabled = False
        self.proxy_host = None
        self.proxy_port = None
        self.save_settings()
    
    def set_vpn(self, config: Dict):
        """Настройка VPN"""
        self.vpn_config = config
        self.vpn_enabled = True
        self.vpn_status_changed.emit(True)
        self.save_settings()
        
        # Подключение VPN
        self.connect_vpn()
    
    def connect_vpn(self):
        """Подключение VPN"""
        if not self.vpn_config:
            return
        
        # Здесь код для подключения к VPN
        # Используем OpenVPN, WireGuard или свой протокол
        print(f"Подключение к VPN: {self.vpn_config.get('server')}")
        
        # Эмуляция подключения
        QTimer.singleShot(2000, lambda: self.vpn_status_changed.emit(True))
    
    def disconnect_vpn(self):
        """Отключение VPN"""
        self.vpn_enabled = False
        self.vpn_status_changed.emit(False)
        self.save_settings()
    
    def enable_sniffer(self):
        """Включение сниффера трафика"""
        if self.sniffer_enabled:
            return
        
        self.sniffer_enabled = True
        self.sniffer_thread = threading.Thread(target=self.sniffer_loop, daemon=True)
        self.sniffer_thread.start()
    
    def disable_sniffer(self):
        """Отключение сниффера"""
        self.sniffer_enabled = False
        if self.sniffer_thread:
            self.sniffer_thread.join(timeout=1)
            self.sniffer_thread = None
    
    def sniffer_loop(self):
        """Цикл сниффера"""
        while self.sniffer_enabled:
            try:
                # Сниффинг трафика
                # Здесь код для перехвата пакетов
                time.sleep(1)
            except Exception as e:
                print(f"Ошибка сниффера: {e}")
    
    def cache_response(self, url: str, response: requests.Response):
        """Кэширование ответа"""
        if not self.cache_enabled:
            return
        
        # Создаем хэш URL
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{url_hash}.cache")
        
        try:
            cache_data = {
                "url": url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content.decode('utf-8', errors='ignore'),
                "timestamp": datetime.now().isoformat()
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка кэширования: {e}")
    
    def get_cached_response(self, url: str) -> Optional[requests.Response]:
        """Получение кэшированного ответа"""
        if not self.cache_enabled:
            return None
        
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{url_hash}.cache")
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            # Проверка на устаревание (24 часа)
            timestamp = datetime.fromisoformat(cache_data["timestamp"])
            if (datetime.now() - timestamp).total_seconds() > 86400:
                os.remove(cache_file)
                return None
            
            # Создаем объект ответа
            response = requests.Response()
            response.status_code = cache_data["status_code"]
            response.headers = cache_data["headers"]
            response._content = cache_data["content"].encode('utf-8')
            response.url = url
            
            return response
            
        except Exception as e:
            print(f"Ошибка загрузки кэша: {e}")
            return None
    
    def clear_cache(self):
        """Очистка кэша"""
        for file in os.listdir(self.cache_dir):
            if file.endswith(".cache"):
                os.remove(os.path.join(self.cache_dir, file))
    
    def get_cookies(self, url: str) -> List[Dict]:
        """Получение cookies для URL"""
        # Используем requests для получения cookies
        response = self.head(url)
        cookies = []
        for cookie in response.cookies:
            cookies.append({
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "expires": cookie.expires
            })
        return cookies
    
    def save_settings(self):
        """Сохранение настроек"""
        self.settings.setValue("proxy_enabled", self.proxy_enabled)
        self.settings.setValue("proxy_host", self.proxy_host)
        self.settings.setValue("proxy_port", self.proxy_port)
        self.settings.setValue("proxy_type", self.proxy_type)
        self.settings.setValue("vpn_enabled", self.vpn_enabled)
        self.settings.setValue("cache_enabled", self.cache_enabled)
        self.settings.sync()
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        return self.stats
    
    def reset_stats(self):
        """Сброс статистики"""
        for key in self.stats:
            self.stats[key] = 0