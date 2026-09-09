"""
Менеджер загрузок:
- Многопоточная загрузка
- Пауза/возобновление
- Планировщик загрузок
- Список загрузок с прогрессом
"""

import os
import threading
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class DownloadItem:
    """Объект загрузки"""
    
    def __init__(self, url: str, filename: str, save_path: str):
        self.url = url
        self.filename = filename
        self.save_path = save_path
        self.size = 0
        self.downloaded = 0
        self.status = "pending"  # pending, downloading, paused, completed, failed
        self.speed = 0
        self.start_time = None
        self.end_time = None
        self.thread = None
        self.paused = False
        self.error = None
    
    def get_progress(self) -> float:
        """Получение прогресса загрузки"""
        if self.size == 0:
            return 0
        return (self.downloaded / self.size) * 100
    
    def get_speed_text(self) -> str:
        """Получение скорости в читаемом формате"""
        if self.speed < 1024:
            return f"{self.speed:.0f} B/s"
        elif self.speed < 1024 * 1024:
            return f"{self.speed / 1024:.1f} KB/s"
        else:
            return f"{self.speed / (1024 * 1024):.1f} MB/s"
    
    def get_size_text(self) -> str:
        """Получение размера в читаемом формате"""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        else:
            return f"{self.size / (1024 * 1024):.1f} MB"
    
    def get_downloaded_text(self) -> str:
        """Получение загруженного в читаемом формате"""
        if self.downloaded < 1024:
            return f"{self.downloaded} B"
        elif self.downloaded < 1024 * 1024:
            return f"{self.downloaded / 1024:.1f} KB"
        else:
            return f"{self.downloaded / (1024 * 1024):.1f} MB"

