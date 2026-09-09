"""
RSS-агрегатор:
- Подписка на RSS-ленты
- Парсинг новостей
- Обновление в реальном времени
- Фильтрация новостей
- Экспорт/импорт подписок
"""

import feedparser
import json
import os
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class RSSFeed:
    """Класс RSS-ленты"""
    
    def __init__(self, url: str, title: str = None):
        self.url = url
        self.title = title or url
        self.icon = None
        self.last_updated = None
        self.update_interval = 3600  # 1 час
        self.items = []
        self.unread_count = 0
        self.category = "Основные"
        self.enabled = True
    
    def to_dict(self) -> Dict:
        return {
            "url": self.url,
            "title": self.title,
            "icon": self.icon,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "update_interval": self.update_interval,
            "category": self.category,
            "enabled": self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RSSFeed':
        feed = cls(data["url"], data.get("title"))
        feed.icon = data.get("icon")
        feed.last_updated = datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else None
        feed.update_interval = data.get("update_interval", 3600)
        feed.category = data.get("category", "Основные")
        feed.enabled = data.get("enabled", True)
        return feed

class RSSItem:
    """Класс RSS-элемента (новости)"""
    
    def __init__(self, feed_url: str, title: str, link: str, description: str = "",
                 pub_date: datetime = None, author: str = "", guid: str = ""):
        self.feed_url = feed_url
        self.title = title
        self.link = link
        self.description = description
        self.pub_date = pub_date or datetime.now()
        self.author = author
        self.guid = guid or link
        self.read = False
        self.starred = False
        self.saved = False
    
    def to_dict(self) -> Dict:
        return {
            "feed_url": self.feed_url,
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "pub_date": self.pub_date.isoformat(),
            "author": self.author,
            "guid": self.guid,
            "read": self.read,
            "starred": self.starred,
            "saved": self.saved
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RSSItem':
        item = cls(
            data["feed_url"],
            data["title"],
            data["link"],
            data.get("description", ""),
            datetime.fromisoformat(data["pub_date"]),
            data.get("author", ""),
            data.get("guid", data["link"])
        )
        item.read = data.get("read", False)
        item.starred = data.get("starred", False)
        item.saved = data.get("saved", False)
        return item

class RSSReader(QObject):
    """RSS-агрегатор"""
    
    # Сигналы
    feed_added = pyqtSignal(RSSFeed)
    feed_removed = pyqtSignal(str)  # feed_url
    feed_updated = pyqtSignal(RSSFeed, int)  # feed, new_items_count
    feed_update_failed = pyqtSignal(str, str)  # feed_url, error
    new_items = pyqtSignal(list)  # list of RSSItem
    item_read = pyqtSignal(RSSItem)
    item_starred = pyqtSignal(RSSItem)
    item_saved = pyqtSignal(RSSItem)
    
    def __init__(self):
        super().__init__()
        
        self.feeds: Dict[str, RSSFeed] = {}
        self.items: List[RSSItem] = []
        self.categories = set()
        
        self.auto_update_enabled = True
        self.update_interval = 1800  # 30 минут
        self.max_items_per_feed = 200
        
        # Загрузка сохраненных данных
        self.load_feeds()
        self.load_items()
        
        # Таймер автообновления
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_feeds)
        self.update_timer.start(self.update_interval * 1000)
        
        # Обновляем сразу после запуска
        QTimer.singleShot(1000, self.update_all_feeds)
    
    def add_feed(self, url: str, title: str = None, category: str = "Основные") -> Optional[RSSFeed]:
        """Добавление RSS-ленты"""
        if url in self.feeds:
            return None
        
        # Проверяем доступность
        try:
            feed_data = feedparser.parse(url)
            if feed_data.bozo:
                raise Exception("Неверный RSS-формат")
            
            feed = RSSFeed(url, title or feed_data.feed.get("title", url))
            feed.category = category
            
            # Получаем иконку
            if "image" in feed_data.feed:
                feed.icon = feed_data.feed.image.get("href")
            
            self.feeds[url] = feed
            self.categories.add(category)
            
            # Парсим новости
            items = self.parse_feed_items(url, feed_data)
            self.items.extend(items)
            
            self.feed_added.emit(feed)
            self.save_feeds()
            self.save_items()
            
            return feed
            
        except Exception as e:
            self.feed_update_failed.emit(url, str(e))
            return None
    
    def remove_feed(self, url: str) -> bool:
        """Удаление RSS-ленты"""
        if url not in self.feeds:
            return False
        
        del self.feeds[url]
        
        # Удаляем все новости из этой ленты
        self.items = [item for item in self.items if item.feed_url != url]
        
        self.feed_removed.emit(url)
        self.save_feeds()
        self.save_items()
        return True
    
    def update_feed(self, url: str) -> bool:
        """Обновление конкретной ленты"""
        if url not in self.feeds:
            return False
        
        feed = self.feeds[url]
        
        try:
            feed_data = feedparser.parse(url)
            if feed_data.bozo:
                raise Exception("Неверный RSS-формат")
            
            # Обновляем заголовок
            if feed_data.feed.get("title"):
                feed.title = feed_data.feed.get("title")
            
            # Получаем новые элементы
            new_items = self.parse_feed_items(url, feed_data)
            
            # Фильтруем дубликаты
            existing_guids = {item.guid for item in self.items if item.feed_url == url}
            unique_items = [item for item in new_items if item.guid not in existing_guids]
            
            if unique_items:
                self.items.extend(unique_items)
                self.new_items.emit(unique_items)
                
                # Ограничиваем количество
                feed_items = [item for item in self.items if item.feed_url == url]
                if len(feed_items) > self.max_items_per_feed:
                    # Удаляем старые новости
                    feed_items.sort(key=lambda x: x.pub_date, reverse=True)
                    to_remove = feed_items[self.max_items_per_feed:]
                    for item in to_remove:
                        self.items.remove(item)
            
            feed.last_updated = datetime.now()
            self.feed_updated.emit(feed, len(unique_items))
            self.save_feeds()
            self.save_items()
            
            return True
            
        except Exception as e:
            self.feed_update_failed.emit(url, str(e))
            return False
    
    def update_all_feeds(self):
        """Обновление всех лент"""
        if not self.auto_update_enabled:
            return
        
        for url in self.feeds:
            feed = self.feeds[url]
            if not feed.enabled:
                continue
            
            # Проверяем, нужно ли обновлять
            if feed.last_updated:
                time_diff = (datetime.now() - feed.last_updated).total_seconds()
                if time_diff < feed.update_interval:
                    continue
            
            self.update_feed(url)
    
    def parse_feed_items(self, feed_url: str, feed_data) -> List[RSSItem]:
        """Парсинг элементов RSS-ленты"""
        items = []
        
        for entry in feed_data.entries:
            # Получаем дату
            pub_date = None
            if hasattr(entry, "published_parsed"):
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed"):
                pub_date = datetime(*entry.updated_parsed[:6])
            
            # Получаем GUID
            guid = getattr(entry, "id", getattr(entry, "guid", entry.link))
            
            item = RSSItem(
                feed_url=feed_url,
                title=entry.get("title", "Без заголовка"),
                link=entry.get("link", ""),
                description=entry.get("description", entry.get("summary", "")),
                pub_date=pub_date or datetime.now(),
                author=entry.get("author", ""),
                guid=guid
            )
            
            items.append(item)
        
        return items
    
    def get_items(self, feed_url: str = None, unread_only: bool = False,
                  starred_only: bool = False, saved_only: bool = False,
                  limit: int = None) -> List[RSSItem]:
        """Получение новостей с фильтрацией"""
        items = self.items
        
        if feed_url:
            items = [item for item in items if item.feed_url == feed_url]
        
        if unread_only:
            items = [item for item in items if not item.read]
        
        if starred_only:
            items = [item for item in items if item.starred]
        
        if saved_only:
            items = [item for item in items if item.saved]
        
        # Сортировка по дате (новые сверху)
        items.sort(key=lambda x: x.pub_date, reverse=True)
        
        if limit:
            items = items[:limit]
        
        return items
    
    def get_unread_count(self, feed_url: str = None) -> int:
        """Получение количества непрочитанных новостей"""
        items = self.get_items(feed_url, unread_only=True)
        return len(items)
    
    def mark_as_read(self, item: RSSItem):
        """Отметка новости как прочитанной"""
        item.read = True
        self.item_read.emit(item)
        self.save_items()
    
    def mark_all_as_read(self, feed_url: str = None):
        """Отметка всех новостей как прочитанных"""
        for item in self.get_items(feed_url):
            item.read = True
        self.save_items()
    
    def toggle_starred(self, item: RSSItem):
        """Переключение звездочки у новости"""
        item.starred = not item.starred
        self.item_starred.emit(item)
        self.save_items()
    
    def toggle_saved(self, item: RSSItem):
        """Переключение сохранения новости"""
        item.saved = not item.saved
        self.item_saved.emit(item)
        self.save_items()
    
    def get_categories(self) -> List[str]:
        """Получение списка категорий"""
        return sorted(list(self.categories))
    
    def get_feeds_by_category(self, category: str) -> List[RSSFeed]:
        """Получение лент по категории"""
        return [feed for feed in self.feeds.values() if feed.category == category]
    
    def search_items(self, query: str) -> List[RSSItem]:
        """Поиск по новостям"""
        query_lower = query.lower()
        results = []
        
        for item in self.items:
            if (query_lower in item.title.lower() or 
                query_lower in item.description.lower() or
                query_lower in item.author.lower()):
                results.append(item)
        
        return results
    
    def save_feeds(self):
        """Сохранение лент"""
        try:
            data = [feed.to_dict() for feed in self.feeds.values()]
            with open("rss_feeds.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения лент: {e}")
    
    def load_feeds(self):
        """Загрузка лент"""
        try:
            with open("rss_feeds.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for feed_data in data:
                    feed = RSSFeed.from_dict(feed_data)
                    self.feeds[feed.url] = feed
                    self.categories.add(feed.category)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки лент: {e}")
    
    def save_items(self):
        """Сохранение новостей"""
        try:
            data = [item.to_dict() for item in self.items]
            with open("rss_items.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения новостей: {e}")
    
    def load_items(self):
        """Загрузка новостей"""
        try:
            with open("rss_items.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.items = [RSSItem.from_dict(item_data) for item_data in data]
        except FileNotFoundError:
            self.items = []
        except Exception as e:
            print(f"Ошибка загрузки новостей: {e}")
    
    def export_opml(self, filename: str):
        """Экспорт в OPML-формат"""
        try:
            opml = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.1">
  <head>
    <title>SuperBrowser RSS Subscriptions</title>
    <dateCreated>{}</dateCreated>
  </head>
  <body>
""".format(datetime.now().isoformat())
            
            for feed in self.feeds.values():
                opml += f"""    <outline type="rss" text="{feed.title}" xmlUrl="{feed.url}" />
"""
            
            opml += """  </body>
</opml>"""
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(opml)
            
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
    
    def import_opml(self, filename: str) -> int:
        """Импорт из OPML-формата"""
        try:
            import xml.etree.ElementTree as ET
            
            tree = ET.parse(filename)
            root = tree.getroot()
            
            imported = 0
            for outline in root.findall(".//outline[@type='rss']"):
                url = outline.get("xmlUrl")
                title = outline.get("title", url)
                
                if url and url not in self.feeds:
                    feed = self.add_feed(url, title)
                    if feed:
                        imported += 1
            
            return imported
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return 0
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        return {
            "feeds": len(self.feeds),
            "items": len(self.items),
            "unread": self.get_unread_count(),
            "categories": len(self.categories)
        }