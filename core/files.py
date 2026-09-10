"""
📂 Менеджер файлов InfinityBrowser v1.1
"""

import os
from datetime import datetime


class FileManager:
    """Менеджер скачанных файлов"""

    def __init__(self):
        self.base_dir = os.path.expanduser("~/Downloads/InfinityBrowser")
        os.makedirs(self.base_dir, exist_ok=True)

        self.categories = {
            "Все": "*",
            "📄 Документы": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "🖼️ Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico"],
            "🎵 Аудио": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "🎬 Видео": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "📦 Архивы": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "💻 Программы": [".exe", ".msi", ".apk", ".dmg"],
            "📊 Таблицы": [".xls", ".xlsx", ".csv"],
            "📑 Презентации": [".ppt", ".pptx"],
            "🌐 Веб": [".html", ".htm", ".css", ".js"]
        }

    def get_files(self, category="Все"):
        files = []
        if not os.path.exists(self.base_dir):
            return files

        for name in os.listdir(self.base_dir):
            fp = os.path.join(self.base_dir, name)
            if os.path.isfile(fp):
                ext = os.path.splitext(name)[1].lower()
                if category != "Все":
                    if ext not in self.categories.get(category, []):
                        continue
                stats = os.stat(fp)
                files.append({
                    "name": name,
                    "path": fp,
                    "size": stats.st_size,
                    "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "extension": ext,
                    "category": self.get_category(ext)
                })

        files.sort(key=lambda x: x["modified"], reverse=True)
        return files

    def get_category(self, ext):
        for cat, exts in self.categories.items():
            if cat != "Все" and ext in exts:
                return cat
        return "Другое"

    def delete_file(self, name):
        fp = os.path.join(self.base_dir, name)
        if os.path.exists(fp):
            os.remove(fp)
            return True
        return False

    def open_file(self, name):
        fp = os.path.join(self.base_dir, name)
        if os.path.exists(fp):
            os.startfile(fp)
            return True
        return False

    def open_folder(self):
        os.startfile(self.base_dir)

    def get_file_info(self, name):
        fp = os.path.join(self.base_dir, name)
        if os.path.exists(fp):
            stats = os.stat(fp)
            ext = os.path.splitext(name)[1].lower()
            return {
                "name": name,
                "path": fp,
                "size": stats.st_size,
                "size_text": self.format_size(stats.st_size),
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                "extension": ext,
                "category": self.get_category(ext)
            }
        return None

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"