class DownloadManager(QObject):
    """Менеджер загрузок"""
    
    # Сигналы
    download_added = pyqtSignal(DownloadItem)
    download_updated = pyqtSignal(DownloadItem)
    download_finished = pyqtSignal(DownloadItem)
    download_failed = pyqtSignal(DownloadItem, str)
    
    def __init__(self):
        super().__init__()
        
        self.downloads: List[DownloadItem] = []
        self.max_concurrent = 5
        self.active_downloads = 0
        self.download_dir = os.path.expanduser("~/Downloads")
        self.temp_dir = "./temp_downloads"
        
        # Создаем директории
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Таймер для обновления скоростей
        self.speed_timer = QTimer()
        self.speed_timer.timeout.connect(self.update_speeds)
        self.speed_timer.start(1000)
    
    def add_download(self, url: str, filename: str = None, save_path: str = None) -> DownloadItem:
        """Добавление загрузки"""
        if not filename:
            filename = url.split("/")[-1] or "download"
        
        if not save_path:
            save_path = self.download_dir
        
        # Проверяем, существует ли файл
        filepath = os.path.join(save_path, filename)
        if os.path.exists(filepath):
            # Добавляем номер к имени
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(save_path, f"{name}_{counter}{ext}")):
                counter += 1
            filename = f"{name}_{counter}{ext}"
        
        download = DownloadItem(url, filename, save_path)
        self.downloads.append(download)
        self.download_added.emit(download)
        
        # Начинаем загрузку
        self.start_download(download)
        
        return download
    
    def start_download(self, download: DownloadItem):
        """Запуск загрузки"""
        if self.active_downloads >= self.max_concurrent:
            download.status = "pending"
            return
        
        download.status = "downloading"
        download.start_time = datetime.now()
        self.active_downloads += 1
        
        # Запускаем в отдельном потоке
        download.thread = threading.Thread(
            target=self.download_thread,
            args=(download,),
            daemon=True
        )
        download.thread.start()
    
    def download_thread(self, download: DownloadItem):
        """Поток загрузки"""
        try:
            temp_path = os.path.join(self.temp_dir, f"{download.filename}.part")
            
            # Проверяем, есть ли частичная загрузка
            if os.path.exists(temp_path):
                downloaded = os.path.getsize(temp_path)
                download.downloaded = downloaded
            else:
                downloaded = 0
            
            headers = {}
            if downloaded > 0:
                headers["Range"] = f"bytes={downloaded}-"
            
            # Начинаем загрузку
            response = requests.get(download.url, stream=True, headers=headers)
            response.raise_for_status()
            
            # Получаем размер файла
            content_length = response.headers.get("content-length")
            if content_length:
                download.size = int(content_length) + downloaded
            
            # Открываем файл
            mode = "ab" if downloaded > 0 else "wb"
            with open(temp_path, mode) as f:
                last_update = time.time()
                last_downloaded = downloaded
                
                for chunk in response.iter_content(chunk_size=8192):
                    if download.paused:
                        # Приостановка загрузки
                        while download.paused:
                            time.sleep(0.1)
                    
                    if chunk:
                        f.write(chunk)
                        download.downloaded += len(chunk)
                        
                        # Обновляем скорость
                        current_time = time.time()
                        if current_time - last_update >= 1:
                            download.speed = (download.downloaded - last_downloaded) / (current_time - last_update)
                            last_update = current_time
                            last_downloaded = download.downloaded
                            self.download_updated.emit(download)
            
            # Завершаем загрузку
            download.end_time = datetime.now()
            download.status = "completed"
            download.speed = 0
            
            # Перемещаем файл в конечную папку
            final_path = os.path.join(download.save_path, download.filename)
            os.rename(temp_path, final_path)
            
            self.download_finished.emit(download)
            
        except Exception as e:
            download.status = "failed"
            download.error = str(e)
            self.download_failed.emit(download, str(e))
        
        finally:
            self.active_downloads -= 1
            # Запускаем следующую загрузку из очереди
            self.process_queue()
    
    def process_queue(self):
        """Обработка очереди загрузок"""
        if self.active_downloads >= self.max_concurrent:
            return
        
        for download in self.downloads:
            if download.status == "pending":
                self.start_download(download)
                break
    
    def pause_download(self, download: DownloadItem):
        """Приостановка загрузки"""
        if download.status == "downloading":
            download.paused = True
            download.status = "paused"
            self.download_updated.emit(download)
    
    def resume_download(self, download: DownloadItem):
        """Возобновление загрузки"""
        if download.status == "paused":
            download.paused = False
            download.status = "downloading"
            self.download_updated.emit(download)
    
    def cancel_download(self, download: DownloadItem):
        """Отмена загрузки"""
        if download.status in ["pending", "downloading", "paused"]:
            download.status = "cancelled"
            download.paused = True
            
            # Удаляем временный файл
            temp_path = os.path.join(self.temp_dir, f"{download.filename}.part")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            self.download_updated.emit(download)
            
            if download.thread:
                download.thread.join(timeout=0.1)
    
    def remove_download(self, download: DownloadItem):
        """Удаление загрузки"""
        if download in self.downloads:
            if download.status == "completed":
                # Удаляем файл
                filepath = os.path.join(download.save_path, download.filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            self.downloads.remove(download)
    
    def clear_completed(self):
        """Очистка завершенных загрузок"""
        for download in self.downloads[:]:
            if download.status == "completed":
                self.downloads.remove(download)
    
    def update_speeds(self):
        """Обновление скоростей загрузки"""
        for download in self.downloads:
            if download.status == "downloading":
                self.download_updated.emit(download)
    
    def get_downloads(self) -> List[DownloadItem]:
        """Получение списка загрузок"""
        return self.downloads
    
    def get_active_downloads(self) -> List[DownloadItem]:
        """Получение активных загрузок"""
        return [d for d in self.downloads if d.status in ["downloading", "pending"]]
    
    def get_completed_downloads(self) -> List[DownloadItem]:
        """Получение завершенных загрузок"""
        return [d for d in self.downloads if d.status == "completed"]
    
    def get_failed_downloads(self) -> List[DownloadItem]:
        """Получение неудачных загрузок"""
        return [d for d in self.downloads if d.status == "failed"]