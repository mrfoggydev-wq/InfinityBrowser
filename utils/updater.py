"""
Система автообновления:
- Проверка новых версий
- Загрузка обновлений
- Установка обновлений
- Откат к предыдущей версии
"""

import os
import sys
import json
import requests
import zipfile
import shutil
import tempfile
from datetime import datetime, timedelta
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class AutoUpdater(QObject):
    """Система автообновления"""
    
    # Сигналы
    update_available = pyqtSignal(str, str)  # version, size
    update_downloading = pyqtSignal(int)  # progress
    update_downloaded = pyqtSignal(str)  # filepath
    update_installing = pyqtSignal()
    update_installed = pyqtSignal()
    update_failed = pyqtSignal(str)  # error
    
    def __init__(self, current_version: str, parent_widget=None):
        super().__init__()
        
        self.current_version = current_version
        self.parent_widget = parent_widget
        self.update_url = "https://api.github.com/repos/superbrowser/superbrowser/releases/latest"
        self.download_url = None
        self.update_info = None
        self.update_file = None
        
        # Настройки
        self.check_interval = 86400  # 24 часа
        self.auto_download = False
        self.auto_install = False
        
        # Состояние
        self.last_check = None
        self.is_updating = False
        self.update_available_version = None
        
        # Загрузка настроек
        self.load_settings()
        
        # Таймер для проверки обновлений
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_updates)
        self.check_timer.start(self.check_interval * 1000)
    
    def check_updates(self, force: bool = False) -> bool:
        """Проверка наличия обновлений"""
        if self.is_updating:
            return False
        
        # Проверяем, не проверяли ли недавно
        if not force and self.last_check:
            if (datetime.now() - self.last_check).total_seconds() < self.check_interval:
                return False
        
        self.is_updating = True
        
        try:
            # Запрос к серверу
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Получаем версию
            latest_version = data.get("tag_name", "").lstrip("v")
            
            if self.compare_versions(latest_version, self.current_version) > 0:
                # Есть новая версия
                self.update_available_version = latest_version
                self.update_info = data
                
                # Получаем ссылку на загрузку
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".zip"):
                        self.download_url = asset["browser_download_url"]
                        size = asset["size"]
                        break
                
                if self.download_url:
                    self.update_available.emit(latest_version, self.format_size(size))
                    
                    if self.auto_download:
                        self.download_update()
                    
                    self.is_updating = False
                    return True
            
            self.last_check = datetime.now()
            self.is_updating = False
            return False
            
        except Exception as e:
            self.update_failed.emit(f"Ошибка проверки обновлений: {e}")
            self.is_updating = False
            return False
    
    def download_update(self):
        """Загрузка обновления"""
        if not self.download_url:
            self.update_failed.emit("Ссылка на загрузку не найдена")
            return
        
        self.is_updating = True
        
        try:
            # Загрузка файла
            response = requests.get(self.download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Создаем временный файл
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        self.update_downloading.emit(progress)
            
            temp_file.close()
            self.update_file = temp_file.name
            self.update_downloaded.emit(self.update_file)
            
            if self.auto_install:
                self.install_update()
            
            self.is_updating = False
            
        except Exception as e:
            self.update_failed.emit(f"Ошибка загрузки обновления: {e}")
            self.is_updating = False
    
    def install_update(self):
        """Установка обновления"""
        if not self.update_file or not os.path.exists(self.update_file):
            self.update_failed.emit("Файл обновления не найден")
            return
        
        self.is_updating = True
        self.update_installing.emit()
        
        try:
            # Создаем резервную копию
            backup_dir = "./backup"
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.copytree(".", backup_dir, ignore=shutil.ignore_patterns('backup', 'logs'))
            
            # Распаковываем обновление
            with zipfile.ZipFile(self.update_file, 'r') as zip_ref:
                zip_ref.extractall("./temp_update")
            
            # Копируем файлы обновления
            for item in os.listdir("./temp_update"):
                src = os.path.join("./temp_update", item)
                dst = os.path.join(".", item)
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            # Очищаем временные файлы
            shutil.rmtree("./temp_update")
            os.remove(self.update_file)
            
            self.update_installed.emit()
            
            # Перезапускаем приложение
            self.restart_application()
            
        except Exception as e:
            # Восстанавливаем из резервной копии
            if os.path.exists("./backup"):
                shutil.rmtree(".")
                shutil.copytree("./backup", ".")
                shutil.rmtree("./backup")
            
            self.update_failed.emit(f"Ошибка установки обновления: {e}")
        
        finally:
            self.is_updating = False
    
    def restart_application(self):
        """Перезапуск приложения"""
        if self.parent_widget:
            self.parent_widget.close()
        
        # Перезапускаем с теми же аргументами
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def rollback_update(self):
        """Откат к предыдущей версии"""
        backup_dir = "./backup"
        if not os.path.exists(backup_dir):
            return False
        
        try:
            shutil.rmtree(".")
            shutil.copytree(backup_dir, ".")
            shutil.rmtree(backup_dir)
            return True
        except Exception as e:
            print(f"Ошибка отката: {e}")
            return False
    
    def compare_versions(self, v1: str, v2: str) -> int:
        """Сравнение версий"""
        def parse_version(v):
            return [int(x) for x in v.split('.')]
        
        try:
            v1_parts = parse_version(v1)
            v2_parts = parse_version(v2)
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_val = v1_parts[i] if i < len(v1_parts) else 0
                v2_val = v2_parts[i] if i < len(v2_parts) else 0
                
                if v1_val > v2_val:
                    return 1
                elif v1_val < v2_val:
                    return -1
            
            return 0
        except:
            return 0
    
    def format_size(self, size: int) -> str:
        """Форматирование размера"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def load_settings(self):
        """Загрузка настроек"""
        try:
            with open("updater_settings.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.check_interval = data.get("check_interval", 86400)
                self.auto_download = data.get("auto_download", False)
                self.auto_install = data.get("auto_install", False)
                self.last_check = datetime.fromisoformat(data["last_check"]) if "last_check" in data else None
        except:
            pass
    
    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open("updater_settings.json", "w", encoding='utf-8') as f:
                json.dump({
                    "check_interval": self.check_interval,
                    "auto_download": self.auto_download,
                    "auto_install": self.auto_install,
                    "last_check": self.last_check.isoformat() if self.last_check else None
                }, f)
        except:
            pass