"""
📥 Менеджер загрузок InfinityBrowser v1.1
"""

import os
import time
import json
import threading
from datetime import datetime
from urllib.parse import urlparse
from PyQt5.QtWidgets import QApplication


class DownloadManager:
    """Менеджер загрузок с прогрессом и паузой"""

    def __init__(self):
        self.downloads = []
        self.download_dir = os.path.expanduser("~/Downloads/InfinityBrowser")
        os.makedirs(self.download_dir, exist_ok=True)
        self.load_downloads()

    def add_download(self, url, filename=None, save_path=None):
        """Добавляет новую загрузку"""
        if not filename:
            filename = os.path.basename(urlparse(url).path) or "download"
        if not save_path:
            save_path = self.download_dir

        filepath = os.path.join(save_path, filename)
        counter = 1
        name, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filepath = os.path.join(save_path, f"{name}_{counter}{ext}")
            counter += 1

        download = {
            "id": str(int(time.time() * 1000)),
            "url": url,
            "filename": filename,
            "filepath": filepath,
            "save_path": save_path,
            "size": 0,
            "downloaded": 0,
            "status": "pending",
            "speed": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "progress": 0,
            "error": None
        }

        self.downloads.insert(0, download)
        self.save_downloads()
        self.start_download(download)
        return download

    def start_download(self, download):
        """Запускает загрузку в отдельном потоке"""
        def worker():
            try:
                import requests
                download["status"] = "downloading"
                r = requests.get(download["url"], stream=True, timeout=30)
                r.raise_for_status()

                total = int(r.headers.get('content-length', 0))
                download["size"] = total
                downloaded = 0
                last_time = time.time()
                last_dl = 0

                with open(download["filepath"], "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                download["progress"] = (downloaded / total) * 100
                            download["downloaded"] = downloaded

                            now = time.time()
                            if now - last_time >= 1:
                                download["speed"] = (downloaded - last_dl) / (now - last_time)
                                last_time = now
                                last_dl = downloaded

                            self.save_downloads()

                download["status"] = "completed"
                download["end_time"] = datetime.now().isoformat()
                download["progress"] = 100
                self.save_downloads()
                QApplication.processEvents()

            except Exception as e:
                download["status"] = "failed"
                download["error"] = str(e)
                self.save_downloads()

        threading.Thread(target=worker, daemon=True).start()

    def get_downloads(self):
        return self.downloads

    def get_active_downloads(self):
        return [d for d in self.downloads if d["status"] in ["pending", "downloading"]]

    def get_completed_downloads(self):
        return [d for d in self.downloads if d["status"] == "completed"]

    def open_file(self, did):
        for d in self.downloads:
            if d["id"] == did and d["status"] == "completed":
                if os.path.exists(d["filepath"]):
                    os.startfile(d["filepath"])
                    return True
        return False

    def open_folder(self, did):
        for d in self.downloads:
            if d["id"] == did and os.path.exists(d["save_path"]):
                os.startfile(d["save_path"])
                return True
        return False

    def remove_download(self, did):
        self.downloads = [d for d in self.downloads if d["id"] != did]
        self.save_downloads()

    def pause_download(self, did):
        for d in self.downloads:
            if d["id"] == did and d["status"] == "downloading":
                d["status"] = "paused"
                self.save_downloads()
                return True
        return False

    def resume_download(self, did):
        for d in self.downloads:
            if d["id"] == did and d["status"] == "paused":
                d["status"] = "pending"
                self.save_downloads()
                self.start_download(d)
                return True
        return False

    def save_downloads(self):
        try:
            with open("downloads.json", "w", encoding="utf-8") as f:
                json.dump(self.downloads, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_downloads(self):
        try:
            with open("downloads.json", "r", encoding="utf-8") as f:
                self.downloads = json.load(f)
        except:
            self.downloads = []