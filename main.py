"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🌌 INFINITY BROWSER v4.0                                   ║
║   Полноценный браузер с 50+ функциями                        ║
║                                                              ║
║   ВОЗМОЖНОСТИ:                                               ║
║   ✅ Открытие ссылок в новой вкладке (Ctrl+Click, MMB)      ║
║   ✅ target=_blank и window.open() → новая вкладка          ║
║   ✅ Вкладки, закладки, история                              ║
║   ✅ AdBlock                                                 ║
║   ✅ Менеджер загрузок                                       ║
║   ✅ Менеджер файлов                                         ║
║   ✅ Расширения (ZIP / папка / JS)                           ║
║   ✅ F12 DevTools                                            ║
║   ✅ Заметки, RSS, разрешения                                ║
║   ✅ 5 тем оформления                                        ║
║   ✅ 15+ языков интерфейса                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import json
import re
import time
import threading
import hashlib
import shutil
import zipfile
import tempfile
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *

# ============================================================================
# 📌 ВЕРСИЯ
# ============================================================================
VERSION = "4.0"
BUILD = "2026.09.10"


# ============================================================================
# 🌍 МЕНЕДЖЕР ЯЗЫКОВ (15+ языков)
# ============================================================================
class LanguageManager:
    """Менеджер локализации интерфейса"""

    LANGUAGES = {
        "ru": {"name": "🇷🇺 Русский", "native": "Русский"},
        "en": {"name": "🇬🇧 English", "native": "English"},
        "uk": {"name": "🇺🇦 Українська", "native": "Українська"},
        "de": {"name": "🇩🇪 Deutsch", "native": "Deutsch"},
        "fr": {"name": "🇫🇷 Français", "native": "Français"},
        "es": {"name": "🇪🇸 Español", "native": "Español"},
        "it": {"name": "🇮🇹 Italiano", "native": "Italiano"},
        "pt": {"name": "🇵🇹 Português", "native": "Português"},
        "pl": {"name": "🇵🇱 Polski", "native": "Polski"},
        "zh": {"name": "🇨🇳 中文", "native": "中文"},
        "ja": {"name": "🇯🇵 日本語", "native": "日本語"},
        "ko": {"name": "🇰🇷 한국어", "native": "한국어"},
        "ar": {"name": "🇸🇦 العربية", "native": "العربية"},
        "hi": {"name": "🇮🇳 हिन्दी", "native": "हिन्दी"},
        "tr": {"name": "🇹🇷 Türkçe", "native": "Türkçe"},
    }

    TRANSLATIONS = {
        "ru": {
            "app_title": f"🌌 InfinityBrowser v{VERSION}",
            "window_title": f"🌌 InfinityBrowser v{VERSION} - {{title}}",
            "back": "◀ Назад", "forward": "▶ Вперед", "reload": "🔄 Обновить",
            "home": "🏠 Домой", "go": "🚀 Перейти",
            "search_placeholder": "🔍 Поиск или введите URL...",
            "bookmark": "⭐ Закладка",
            "bookmark_added": "⭐ Закладка добавлена",
            "bookmark_removed": "⭐ Закладка удалена",
            "adblock": "🛡️ AdBlock",
            "adblock_on": "🛡️ AdBlock включен",
            "adblock_off": "🛡️ AdBlock отключен",
            "theme": "🌙 Тема",
            "sidebar": "📋 Панель",
            "downloads": "📥 Загрузки",
            "files": "📂 Файлы",
            "extensions": "🧩 Расширения",
            "tools": "⚙️ Инструменты",
            "status_ready": "✅ Готово",
            "status_loaded": "✅ Страница загружена",
            "status_connecting": "⏳ Подключение... {progress}%",
            "status_loading": "⏳ Загрузка... {progress}%",
            "status_rendering": "⏳ Рендеринг... {progress}%",
            "status_download_started": "📥 Начата загрузка: {filename}",
            "status_download_finished": "✅ Загрузка завершена: {filename}",
            "tab_new": "Новая вкладка",
            "tab_from_link": "🆕 Новая вкладка из ссылки",
            "tab_restored": "↩️ Восстановлена",
            "menu_file": "📁 Файл",
            "menu_new_tab": "📄 Новая вкладка",
            "menu_new_window": "📂 Новое окно",
            "menu_incognito": "🕵️ Инкогнито",
            "menu_downloads": "📥 Менеджер загрузок",
            "menu_files": "📂 Менеджер файлов",
            "menu_save": "💾 Сохранить как...",
            "menu_print": "🖨️ Печать",
            "menu_exit": "🚪 Выход",
            "menu_tabs": "📑 Вкладки",
            "menu_close_tab": "❌ Закрыть вкладку",
            "menu_restore_tab": "↩️ Восстановить вкладку",
            "menu_next_tab": "◀ Следующая",
            "menu_prev_tab": "▶ Предыдущая",
            "menu_tools": "🛠️ Инструменты",
            "menu_notes": "📝 Заметки",
            "menu_rss": "📰 RSS",
            "menu_extensions": "🧩 Расширения",
            "menu_permissions": "🔒 Разрешения",
            "menu_themes": "🎨 Темы",
            "menu_settings": "⚡ Настройки",
            "menu_help": "❓ Помощь",
            "menu_help_item": "📖 Справка",
            "menu_about": "ℹ️ О программе",
            "downloads_title": "📥 Менеджер загрузок",
            "downloads_open": "📂 Открыть файл",
            "downloads_folder": "📁 Открыть папку",
            "downloads_remove": "❌ Удалить из списка",
            "downloads_clear": "🗑️ Очистить завершенные",
            "downloads_close": "Закрыть",
            "downloads_pending": "⏳ Ожидание",
            "downloads_active": "📥 Загрузка",
            "downloads_completed": "✅ Завершена",
            "downloads_failed": "❌ Ошибка",
            "files_title": "📂 Менеджер файлов",
            "files_category": "📂 Категория:",
            "files_search": "🔍 Поиск файлов...",
            "files_open_folder": "📁 Открыть папку",
            "files_open": "📂 Открыть",
            "files_delete": "🗑️ Удалить",
            "files_info": "ℹ️ Информация",
            "files_close": "Закрыть",
            "files_deleted": "🗑️ Файл '{filename}' удален",
            "extensions_title": "🧩 Расширения",
            "extensions_install": "🧩 Установить расширение",
            "extensions_install_zip": "📦 Установить из ZIP",
            "extensions_install_folder": "📁 Установить из папки",
            "extensions_install_js": "📄 Установить из JS",
            "extensions_manage": "🧩 Управление расширениями",
            "extensions_open": "🔍 Открыть",
            "extensions_toggle": "🔄 Вкл/Выкл",
            "extensions_uninstall": "🗑️ Удалить",
            "extensions_code": "📄 Код",
            "extensions_options": "⚙️ Настройки",
            "extensions_installed": "🧩 Расширение '{name}' установлено!",
            "extensions_uninstalled": "❌ Расширение '{name}' удалено",
            "extensions_enabled": "🟢 Расширение '{name}' включено",
            "extensions_disabled": "🔴 Расширение '{name}' выключено",
            "extensions_cannot_uninstall": "❌ Нельзя удалить встроенное расширение!",
            "extensions_uninstall_confirm": "Удалить расширение '{name}'?",
            "permissions_title": "🔒 Разрешения",
            "permissions_request": "🔒 Запрос разрешения",
            "permissions_text": "Сайт <b>{domain}</b> запрашивает разрешение на <b>{permission}</b>",
            "permissions_allow": "✅ Разрешить",
            "permissions_deny": "❌ Запретить",
            "permissions_revoke": "❌ Отозвать все",
            "settings_title": "⚡ Настройки",
            "settings_general": "Общие настройки",
            "settings_home": "🏠 Домашняя страница:",
            "settings_search": "🔍 Поисковик:",
            "settings_security": "Безопасность",
            "settings_adblock": "🛡️ Включить AdBlock",
            "settings_language": "🌍 Язык:",
            "settings_save": "💾 Сохранить",
            "settings_cancel": "❌ Отмена",
            "settings_saved": "⚡ Настройки сохранены",
            "themes_title": "🎨 Выбор темы",
            "themes_select": "Выберите тему:",
            "find_title": "🔍 Поиск",
            "find_text": "Введите текст для поиска:",
            "find_result": "🔍 Поиск: {text}",
            "help_title": "📖 Справка",
            "about_title": "ℹ️ О программе",
            "notification_copied": "✅ Ссылка скопирована",
            "notification_theme_changed": "🎨 Тема изменена",
            "notification_history_cleared": "🗑️ История очищена",
            "sidebar_bookmarks": "⭐ Закладки",
            "sidebar_history": "⏳ История",
            "sidebar_notes": "📝 Заметки",
            "sidebar_rss": "📰 RSS",
            "sidebar_extensions": "🧩 Расширения",
            "sidebar_search_bookmarks": "🔍 Поиск закладок...",
            "sidebar_search_history": "🔍 Поиск в истории...",
            "sidebar_search_notes": "🔍 Поиск заметок...",
            "sidebar_add_bookmark": "➕ Добавить закладку",
            "sidebar_add_note": "➕ Новая заметка",
            "sidebar_clear_history": "🗑️ Очистить историю",
            "notes_new_title": "📝 Новая заметка",
            "notes_title_label": "Заголовок:",
            "notes_content_label": "Текст:",
            "notes_save": "💾 Сохранить",
            "notes_cancel": "❌ Отмена",
            "notes_created": "📝 Заметка '{title}' создана",
            "notes_deleted": "🗑️ Заметка удалена",
            "rss_placeholder": "Введите URL RSS...",
            "rss_added": "📰 RSS добавлен: {url}",
            "rss_exists": "❌ RSS уже существует",
            "indicator_downloads": "📥 {total} ({active})",
            "indicator_extensions": "🧩 {count}",
            "ssl_secure": "🔒 Безопасное соединение",
            "ssl_insecure": "🔓 Незащищенное соединение",
            "incognito_title": "🕵️ Инкогнито - InfinityBrowser",
            "incognito_activated": "🕵️ Режим инкогнито активирован",
            "save_page_title": "💾 Сохранить страницу",
            "save_page_filter": "HTML файлы (*.html);;Все файлы (*.*)",
            "save_page_saved": "✅ Страница сохранена: {filename}",
            "save_page_error": "❌ Ошибка: {error}",
            "print_started": "🖨️ Печать в PDF запущена",
            "welcome_title": f"🌌 Добро пожаловать в InfinityBrowser v{VERSION}!",
            "welcome_text": f"""
                <h2>🚀 InfinityBrowser v{VERSION} готов!</h2>
                <p><b>Что нового:</b></p>
                <ul>
                    <li><b>🆕 Открытие ссылок в новой вкладке</b></li>
                    <li><b>💡 Ctrl + клик по ссылке</b> → новая вкладка</li>
                    <li><b>🖱️ Клик колёсиком мыши</b> → новая вкладка</li>
                    <li><b>🎯 target=_blank и window.open()</b> → новая вкладка</li>
                </ul>
                <p>📚 Нажми <b>F1</b> для справки, <b>F12</b> для DevTools</p>
            """
        },
        "en": {
            "app_title": f"🌌 InfinityBrowser v{VERSION}",
            "window_title": f"🌌 InfinityBrowser v{VERSION} - {{title}}",
            "back": "◀ Back", "forward": "▶ Forward", "reload": "🔄 Reload",
            "home": "🏠 Home", "go": "🚀 Go",
            "search_placeholder": "🔍 Search or enter URL...",
            "bookmark": "⭐ Bookmark",
            "bookmark_added": "⭐ Bookmark added",
            "bookmark_removed": "⭐ Bookmark removed",
            "adblock": "🛡️ AdBlock",
            "adblock_on": "🛡️ AdBlock enabled",
            "adblock_off": "🛡️ AdBlock disabled",
            "theme": "🌙 Theme",
            "sidebar": "📋 Sidebar",
            "downloads": "📥 Downloads",
            "files": "📂 Files",
            "extensions": "🧩 Extensions",
            "tools": "⚙️ Tools",
            "status_ready": "✅ Ready",
            "status_loaded": "✅ Page loaded",
            "status_connecting": "⏳ Connecting... {progress}%",
            "status_loading": "⏳ Loading... {progress}%",
            "status_rendering": "⏳ Rendering... {progress}%",
            "status_download_started": "📥 Download started: {filename}",
            "status_download_finished": "✅ Download complete: {filename}",
            "tab_new": "New Tab",
            "tab_from_link": "🆕 New Tab from link",
            "tab_restored": "↩️ Restored",
            "menu_file": "📁 File",
            "menu_new_tab": "📄 New Tab",
            "menu_new_window": "📂 New Window",
            "menu_incognito": "🕵️ Incognito",
            "menu_downloads": "📥 Downloads",
            "menu_files": "📂 Files",
            "menu_save": "💾 Save As...",
            "menu_print": "🖨️ Print",
            "menu_exit": "🚪 Exit",
            "menu_tabs": "📑 Tabs",
            "menu_close_tab": "❌ Close Tab",
            "menu_restore_tab": "↩️ Restore Tab",
            "menu_next_tab": "◀ Next",
            "menu_prev_tab": "▶ Previous",
            "menu_tools": "🛠️ Tools",
            "menu_notes": "📝 Notes",
            "menu_rss": "📰 RSS",
            "menu_extensions": "🧩 Extensions",
            "menu_permissions": "🔒 Permissions",
            "menu_themes": "🎨 Themes",
            "menu_settings": "⚡ Settings",
            "menu_help": "❓ Help",
            "menu_help_item": "📖 Help",
            "menu_about": "ℹ️ About",
            "downloads_title": "📥 Download Manager",
            "downloads_open": "📂 Open File",
            "downloads_folder": "📁 Open Folder",
            "downloads_remove": "❌ Remove",
            "downloads_clear": "🗑️ Clear Completed",
            "downloads_close": "Close",
            "downloads_pending": "⏳ Pending",
            "downloads_active": "📥 Downloading",
            "downloads_completed": "✅ Completed",
            "downloads_failed": "❌ Failed",
            "files_title": "📂 File Manager",
            "files_category": "📂 Category:",
            "files_search": "🔍 Search files...",
            "files_open_folder": "📁 Open Folder",
            "files_open": "📂 Open",
            "files_delete": "🗑️ Delete",
            "files_info": "ℹ️ Info",
            "files_close": "Close",
            "files_deleted": "🗑️ File '{filename}' deleted",
            "extensions_title": "🧩 Extensions",
            "extensions_install": "🧩 Install Extension",
            "extensions_install_zip": "📦 Install from ZIP",
            "extensions_install_folder": "📁 Install from folder",
            "extensions_install_js": "📄 Install from JS",
            "extensions_manage": "🧩 Manage Extensions",
            "extensions_open": "🔍 Open",
            "extensions_toggle": "🔄 Toggle",
            "extensions_uninstall": "🗑️ Uninstall",
            "extensions_code": "📄 Code",
            "extensions_options": "⚙️ Options",
            "extensions_installed": "🧩 Extension '{name}' installed!",
            "extensions_uninstalled": "❌ Extension '{name}' uninstalled",
            "extensions_enabled": "🟢 Extension '{name}' enabled",
            "extensions_disabled": "🔴 Extension '{name}' disabled",
            "extensions_cannot_uninstall": "❌ Cannot uninstall built-in extension!",
            "extensions_uninstall_confirm": "Uninstall extension '{name}'?",
            "permissions_title": "🔒 Permissions",
            "permissions_request": "🔒 Permission Request",
            "permissions_text": "Site <b>{domain}</b> requests permission for <b>{permission}</b>",
            "permissions_allow": "✅ Allow",
            "permissions_deny": "❌ Deny",
            "permissions_revoke": "❌ Revoke All",
            "settings_title": "⚡ Settings",
            "settings_general": "General Settings",
            "settings_home": "🏠 Home Page:",
            "settings_search": "🔍 Search Engine:",
            "settings_security": "Security",
            "settings_adblock": "🛡️ Enable AdBlock",
            "settings_language": "🌍 Language:",
            "settings_save": "💾 Save",
            "settings_cancel": "❌ Cancel",
            "settings_saved": "⚡ Settings saved",
            "themes_title": "🎨 Choose Theme",
            "themes_select": "Select theme:",
            "find_title": "🔍 Find",
            "find_text": "Enter search text:",
            "find_result": "🔍 Search: {text}",
            "help_title": "📖 Help",
            "about_title": "ℹ️ About",
            "notification_copied": "✅ Link copied",
            "notification_theme_changed": "🎨 Theme changed",
            "notification_history_cleared": "🗑️ History cleared",
            "sidebar_bookmarks": "⭐ Bookmarks",
            "sidebar_history": "⏳ History",
            "sidebar_notes": "📝 Notes",
            "sidebar_rss": "📰 RSS",
            "sidebar_extensions": "🧩 Extensions",
            "sidebar_search_bookmarks": "🔍 Search bookmarks...",
            "sidebar_search_history": "🔍 Search in history...",
            "sidebar_search_notes": "🔍 Search notes...",
            "sidebar_add_bookmark": "➕ Add Bookmark",
            "sidebar_add_note": "➕ New Note",
            "sidebar_clear_history": "🗑️ Clear History",
            "notes_new_title": "📝 New Note",
            "notes_title_label": "Title:",
            "notes_content_label": "Content:",
            "notes_save": "💾 Save",
            "notes_cancel": "❌ Cancel",
            "notes_created": "📝 Note '{title}' created",
            "notes_deleted": "🗑️ Note deleted",
            "rss_placeholder": "Enter RSS URL...",
            "rss_added": "📰 RSS added: {url}",
            "rss_exists": "❌ RSS already exists",
            "indicator_downloads": "📥 {total} ({active})",
            "indicator_extensions": "🧩 {count}",
            "ssl_secure": "🔒 Secure connection",
            "ssl_insecure": "🔓 Insecure connection",
            "incognito_title": "🕵️ Incognito - InfinityBrowser",
            "incognito_activated": "🕵️ Incognito mode activated",
            "save_page_title": "💾 Save Page",
            "save_page_filter": "HTML files (*.html);;All files (*.*)",
            "save_page_saved": "✅ Page saved: {filename}",
            "save_page_error": "❌ Error: {error}",
            "print_started": "🖨️ PDF printing started",
            "welcome_title": f"🌌 Welcome to InfinityBrowser v{VERSION}!",
            "welcome_text": f"""
                <h2>🚀 InfinityBrowser v{VERSION} is ready!</h2>
                <p><b>New features:</b></p>
                <ul>
                    <li><b>🆕 Open links in new tab</b></li>
                    <li><b>💡 Ctrl + click</b> → new tab</li>
                    <li><b>🖱️ Middle click</b> → new tab</li>
                    <li><b>🎯 target=_blank and window.open()</b> → new tab</li>
                </ul>
                <p>📚 Press <b>F1</b> for help, <b>F12</b> for DevTools</p>
            """
        }
    }

    def __init__(self):
        self.current_language = "ru"
        self.load_language()

    def load_language(self):
        try:
            with open("language.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_language = data.get("language", "ru")
        except:
            self.current_language = "ru"

    def save_language(self):
        try:
            with open("language.json", "w", encoding="utf-8") as f:
                json.dump({"language": self.current_language}, f)
        except:
            pass

    def set_language(self, code):
        if code in self.LANGUAGES:
            self.current_language = code
            self.save_language()
            return True
        return False

    def get_languages(self):
        return self.LANGUAGES

    def get_current_language(self):
        return self.current_language

    def get_language_name(self, code):
        return self.LANGUAGES.get(code, {}).get("name", code)

    def tr(self, key, **kwargs):
        translations = self.TRANSLATIONS.get(self.current_language, {})
        text = translations.get(key, key)
        for k, v in kwargs.items():
            text = text.replace("{" + k + "}", str(v))
        return text


# Глобальный экземпляр
language_manager = LanguageManager()


def _(key, **kwargs):
    """Глобальная функция перевода"""
    return language_manager.tr(key, **kwargs)


# ============================================================================
# 🛡️ МЕНЕДЖЕР ADBLOCK
# ============================================================================
class AdBlockManager:
    """Блокировка рекламы"""

    def __init__(self):
        self.enabled = True

        # Правила блокировки
        self.rules = [
            r"ads\.",
            r"adserver",
            r"doubleclick",
            r"googleads",
            r"googlesyndication",
            r"yandexads",
            r"adfox",
            r"adriver",
            r"rtb",
            r"criteo",
            r"adnxs",
            r"openx",
            r"rubicon",
            r"pubmatic",
            r"indexexchange",
            r"smartadserver",
            r"taboola",
            r"outbrain",
            r"adform",
            r"adroll",
            r"adsrv",
            r"adtech",
            r"advertising",
            r"banner",
            r"popup",
            r"tracker",
            r"analytics",
            r"doubleclick\.net",
            r"googletagmanager",
            r"google-analytics",
            r"facebook\.com\/tr",
            r"vk\.com\/rtrg"
        ]

        self.custom_rules = []
        self.whitelist = []
        self.blocked_count = 0

        self.load_rules()

    def should_block(self, url):
        """Проверяет, надо ли заблокировать URL"""
        if not self.enabled:
            return False

        # Проверка whitelist
        for w in self.whitelist:
            if w in url:
                return False

        # Стандартные правила
        for rule in self.rules:
            if re.search(rule, url, re.IGNORECASE):
                self.blocked_count += 1
                return True

        # Пользовательские правила
        for rule in self.custom_rules:
            if re.search(rule, url, re.IGNORECASE):
                self.blocked_count += 1
                return True

        return False

    def toggle(self):
        """Включает/выключает AdBlock"""
        self.enabled = not self.enabled
        self.save_rules()
        return self.enabled

    def add_custom_rule(self, rule):
        """Добавляет пользовательское правило"""
        if rule not in self.custom_rules:
            self.custom_rules.append(rule)
            self.save_rules()
            return True
        return False

    def remove_custom_rule(self, rule):
        """Удаляет пользовательское правило"""
        if rule in self.custom_rules:
            self.custom_rules.remove(rule)
            self.save_rules()
            return True
        return False

    def add_to_whitelist(self, url):
        """Добавляет сайт в белый список"""
        if url not in self.whitelist:
            self.whitelist.append(url)
            self.save_rules()
            return True
        return False

    def get_stats(self):
        """Статистика блокировок"""
        return {
            "enabled": self.enabled,
            "blocked_count": self.blocked_count,
            "rules_count": len(self.rules),
            "custom_rules": len(self.custom_rules),
            "whitelist": len(self.whitelist)
        }

    def save_rules(self):
        try:
            with open("adblock.json", "w", encoding="utf-8") as f:
                json.dump({
                    "enabled": self.enabled,
                    "custom_rules": self.custom_rules,
                    "whitelist": self.whitelist,
                    "blocked_count": self.blocked_count
                }, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_rules(self):
        try:
            with open("adblock.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.enabled = data.get("enabled", True)
                self.custom_rules = data.get("custom_rules", [])
                self.whitelist = data.get("whitelist", [])
                self.blocked_count = data.get("blocked_count", 0)
        except:
            pass


# ============================================================================
# 📥 МЕНЕДЖЕР ЗАГРУЗОК
# ============================================================================
class DownloadManager:
    """Менеджер загрузок с прогрессом"""

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

                with open(download["filepath"], "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                download["progress"] = (downloaded / total) * 100
                            download["downloaded"] = downloaded
                            self.save_downloads()

                download["status"] = "completed"
                download["end_time"] = datetime.now().isoformat()
                download["progress"] = 100
                self.save_downloads()

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


# ═══════════════════════════════════════════════════════════════
# 📌 КОНЕЦ ЧАСТИ 1
# ═══════════════════════════════════════════════════════════════
# ============================================================================
# 📂 МЕНЕДЖЕР ФАЙЛОВ
# ============================================================================
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


# ============================================================================
# 🧩 РАСШИРЕНИЯ
# ============================================================================
class Extension:
    """Класс расширения"""

    def __init__(self, id, name, version, author, description,
                 script="", manifest=None):
        self.id = id
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.script = script
        self.manifest = manifest or {}
        self.enabled = True
        self.permissions = []
        self.path = ""
        self.popup_html = ""
        self.options_html = ""

    def get_popup_html(self):
        """Возвращает HTML всплывающего окна расширения"""
        if self.popup_html:
            return self.popup_html

        status_class = "status-enabled" if self.enabled else "status-disabled"
        status_text = "✅ Включено" if self.enabled else "❌ Отключено"

        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body {{
    font-family: 'Segoe UI', sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    padding: 15px;
    margin: 0;
    min-width: 280px;
}}
.header {{
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #2a2a3e;
    padding-bottom: 10px;
    margin-bottom: 10px;
}}
.icon {{ font-size: 28px; width: 40px; text-align: center; }}
.name {{ font-size: 16px; font-weight: bold; color: #00d4ff; }}
.version {{ font-size: 11px; color: #808090; }}
.desc {{ font-size: 12px; color: #c0c0d0; margin: 8px 0; line-height: 1.5; }}
.status {{
    display: inline-block;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
}}
.status-enabled {{ background: #00ff88; color: #000; }}
.status-disabled {{ background: #ff4444; color: #fff; }}
.actions {{
    display: flex;
    gap: 8px;
    margin-top: 12px;
    flex-wrap: wrap;
}}
.btn {{
    padding: 6px 14px;
    border: none;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    font-weight: bold;
}}
.btn-primary {{ background: #00d4ff; color: #000; }}
.btn-secondary {{ background: #2a2a3e; color: #e0e0e0; }}
.btn-danger {{ background: #ff4444; color: #fff; }}
.info {{ font-size: 11px; color: #808090; margin: 5px 0; }}
</style></head><body>
<div class="header">
    <span class="icon">🧩</span>
    <div>
        <div class="name">{self.name}</div>
        <div class="version">v{self.version}</div>
    </div>
</div>
<div class="desc">{self.description}</div>
<div style="margin: 8px 0;">
    <span class="status {status_class}">{status_text}</span>
</div>
<div class="info">👤 {self.author}</div>
<div class="actions">
    <button class="btn btn-primary" onclick="parent.toggleExtension('{self.id}')">
        🔄 Вкл/Выкл
    </button>
    <button class="btn btn-secondary" onclick="parent.viewExtensionCode('{self.id}')">
        📄 Код
    </button>
    <button class="btn btn-secondary" onclick="parent.show_extension_options('{self.id}')">
        ⚙️
    </button>
    <button class="btn btn-danger" onclick="parent.uninstallExtension('{self.id}')">
        🗑️
    </button>
</div>
</body></html>"""

    def get_options_html(self):
        """Возвращает HTML страницы настроек расширения"""
        if self.options_html:
            return self.options_html

        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body {{
    font-family: 'Segoe UI', sans-serif;
    background: #0a0a1a;
    color: #e0e0e0;
    padding: 20px;
}}
h1 {{ color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }}
.setting {{
    background: #1a1a2e;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}}
.setting b {{ color: #00d4ff; }}
</style></head><body>
<h1>⚙️ {self.name}</h1>
<div class="setting"><b>Версия:</b> {self.version}</div>
<div class="setting"><b>Автор:</b> {self.author}</div>
<div class="setting"><b>Описание:</b> {self.description}</div>
<div class="setting"><b>ID:</b> {self.id}</div>
</body></html>"""

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "script": self.script,
            "manifest": self.manifest,
            "enabled": self.enabled,
            "permissions": self.permissions,
            "path": self.path,
            "popup_html": self.popup_html,
            "options_html": self.options_html
        }

    @classmethod
    def from_dict(cls, data):
        ext = cls(
            data["id"],
            data["name"],
            data["version"],
            data["author"],
            data["description"],
            data.get("script", ""),
            data.get("manifest", {})
        )
        ext.enabled = data.get("enabled", True)
        ext.permissions = data.get("permissions", [])
        ext.path = data.get("path", "")
        ext.popup_html = data.get("popup_html", "")
        ext.options_html = data.get("options_html", "")
        return ext


class ExtensionManager:
    """Менеджер расширений"""

    BUILTIN_IDS = ["adblock_plus", "dark_reader", "translator", "screenshot"]

    def __init__(self):
        self.extensions = {}
        self.load_extensions()
        self.install_builtins()

    def install_builtins(self):
        """Устанавливает встроенные расширения"""
        builtins = [
            ("adblock_plus", "🛡️ AdBlock Plus", "1.0.0",
             "InfinitySoft", "Блокировка рекламы на всех сайтах"),
            ("dark_reader", "🌙 Dark Reader", "1.0.0",
             "InfinitySoft", "Ночной режим для всех сайтов"),
            ("translator", "🌍 Переводчик", "1.0.0",
             "InfinitySoft", "Перевод страниц на любой язык"),
            ("screenshot", "📸 Скриншоты", "1.0.0",
             "InfinitySoft", "Быстрые скриншоты страниц")
        ]

        for eid, name, ver, author, desc in builtins:
            if eid not in self.extensions:
                ext = Extension(eid, name, ver, author, desc)
                ext.permissions = ["activeTab"]
                self.extensions[eid] = ext

        self.save_extensions()

    def install_from_zip(self, zip_path):
        """Устанавливает расширение из ZIP-архива"""
        try:
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(zip_path, 'r') as zf:
                if "manifest.json" not in zf.namelist():
                    shutil.rmtree(temp_dir)
                    return None
                zf.extractall(temp_dir)

            manifest_path = os.path.join(temp_dir, "manifest.json")
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            ext_id = hashlib.md5(manifest.get("name", "").encode()).hexdigest()[:8]
            ext_dir = os.path.join("extensions", ext_id)
            os.makedirs(ext_dir, exist_ok=True)

            for item in os.listdir(temp_dir):
                src = os.path.join(temp_dir, item)
                dst = os.path.join(ext_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            ext = Extension(
                id=ext_id,
                name=manifest.get("name", "Unknown"),
                version=manifest.get("version", "1.0.0"),
                author=manifest.get("author", "Unknown"),
                description=manifest.get("description", ""),
                manifest=manifest
            )
            ext.path = ext_dir
            ext.permissions = manifest.get("permissions", [])

            # Загружаем JS-скрипты
            if "scripts" in manifest:
                for script in manifest["scripts"]:
                    script_path = os.path.join(ext_dir, script)
                    if os.path.exists(script_path):
                        with open(script_path, "r", encoding="utf-8") as f:
                            ext.script += f.read() + "\n"

            # Загружаем popup.html
            popup_path = os.path.join(ext_dir, "popup.html")
            if os.path.exists(popup_path):
                with open(popup_path, "r", encoding="utf-8") as f:
                    ext.popup_html = f.read()

            # Загружаем options.html
            options_path = os.path.join(ext_dir, "options.html")
            if os.path.exists(options_path):
                with open(options_path, "r", encoding="utf-8") as f:
                    ext.options_html = f.read()

            self.extensions[ext_id] = ext
            self.save_extensions()
            shutil.rmtree(temp_dir, ignore_errors=True)
            return ext

        except Exception as e:
            print(f"Ошибка установки из ZIP: {e}")
            return None

    def install_from_folder(self, folder_path):
        """Устанавливает расширение из папки"""
        try:
            manifest_path = os.path.join(folder_path, "manifest.json")
            if not os.path.exists(manifest_path):
                return None

            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            ext_id = hashlib.md5(manifest.get("name", "").encode()).hexdigest()[:8]
            ext_dir = os.path.join("extensions", ext_id)
            os.makedirs(ext_dir, exist_ok=True)

            for item in os.listdir(folder_path):
                src = os.path.join(folder_path, item)
                dst = os.path.join(ext_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            ext = Extension(
                id=ext_id,
                name=manifest.get("name", "Unknown"),
                version=manifest.get("version", "1.0.0"),
                author=manifest.get("author", "Unknown"),
                description=manifest.get("description", ""),
                manifest=manifest
            )
            ext.path = ext_dir
            ext.permissions = manifest.get("permissions", [])

            if "scripts" in manifest:
                for script in manifest["scripts"]:
                    script_path = os.path.join(ext_dir, script)
                    if os.path.exists(script_path):
                        with open(script_path, "r", encoding="utf-8") as f:
                            ext.script += f.read() + "\n"

            self.extensions[ext_id] = ext
            self.save_extensions()
            return ext

        except Exception as e:
            print(f"Ошибка установки из папки: {e}")
            return None

    def install_from_js(self, name, code):
        """Устанавливает расширение из JS-кода"""
        try:
            ext_id = hashlib.md5(name.encode()).hexdigest()[:8]
            ext_dir = os.path.join("extensions", ext_id)
            os.makedirs(ext_dir, exist_ok=True)

            with open(os.path.join(ext_dir, "script.js"), "w", encoding="utf-8") as f:
                f.write(code)

            manifest = {
                "name": name,
                "version": "1.0.0",
                "author": "Пользователь",
                "description": "Пользовательское расширение",
                "scripts": ["script.js"],
                "permissions": ["activeTab"]
            }

            with open(os.path.join(ext_dir, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

            ext = Extension(ext_id, name, "1.0.0", "Пользователь",
                            "Пользовательское расширение", code, manifest)
            ext.path = ext_dir
            ext.permissions = ["activeTab"]

            self.extensions[ext_id] = ext
            self.save_extensions()
            return ext

        except Exception as e:
            print(f"Ошибка установки из JS: {e}")
            return None

    def uninstall(self, eid):
        """Удаляет расширение"""
        if eid in self.BUILTIN_IDS:
            return False
        if eid in self.extensions:
            ext = self.extensions[eid]
            if ext.path and os.path.exists(ext.path):
                shutil.rmtree(ext.path, ignore_errors=True)
            del self.extensions[eid]
            self.save_extensions()
            return True
        return False

    def toggle(self, eid):
        """Включает/выключает расширение"""
        if eid in self.extensions:
            self.extensions[eid].enabled = not self.extensions[eid].enabled
            self.save_extensions()
            return self.extensions[eid].enabled
        return False

    def get(self, eid):
        return self.extensions.get(eid)

    def get_all(self):
        return list(self.extensions.values())

    def get_enabled(self):
        return [e for e in self.extensions.values() if e.enabled]

    def save_extensions(self):
        try:
            os.makedirs("extensions", exist_ok=True)
            with open("extensions.json", "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self.extensions.values()],
                          f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_extensions(self):
        try:
            with open("extensions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    ext = Extension.from_dict(item)
                    self.extensions[ext.id] = ext
        except:
            self.extensions = {}


# ============================================================================
# 📝 МЕНЕДЖЕР ЗАМЕТОК
# ============================================================================
class NotesManager:
    """Менеджер заметок"""

    def __init__(self):
        self.notes = []
        self.load_notes()

    def add_note(self, title, content, category="Общие"):
        note = {
            "id": str(int(time.time() * 1000)),
            "title": title,
            "content": content,
            "category": category,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        self.notes.append(note)
        self.save_notes()
        return note

    def update_note(self, note_id, title=None, content=None):
        for note in self.notes:
            if note["id"] == note_id:
                if title is not None:
                    note["title"] = title
                if content is not None:
                    note["content"] = content
                note["updated"] = datetime.now().isoformat()
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self.save_notes()

    def get_note(self, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None

    def get_notes(self):
        return self.notes

    def search_notes(self, query):
        q = query.lower()
        return [n for n in self.notes
                if q in n["title"].lower() or q in n["content"].lower()]

    def save_notes(self):
        try:
            with open("notes.json", "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_notes(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        except:
            self.notes = []


# ============================================================================
# 📰 RSS-АГРЕГАТОР
# ============================================================================
class RSSReader:
    """RSS-агрегатор"""

    def __init__(self):
        self.feeds = []
        self.load_feeds()

    def add_feed(self, url, title=None):
        if any(f["url"] == url for f in self.feeds):
            return False
        feed = {
            "url": url,
            "title": title or url,
            "added": datetime.now().isoformat()
        }
        self.feeds.append(feed)
        self.save_feeds()
        return True

    def remove_feed(self, url):
        for i, f in enumerate(self.feeds):
            if f["url"] == url:
                del self.feeds[i]
                self.save_feeds()
                return True
        return False

    def get_feeds(self):
        return self.feeds

    def get_feed_urls(self):
        return [f["url"] for f in self.feeds]

    def save_feeds(self):
        try:
            with open("rss_feeds.json", "w", encoding="utf-8") as f:
                json.dump(self.feeds, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_feeds(self):
        try:
            with open("rss_feeds.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # Поддержка старого формата (список URL)
                if data and isinstance(data[0], str):
                    self.feeds = [{"url": u, "title": u} for u in data]
                else:
                    self.feeds = data
        except:
            self.feeds = []


# ============================================================================
# 🔒 МЕНЕДЖЕР РАЗРЕШЕНИЙ
# ============================================================================
class PermissionManager:
    """Менеджер разрешений для сайтов"""

    PERMISSION_NAMES = {
        "geolocation": "📍 Геолокация",
        "notifications": "🔔 Уведомления",
        "camera": "📷 Камера",
        "microphone": "🎤 Микрофон",
        "clipboard": "📋 Буфер обмена",
        "popups": "🪟 Всплывающие окна",
        "autoplay": "▶️ Автовоспроизведение",
        "downloads": "📥 Скачивание",
        "fullscreen": "⛶ Полный экран",
        "screen_capture": "🖥️ Запись экрана"
    }

    def __init__(self):
        self.permissions = {}
        self.load_permissions()

    def request_permission(self, domain, permission, parent=None):
        """Запрашивает разрешение у пользователя"""
        # Проверяем сохранённое разрешение
        if domain in self.permissions:
            if permission in self.permissions[domain]:
                return self.permissions[domain][permission] == "allow"

        # Показываем диалог
        result = self.show_dialog(domain, permission, parent)

        if domain not in self.permissions:
            self.permissions[domain] = {}
        self.permissions[domain][permission] = "allow" if result else "deny"
        self.save_permissions()
        return result

    def show_dialog(self, domain, permission, parent=None):
        perm_name = self.PERMISSION_NAMES.get(permission, permission)

        msg = QMessageBox(parent)
        msg.setWindowTitle(_("permissions_request"))
        msg.setText(_("permissions_text", domain=domain, permission=perm_name))
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(_("permissions_allow"))
        msg.button(QMessageBox.No).setText(_("permissions_deny"))

        return msg.exec_() == QMessageBox.Yes

    def revoke_all(self, domain):
        if domain in self.permissions:
            del self.permissions[domain]
            self.save_permissions()

    def save_permissions(self):
        try:
            with open("permissions.json", "w", encoding="utf-8") as f:
                json.dump(self.permissions, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_permissions(self):
        try:
            with open("permissions.json", "r", encoding="utf-8") as f:
                self.permissions = json.load(f)
        except:
            self.permissions = {}


# ============================================================================
# 🎨 МЕНЕДЖЕР ТЕМ
# ============================================================================
class ThemeManager:
    """Менеджер тем оформления"""

    THEMES = {
        "infinity": {
            "name": "🌌 Infinity",
            "bg": "#0a0a1a",
            "widget": "#1a1a2e",
            "hover": "#2a2a3e",
            "text": "#e0e0e0",
            "text_dim": "#808090",
            "accent": "#00d4ff",
            "accent_hover": "#00eeff",
            "border": "#2a2a3e"
        },
        "dark": {
            "name": "🌙 Dark",
            "bg": "#0d0d0d",
            "widget": "#1a1a1a",
            "hover": "#2a2a2a",
            "text": "#ffffff",
            "text_dim": "#808080",
            "accent": "#00ff88",
            "accent_hover": "#44ffaa",
            "border": "#2a2a2a"
        },
        "light": {
            "name": "☀️ Light",
            "bg": "#f0f0f0",
            "widget": "#ffffff",
            "hover": "#e8e8e8",
            "text": "#222222",
            "text_dim": "#666666",
            "accent": "#0088ff",
            "accent_hover": "#0066cc",
            "border": "#cccccc"
        },
        "neon": {
            "name": "💜 Neon",
            "bg": "#0a001a",
            "widget": "#1a0033",
            "hover": "#2a0044",
            "text": "#ff88ff",
            "text_dim": "#8844aa",
            "accent": "#ff00ff",
            "accent_hover": "#ff44ff",
            "border": "#440066"
        },
        "ocean": {
            "name": "🌊 Ocean",
            "bg": "#001a33",
            "widget": "#002244",
            "hover": "#003366",
            "text": "#aaddff",
            "text_dim": "#5588aa",
            "accent": "#00ddff",
            "accent_hover": "#44eeff",
            "border": "#004488"
        }
    }

    current = "infinity"

    @classmethod
    def get_theme(cls, name=None):
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.current]

    @classmethod
    def set_theme(cls, name):
        if name in cls.THEMES:
            cls.current = name
            return True
        return False

    @classmethod
    def apply(cls, widget, name=None):
        """Применяет тему к виджету"""
        if name and name in cls.THEMES:
            cls.current = name

        t = cls.THEMES[cls.current]

        widget.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background: {t['bg']};
                color: {t['text']};
            }}
            QMenuBar {{
                background: {t['bg']};
                color: {t['text']};
            }}
            QMenuBar::item:selected {{
                background: {t['widget']};
            }}
            QMenu {{
                background: {t['widget']};
                color: {t['text']};
                border: 1px solid {t['border']};
                border-radius: 8px;
            }}
            QMenu::item:selected {{
                background: {t['accent']};
                color: #000;
            }}
            QPushButton {{
                background: {t['widget']};
                color: {t['text']};
                border: 1px solid {t['border']};
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background: {t['hover']};
                border-color: {t['accent']};
            }}
            QLineEdit {{
                background: {t['widget']};
                color: {t['text']};
                border: 1px solid {t['border']};
                border-radius: 8px;
                padding: 8px 12px;
            }}
            QLineEdit:focus {{
                border-color: {t['accent']};
            }}
            QTabWidget::pane {{
                border: none;
                background: {t['bg']};
            }}
            QTabBar::tab {{
                background: {t['widget']};
                color: {t['text_dim']};
                padding: 8px 15px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background: {t['hover']};
                color: {t['text']};
            }}
            QListWidget {{
                background: transparent;
                border: none;
                color: {t['text']};
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background: {t['widget']};
            }}
            QListWidget::item:selected {{
                background: {t['accent']};
                color: #000;
            }}
            QProgressBar {{
                border: none;
                border-radius: 6px;
                background: {t['widget']};
            }}
            QProgressBar::chunk {{
                background: {t['accent']};
                border-radius: 6px;
            }}
            QComboBox {{
                background: {t['widget']};
                color: {t['text']};
                border: 1px solid {t['border']};
                border-radius: 6px;
                padding: 5px 10px;
            }}
            QDialog {{
                background: {t['bg']};
            }}
            QTextEdit {{
                background: {t['widget']};
                color: {t['text']};
                border: 1px solid {t['border']};
                border-radius: 8px;
            }}
        """)
        # ============================================================================
# 🌌 ГЛАВНОЕ ОКНО БРАУЗЕРА
# ============================================================================
class InfinityBrowser(QMainWindow):
    """Главное окно браузера InfinityBrowser"""

    def __init__(self):
        super().__init__()

        # Инициализация менеджеров
        self.adblock = AdBlockManager()
        self.download_manager = DownloadManager()
        self.file_manager = FileManager()
        self.extension_manager = ExtensionManager()
        self.notes_manager = NotesManager()
        self.rss_reader = RSSReader()
        self.permission_manager = PermissionManager()

        # Состояние
        self.is_fullscreen = False
        self.zoom_factor = 1.0
        self.current_url = ""
        self.history = []
        self.bookmarks = []
        self.closed_tabs = []

        # Настройка UI
        self.setup_ui()
        self.setup_menus()
        self.setup_shortcuts()
        ThemeManager.apply(self, "infinity")

        # Загрузка данных
        self.load_bookmarks()
        self.load_history()

        # Создаем первую вкладку
        self.create_tab("https://www.google.com")

        # Статус
        self.show_status(_("status_ready"))

        # Приветствие
        QTimer.singleShot(500, self.show_welcome)

    # ========================================================================
    # 🎨 НАСТРОЙКА UI
    # ========================================================================

    def setup_ui(self):
        """Создает интерфейс главного окна"""
        self.setWindowTitle(_("app_title"))
        self.setGeometry(100, 50, 1400, 900)
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(self.create_icon())

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)

        # Главный вертикальный layout
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя панель
        main_layout.addWidget(self.create_top_panel())

        # Вкладки
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        main_layout.addWidget(self.tab_widget)

        # Статусбар
        main_layout.addWidget(self.create_status_bar())

        # Боковая панель (скрыта по умолчанию)
        self.sidebar = self.create_sidebar()
        self.sidebar.hide()

    def create_icon(self):
        """Создает иконку приложения"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Фон
        painter.setBrush(QColor("#0a0a1a"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 64, 64, 12, 12)

        # Глаз (символ браузера)
        painter.setPen(QPen(QColor("#00d4ff"), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(16, 16, 32, 32)

        # Зрачок
        painter.setBrush(QColor("#00d4ff"))
        painter.drawEllipse(28, 28, 8, 8)

        # Блик
        painter.setBrush(QColor(255, 255, 255, 100))
        painter.drawEllipse(22, 22, 4, 4)

        painter.end()
        return QIcon(pixmap)

    def create_top_panel(self):
        """Создает верхнюю панель с кнопками"""
        widget = QWidget()
        widget.setFixedHeight(52)
        widget.setObjectName("topPanel")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Кнопка НАЗАД
        self.btn_back = self.create_tool_button("◀", _("back"))
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        # Кнопка ВПЕРЕД
        self.btn_forward = self.create_tool_button("▶", _("forward"))
        self.btn_forward.clicked.connect(self.go_forward)
        layout.addWidget(self.btn_forward)

        # Кнопка ОБНОВИТЬ
        self.btn_reload = self.create_tool_button("⟳", _("reload"))
        self.btn_reload.clicked.connect(self.reload)
        layout.addWidget(self.btn_reload)

        # Кнопка ДОМОЙ
        self.btn_home = self.create_tool_button("🏠", _("home"))
        self.btn_home.clicked.connect(self.go_home)
        layout.addWidget(self.btn_home)

        layout.addSpacing(8)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(_("search_placeholder"))
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.setMinimumHeight(36)
        layout.addWidget(self.url_bar, 1)

        # Кнопка ПЕРЕЙТИ
        self.btn_go = QPushButton(_("go"))
        self.btn_go.setFixedHeight(36)
        self.btn_go.setMinimumWidth(60)
        self.btn_go.setCursor(Qt.PointingHandCursor)
        self.btn_go.clicked.connect(self.navigate)
        layout.addWidget(self.btn_go)

        layout.addSpacing(8)

        # Кнопка ЗАКЛАДКА
        self.btn_bookmark = self.create_tool_button("☆", _("bookmark"))
        self.btn_bookmark.clicked.connect(self.toggle_bookmark)
        layout.addWidget(self.btn_bookmark)

        # Кнопка ADBLOCK
        self.btn_adblock = self.create_tool_button("🛡️", _("adblock"))
        self.btn_adblock.clicked.connect(self.toggle_adblock)
        layout.addWidget(self.btn_adblock)

        # Кнопка ТЕМА
        self.btn_theme = self.create_tool_button("🌙", _("theme"))
        self.btn_theme.clicked.connect(self.toggle_theme)
        layout.addWidget(self.btn_theme)

        # Кнопка ПАНЕЛЬ
        self.btn_sidebar = self.create_tool_button("📋", _("sidebar"))
        self.btn_sidebar.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.btn_sidebar)

        # Кнопка ЗАГРУЗКИ
        self.btn_downloads = self.create_tool_button("📥", _("downloads"))
        self.btn_downloads.clicked.connect(self.show_downloads_dialog)
        layout.addWidget(self.btn_downloads)

        # Кнопка ФАЙЛЫ
        self.btn_files = self.create_tool_button("📂", _("files"))
        self.btn_files.clicked.connect(self.show_files_dialog)
        layout.addWidget(self.btn_files)

        # Кнопка РАСШИРЕНИЯ
        self.btn_extensions = self.create_tool_button("🧩", _("extensions"))
        self.btn_extensions.clicked.connect(self.show_extensions_menu)
        layout.addWidget(self.btn_extensions)

        # Кнопка ИНСТРУМЕНТЫ
        self.btn_tools = self.create_tool_button("⚙️", _("tools"))
        self.btn_tools.clicked.connect(self.show_tools_menu)
        layout.addWidget(self.btn_tools)

        return widget

    def create_tool_button(self, text, tooltip):
        """Создает кнопку на панели инструментов"""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(36, 36)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 6px;
                color: #c0c0d0;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 212, 255, 0.15);
                color: #ffffff;
            }
            QPushButton:pressed {
                background: rgba(0, 212, 255, 0.3);
            }
        """)
        return btn

    def create_status_bar(self):
        """Создает статусбар"""
        widget = QWidget()
        widget.setFixedHeight(30)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 2, 12, 2)

        # Статус
        self.status_label = QLabel(_("status_ready"))
        self.status_label.setStyleSheet("font-size: 11px; color: #808090;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Индикатор загрузок
        self.download_indicator = QLabel("📥 0")
        self.download_indicator.setStyleSheet("font-size: 11px; color: #00d4ff;")
        layout.addWidget(self.download_indicator)

        # Индикатор расширений
        self.extensions_indicator = QLabel("🧩 4")
        self.extensions_indicator.setStyleSheet("font-size: 11px; color: #00d4ff;")
        layout.addWidget(self.extensions_indicator)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        # Зум
        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet("font-size: 11px; color: #808090;")
        layout.addWidget(self.zoom_label)

        # SSL
        self.ssl_label = QLabel("🔒")
        self.ssl_label.setStyleSheet("font-size: 14px;")
        self.ssl_label.setToolTip(_("ssl_secure"))
        layout.addWidget(self.ssl_label)

        return widget

    def create_sidebar(self):
        """Создает боковую панель"""
        widget = QWidget()
        widget.setFixedWidth(300)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Вкладки боковой панели
        self.sidebar_tabs = QTabWidget()
        self.sidebar_tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: transparent; }
            QTabBar::tab {
                background: transparent;
                color: #808090;
                padding: 6px 12px;
                border: none;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                color: #00d4ff;
                border-bottom: 2px solid #00d4ff;
            }
        """)

        # === Вкладка "Закладки" ===
        bookmarks_widget = QWidget()
        bookmarks_layout = QVBoxLayout(bookmarks_widget)
        bookmarks_layout.setContentsMargins(0, 0, 0, 0)

        self.bookmarks_search = QLineEdit()
        self.bookmarks_search.setPlaceholderText(_("sidebar_search_bookmarks"))
        self.bookmarks_search.textChanged.connect(self.search_bookmarks)
        bookmarks_layout.addWidget(self.bookmarks_search)

        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.on_bookmark_clicked)
        bookmarks_layout.addWidget(self.bookmarks_list)

        btn_add_bookmark = QPushButton(_("sidebar_add_bookmark"))
        btn_add_bookmark.clicked.connect(self.add_bookmark)
        bookmarks_layout.addWidget(btn_add_bookmark)

        self.sidebar_tabs.addTab(bookmarks_widget, _("sidebar_bookmarks"))

        # === Вкладка "История" ===
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)

        self.history_search = QLineEdit()
        self.history_search.setPlaceholderText(_("sidebar_search_history"))
        self.history_search.textChanged.connect(self.search_history)
        history_layout.addWidget(self.history_search)

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_history_clicked)
        history_layout.addWidget(self.history_list)

        btn_clear = QPushButton(_("sidebar_clear_history"))
        btn_clear.clicked.connect(self.clear_history)
        history_layout.addWidget(btn_clear)

        self.sidebar_tabs.addTab(history_widget, _("sidebar_history"))

        # === Вкладка "Заметки" ===
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(0, 0, 0, 0)

        self.notes_search = QLineEdit()
        self.notes_search.setPlaceholderText(_("sidebar_search_notes"))
        self.notes_search.textChanged.connect(self.search_notes)
        notes_layout.addWidget(self.notes_search)

        self.notes_list = QListWidget()
        self.notes_list.itemDoubleClicked.connect(self.on_note_clicked)
        notes_layout.addWidget(self.notes_list)

        btn_add_note = QPushButton(_("sidebar_add_note"))
        btn_add_note.clicked.connect(self.add_note_dialog)
        notes_layout.addWidget(btn_add_note)

        self.sidebar_tabs.addTab(notes_widget, _("sidebar_notes"))

        # === Вкладка "RSS" ===
        rss_widget = QWidget()
        rss_layout = QVBoxLayout(rss_widget)
        rss_layout.setContentsMargins(0, 0, 0, 0)

        rss_input_layout = QHBoxLayout()
        self.rss_input = QLineEdit()
        self.rss_input.setPlaceholderText(_("rss_placeholder"))
        rss_input_layout.addWidget(self.rss_input)

        btn_add_rss = QPushButton("➕")
        btn_add_rss.setFixedWidth(36)
        btn_add_rss.clicked.connect(self.add_rss_feed)
        rss_input_layout.addWidget(btn_add_rss)

        rss_layout.addLayout(rss_input_layout)

        self.rss_list = QListWidget()
        self.rss_list.itemDoubleClicked.connect(self.on_rss_clicked)
        rss_layout.addWidget(self.rss_list)

        self.sidebar_tabs.addTab(rss_widget, _("sidebar_rss"))

        # === Вкладка "Расширения" ===
        ext_widget = QWidget()
        ext_layout = QVBoxLayout(ext_widget)
        ext_layout.setContentsMargins(0, 0, 0, 0)

        self.extensions_list = QListWidget()
        self.extensions_list.itemDoubleClicked.connect(self.on_extension_double_clicked)
        ext_layout.addWidget(self.extensions_list)

        btn_install_ext = QPushButton(_("extensions_install"))
        btn_install_ext.clicked.connect(self.install_extension_dialog)
        ext_layout.addWidget(btn_install_ext)

        self.sidebar_tabs.addTab(ext_widget, _("sidebar_extensions"))

        layout.addWidget(self.sidebar_tabs)
        return widget

    # ========================================================================
    # 📋 МЕНЮ
    # ========================================================================

    def setup_menus(self):
        """Создает меню"""
        menubar = self.menuBar()

        # === Файл ===
        file_menu = menubar.addMenu(_("menu_file"))
        file_menu.addAction(_("menu_new_tab"), self.create_tab, "Ctrl+T")
        file_menu.addAction(_("menu_new_window"), self.new_window, "Ctrl+N")
        file_menu.addAction(_("menu_incognito"), self.new_incognito, "Ctrl+Shift+N")
        file_menu.addSeparator()
        file_menu.addAction(_("menu_downloads"), self.show_downloads_dialog, "Ctrl+J")
        file_menu.addAction(_("menu_files"), self.show_files_dialog)
        file_menu.addAction(_("menu_save"), self.save_page, "Ctrl+S")
        file_menu.addAction(_("menu_print"), self.print_page, "Ctrl+P")
        file_menu.addSeparator()
        file_menu.addAction(_("menu_exit"), self.close, "Ctrl+Q")

        # === Вкладки ===
        tabs_menu = menubar.addMenu(_("menu_tabs"))
        tabs_menu.addAction(_("menu_new_tab"), self.create_tab, "Ctrl+T")
        tabs_menu.addAction(_("menu_close_tab"), self.close_current_tab, "Ctrl+W")
        tabs_menu.addAction(_("menu_restore_tab"), self.restore_tab, "Ctrl+Shift+T")
        tabs_menu.addSeparator()
        tabs_menu.addAction(_("menu_next_tab"), self.next_tab, "Ctrl+Tab")
        tabs_menu.addAction(_("menu_prev_tab"), self.prev_tab, "Ctrl+Shift+Tab")

        # === Инструменты ===
        tools_menu = menubar.addMenu(_("menu_tools"))
        tools_menu.addAction(_("menu_downloads"), self.show_downloads_dialog)
        tools_menu.addAction(_("menu_files"), self.show_files_dialog)
        tools_menu.addAction(_("menu_notes"), self.toggle_sidebar)
        tools_menu.addAction(_("menu_rss"), self.toggle_sidebar)
        tools_menu.addSeparator()
        tools_menu.addAction(_("menu_extensions"), self.show_extensions_menu)
        tools_menu.addAction(_("menu_permissions"), self.show_permissions_dialog)
        tools_menu.addAction(_("menu_themes"), self.show_themes)
        tools_menu.addAction(_("menu_settings"), self.show_settings, "Ctrl+,")

        # === Помощь ===
        help_menu = menubar.addMenu(_("menu_help"))
        help_menu.addAction(_("menu_help_item"), self.show_help, "F1")
        help_menu.addAction(_("menu_about"), self.show_about)

    # ========================================================================
    # ⌨️ ГОРЯЧИЕ КЛАВИШИ
    # ========================================================================

    def setup_shortcuts(self):
        """Настраивает горячие клавиши"""
        shortcuts = [
            ("Ctrl+T", self.create_tab),
            ("Ctrl+W", self.close_current_tab),
            ("Ctrl+Shift+T", self.restore_tab),
            ("Ctrl+Tab", self.next_tab),
            ("Ctrl+Shift+Tab", self.prev_tab),
            ("Ctrl+Q", self.close),
            ("Ctrl+S", self.save_page),
            ("Ctrl+P", self.print_page),
            ("Ctrl+J", self.show_downloads_dialog),
            ("Ctrl+D", self.add_bookmark),
            ("Ctrl+H", self.toggle_sidebar),
            ("Ctrl+,", self.show_settings),
            ("F5", self.reload),
            ("F11", self.toggle_fullscreen),
            ("F12", self.show_devtools),
            ("Ctrl++", lambda: self.zoom(0.1)),
            ("Ctrl+-", lambda: self.zoom(-0.1)),
            ("Ctrl+0", self.reset_zoom),
            ("Ctrl+F", self.find_on_page),
            ("Alt+Home", self.go_home),
            ("Alt+Left", self.go_back),
            ("Alt+Right", self.go_forward),
        ]

        for shortcut, callback in shortcuts:
            action = QAction(self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(callback)
            self.addAction(action)

    # ========================================================================
    # 🔥 СОЗДАНИЕ СТРАНИЦЫ С ПЕРЕХВАТОМ ССЫЛОК
    # ========================================================================

    def make_new_page(self, parent_view=None):
        """Создает новую страницу с полной настройкой и перехватом ссылок"""
        view = QWebEngineView()
        page = view.page()

        # Подключаем сигналы
        page.loadProgress.connect(self.on_load_progress)
        page.titleChanged.connect(self.on_title_changed)
        page.urlChanged.connect(self.on_url_changed)
        page.iconChanged.connect(self.on_icon_changed)
        page.fullScreenRequested.connect(self.on_fullscreen_request)
        page.featurePermissionRequested.connect(self.on_feature_permission)
        page.profile().downloadRequested.connect(self.on_download_requested)

        # 🔥 ГЛАВНОЕ: перехват новых окон (target=_blank, window.open)
        page.createWindow = lambda wtype, v=view: self.handle_new_window(v, wtype)

        # Контекстное меню
        view.setContextMenuPolicy(Qt.CustomContextMenu)
        view.customContextMenuRequested.connect(self.show_context_menu)

        # Middle-click handler
        self.setup_middle_click(view)

        # Инъекция расширений после загрузки
        def on_finished(ok):
            if ok:
                for ext in self.extension_manager.get_enabled():
                    if ext.script:
                        page.runJavaScript(ext.script)

        page.loadFinished.connect(on_finished)

        return view

    def create_tab(self, url="https://www.google.com"):
        """Создает новую вкладку"""
        view = self.make_new_page()

        if isinstance(url, str):
            view.setUrl(QUrl(url))
        else:
            view.setUrl(url)

        idx = self.tab_widget.addTab(view, _("tab_new"))
        self.tab_widget.setCurrentIndex(idx)
        return view

    def handle_new_window(self, parent_view, window_type):
        """🔥 ОБРАБОТКА target=_blank и window.open() → новая вкладка"""
        new_view = self.make_new_page(parent_view)

        idx = self.tab_widget.addTab(new_view, _("tab_from_link"))
        self.tab_widget.setCurrentIndex(idx)

        self.show_status(_("tab_from_link"))

        # Возвращаем новую страницу, чтобы QtWebEngine знал куда загружать
        return new_view.page()

    def create_new_tab_from_url(self, url):
        """Создает новую вкладку с указанным URL (для Ctrl+Click и MMB)"""
        if not url:
            return None

        url_str = url.toString() if isinstance(url, QUrl) else str(url)

        if url_str in ("about:blank", "", "about:blank#blocked"):
            return None

        new_view = self.make_new_page()
        new_view.setUrl(QUrl(url_str))

        idx = self.tab_widget.addTab(new_view, _("tab_from_link"))
        self.tab_widget.setCurrentIndex(idx)

        self.show_status(_("tab_from_link"))
        return new_view

    def setup_middle_click(self, view):
        """🔥 Перехват средней кнопки мыши → открытие ссылки в новой вкладке"""
        browser = self

        class MiddleClickFilter(QObject):
            def eventFilter(self, obj, event):
                if event.type() == QEvent.MouseButtonPress:
                    if event.button() == Qt.MiddleButton:
                        pos = event.pos()
                        script = f"""
                        (function() {{
                            var el = document.elementFromPoint({pos.x()}, {pos.y()});
                            while (el && el.tagName !== 'A') {{
                                el = el.parentElement;
                            }}
                            return el ? el.href : null;
                        }})();
                        """

                        def on_result(href):
                            if href:
                                browser.create_new_tab_from_url(QUrl(href))

                        view.page().runJavaScript(script, on_result)
                        return True

                return super().eventFilter(obj, event)

        filter_obj = MiddleClickFilter()
        view.installEventFilter(filter_obj)

    # ========================================================================
    # 🌐 НАВИГАЦИЯ
    # ========================================================================

    def navigate(self):
        """Переход по URL из адресной строки"""
        text = self.url_bar.text().strip()
        if not text:
            return

        # Если не URL - ищем в Google
        if not text.startswith(("http://", "https://", "file://", "about:")):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text = f"https://www.google.com/search?q={text.replace(' ', '+')}"

        view = self.get_current_view()
        if view:
            view.setUrl(QUrl(text))
            self.add_to_history(text)

    def go_back(self):
        view = self.get_current_view()
        if view:
            view.back()

    def go_forward(self):
        view = self.get_current_view()
        if view:
            view.forward()

    def reload(self):
        view = self.get_current_view()
        if view:
            view.reload()

    def go_home(self):
        self.url_bar.setText("https://www.google.com")
        self.navigate()

    def get_current_view(self):
        """Возвращает текущий QWebEngineView"""
        return self.tab_widget.currentWidget()

    def get_current_page(self):
        """Возвращает текущую QWebEnginePage"""
        view = self.get_current_view()
        return view.page() if view else None

    # ========================================================================
    # 📑 УПРАВЛЕНИЕ ВКЛАДКАМИ
    # ========================================================================

    def close_tab(self, idx):
        """Закрывает вкладку"""
        if idx < 0:
            return

        widget = self.tab_widget.widget(idx)
        if widget:
            self.closed_tabs.append(widget)
            if len(self.closed_tabs) > 10:
                self.closed_tabs.pop(0)

        self.tab_widget.removeTab(idx)

        # Если вкладок не осталось - создаем новую
        if self.tab_widget.count() == 0:
            self.create_tab()

    def close_current_tab(self):
        self.close_tab(self.tab_widget.currentIndex())

    def restore_tab(self):
        """Восстанавливает последнюю закрытую вкладку"""
        if self.closed_tabs:
            view = self.closed_tabs.pop()
            url = view.url().toString()
            self.create_tab(url)
            self.show_status(_("tab_restored"))

    def next_tab(self):
        if self.tab_widget.count() > 1:
            idx = (self.tab_widget.currentIndex() + 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(idx)

    def prev_tab(self):
        if self.tab_widget.count() > 1:
            idx = (self.tab_widget.currentIndex() - 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(idx)

    def on_tab_changed(self, idx):
        """Обработка смены вкладки"""
        view = self.tab_widget.widget(idx)
        if view:
            self.on_url_changed(view.url())
            self.on_title_changed(view.page().title())

    # ========================================================================
    # 📊 ИСТОРИЯ
    # ========================================================================

    def add_to_history(self, url):
        """Добавляет URL в историю"""
        title = self.get_current_page().title() if self.get_current_page() else url

        entry = {
            "url": url,
            "title": title or url,
            "timestamp": datetime.now().isoformat()
        }

        # Удаляем дубликат, если есть
        self.history = [h for h in self.history if h["url"] != url]
        self.history.insert(0, entry)

        if len(self.history) > 1000:
            self.history = self.history[:1000]

        self.save_history()
        self.update_history_list()

    def load_history(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except:
            self.history = []
        self.update_history_list()

    def save_history(self):
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_list()
        self.show_status(_("notification_history_cleared"))

    def update_history_list(self):
        if hasattr(self, "history_list"):
            self.history_list.clear()
            for h in self.history[:50]:
                self.history_list.addItem(f"{h['title']} - {h['url']}")

    def search_history(self, text):
        if hasattr(self, "history_list"):
            self.history_list.clear()
            if not text:
                self.update_history_list()
                return
            for h in self.history[:50]:
                if text.lower() in h["title"].lower() or text.lower() in h["url"].lower():
                    self.history_list.addItem(f"{h['title']} - {h['url']}")

    def on_history_clicked(self, item):
        text = item.text()
        if " - " in text:
            url = text.split(" - ")[-1]
            self.url_bar.setText(url)
            self.navigate()

    # ========================================================================
    # ⭐ ЗАКЛАДКИ
    # ========================================================================

    def add_bookmark(self):
        """Добавляет закладку"""
        view = self.get_current_view()
        if not view:
            return

        url = view.url().toString()
        title = view.page().title() or url

        if any(b["url"] == url for b in self.bookmarks):
            self.show_status("⭐ Уже в закладках")
            return

        self.bookmarks.append({"url": url, "title": title})
        self.save_bookmarks()
        self.update_bookmarks_list()
        self.btn_bookmark.setText("★")
        self.show_status(_("bookmark_added"))

    def toggle_bookmark(self):
        view = self.get_current_view()
        if not view:
            return

        url = view.url().toString()

        if any(b["url"] == url for b in self.bookmarks):
            self.bookmarks = [b for b in self.bookmarks if b["url"] != url]
            self.save_bookmarks()
            self.update_bookmarks_list()
            self.btn_bookmark.setText("☆")
            self.show_status(_("bookmark_removed"))
        else:
            self.add_bookmark()

    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r", encoding="utf-8") as f:
                self.bookmarks = json.load(f)
        except:
            self.bookmarks = []
        self.update_bookmarks_list()

    def save_bookmarks(self):
        try:
            with open("bookmarks.json", "w", encoding="utf-8") as f:
                json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
        except:
            pass

    def update_bookmarks_list(self):
        if hasattr(self, "bookmarks_list"):
            self.bookmarks_list.clear()
            for b in self.bookmarks:
                self.bookmarks_list.addItem(f"{b['title']} - {b['url']}")

    def search_bookmarks(self, text):
        if hasattr(self, "bookmarks_list"):
            self.bookmarks_list.clear()
            if not text:
                self.update_bookmarks_list()
                return
            for b in self.bookmarks:
                if text.lower() in b["title"].lower() or text.lower() in b["url"].lower():
                    self.bookmarks_list.addItem(f"{b['title']} - {b['url']}")

    def on_bookmark_clicked(self, item):
        text = item.text()
        if " - " in text:
            url = text.split(" - ")[-1]
            self.url_bar.setText(url)
            self.navigate()

    # ========================================================================
    # 📝 ЗАМЕТКИ
    # ========================================================================

    def add_note_dialog(self):
        """Диалог создания заметки"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("notes_new_title"))
        dialog.resize(400, 350)

        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel(_("notes_title_label")))
        title_edit = QLineEdit()
        layout.addWidget(title_edit)

        layout.addWidget(QLabel(_("notes_content_label")))
        content_edit = QTextEdit()
        layout.addWidget(content_edit)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton(_("notes_save"))
        btn_save.clicked.connect(dialog.accept)
        btn_layout.addWidget(btn_save)

        btn_cancel = QPushButton(_("notes_cancel"))
        btn_cancel.clicked.connect(dialog.reject)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)

        if dialog.exec_() == QDialog.Accepted:
            title = title_edit.text().strip() or "Без названия"
            content = content_edit.toPlainText()
            self.notes_manager.add_note(title, content)
            self.update_notes_list()
            self.show_status(_("notes_created", title=title))

    def update_notes_list(self):
        if hasattr(self, "notes_list"):
            self.notes_list.clear()
            for note in self.notes_manager.get_notes():
                item = QListWidgetItem(f"📝 {note['title']}")
                item.setData(Qt.UserRole, note["id"])
                self.notes_list.addItem(item)

    def search_notes(self, text):
        if hasattr(self, "notes_list"):
            self.notes_list.clear()
            if not text:
                self.update_notes_list()
                return
            for note in self.notes_manager.search_notes(text):
                item = QListWidgetItem(f"📝 {note['title']}")
                item.setData(Qt.UserRole, note["id"])
                self.notes_list.addItem(item)

    def on_note_clicked(self, item):
        note_id = item.data(Qt.UserRole)
        note = self.notes_manager.get_note(note_id)
        if note:
            QMessageBox.information(self, note["title"], note["content"])

    # ========================================================================
    # 📰 RSS
    # ========================================================================

    def add_rss_feed(self):
        """Добавляет RSS-ленту"""
        url = self.rss_input.text().strip()
        if not url:
            return

        if self.rss_reader.add_feed(url):
            self.update_rss_list()
            self.rss_input.clear()
            self.show_status(_("rss_added", url=url))
        else:
            self.show_status(_("rss_exists"))

    def update_rss_list(self):
        if hasattr(self, "rss_list"):
            self.rss_list.clear()
            for feed in self.rss_reader.get_feeds():
                self.rss_list.addItem(f"📰 {feed['title']}")

    def on_rss_clicked(self, item):
        url = item.text().replace("📰 ", "")
        self.url_bar.setText(url)
        self.navigate()

    # ========================================================================
    # 🧩 РАСШИРЕНИЯ
    # ========================================================================

    def show_extensions_menu(self):
        """Показывает меню расширений"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 5px;
                min-width: 220px;
            }
            QMenu::item { padding: 8px 25px; border-radius: 4px; }
            QMenu::item:selected { background: #00d4ff; color: #000; }
            QMenu::separator {
                height: 1px;
                background: #2a2a3e;
                margin: 4px 10px;
            }
        """)

        menu.addAction(_("extensions_manage"), self.show_extensions_dialog)
        menu.addAction(_("extensions_install_zip"), self.install_from_zip)
        menu.addAction(_("extensions_install_folder"), self.install_from_folder)
        menu.addAction(_("extensions_install_js"), self.install_from_js)
        menu.addSeparator()

        # Список расширений с подменю
        for ext in self.extension_manager.get_all():
            status = "✅" if ext.enabled else "❌"
            submenu = QMenu(f"{status} {ext.name}", menu)
            submenu.setStyleSheet(menu.styleSheet())

            submenu.addAction(_("extensions_open"),
                              lambda checked, eid=ext.id: self.show_extension_popup(eid))
            submenu.addAction(_("extensions_toggle"),
                              lambda checked, eid=ext.id: self.toggle_extension(eid))
            submenu.addAction(_("extensions_code"),
                              lambda checked, eid=ext.id: self.show_extension_code(eid))
            submenu.addAction(_("extensions_options"),
                              lambda checked, eid=ext.id: self.show_extension_options(eid))

            if ext.id not in self.extension_manager.BUILTIN_IDS:
                submenu.addSeparator()
                submenu.addAction(_("extensions_uninstall"),
                                  lambda checked, eid=ext.id: self.uninstall_extension(eid))

            menu.addMenu(submenu)

        menu.exec_(self.btn_extensions.mapToGlobal(
            self.btn_extensions.rect().bottomLeft()
        ))

    def show_extensions_dialog(self):
        """Показывает диалог управления расширениями"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("extensions_title"))
        dialog.resize(550, 450)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1a1a2e;
            }
            QListWidget::item:hover { background: #1a1a2e; }
        """)

        for ext in self.extension_manager.get_all():
            status = "🟢" if ext.enabled else "🔴"
            item = QListWidgetItem(f"{status} {ext.name} v{ext.version}")
            item.setData(Qt.UserRole, ext.id)
            item.setToolTip(f"Автор: {ext.author}\n{ext.description}")
            list_widget.addItem(item)

        list_widget.itemDoubleClicked.connect(
            lambda item: self.show_extension_popup(item.data(Qt.UserRole))
        )

        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()

        btn_open = QPushButton(_("extensions_open"))
        btn_open.clicked.connect(
            lambda: self.show_extension_popup(
                list_widget.currentItem().data(Qt.UserRole)
            ) if list_widget.currentItem() else None
        )
        btn_layout.addWidget(btn_open)

        btn_toggle = QPushButton(_("extensions_toggle"))
        btn_toggle.clicked.connect(
            lambda: self.toggle_extension(
                list_widget.currentItem().data(Qt.UserRole)
            ) if list_widget.currentItem() else None
        )
        btn_layout.addWidget(btn_toggle)

        btn_uninstall = QPushButton(_("extensions_uninstall"))
        btn_uninstall.clicked.connect(
            lambda: self.uninstall_extension(
                list_widget.currentItem().data(Qt.UserRole)
            ) if list_widget.currentItem() else None
        )
        btn_layout.addWidget(btn_uninstall)

        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)
        dialog.exec_()

    def toggle_extension(self, eid):
        """Включает/выключает расширение"""
        enabled = self.extension_manager.toggle(eid)
        ext = self.extension_manager.get(eid)

        if ext:
            if enabled:
                self.show_status(_("extensions_enabled", name=ext.name))
            else:
                self.show_status(_("extensions_disabled", name=ext.name))

        self.update_extensions_list()
        self.update_extensions_indicator()

    def uninstall_extension(self, eid):
        """Удаляет расширение"""
        ext = self.extension_manager.get(eid)
        if not ext:
            return

        if eid in self.extension_manager.BUILTIN_IDS:
            QMessageBox.warning(self, "❌", _("extensions_cannot_uninstall"))
            return

        reply = QMessageBox.question(
            self, _("extensions_uninstall"),
            _("extensions_uninstall_confirm", name=ext.name),
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.extension_manager.uninstall(eid):
                self.update_extensions_list()
                self.update_extensions_indicator()
                self.show_status(_("extensions_uninstalled", name=ext.name))

    def show_extension_popup(self, eid):
        """Показывает всплывающее окно расширения"""
        ext = self.extension_manager.get(eid)
        if not ext:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"🧩 {ext.name}")
        dialog.resize(350, 450)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        webview = QWebEngineView()
        webview.page().toggleExtension = lambda: self.toggle_extension(eid)
        webview.page().viewExtensionCode = lambda: self.show_extension_code(eid)
        webview.page().show_extension_options = lambda: self.show_extension_options(eid)
        webview.page().uninstallExtension = lambda: self.uninstall_extension(eid)

        webview.setHtml(ext.get_popup_html())
        layout.addWidget(webview)

        dialog.exec_()

    def show_extension_code(self, eid):
        """Показывает код расширения"""
        ext = self.extension_manager.get(eid)
        if not ext:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"📄 {ext.name}")
        dialog.resize(700, 500)

        layout = QVBoxLayout(dialog)

        info = QLabel(f"<b>{ext.name}</b> v{ext.version} - {ext.author}")
        info.setStyleSheet("color: #00d4ff; padding: 5px;")
        layout.addWidget(info)

        code_edit = QTextEdit()
        code_edit.setPlainText(ext.script or "// Код не найден")
        code_edit.setFont(QFont("Courier New", 11))
        code_edit.setReadOnly(True)
        layout.addWidget(code_edit)

        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec_()

    def show_extension_options(self, eid):
        """Показывает настройки расширения"""
        ext = self.extension_manager.get(eid)
        if not ext:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"⚙️ {ext.name}")
        dialog.resize(500, 450)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        webview = QWebEngineView()
        webview.setHtml(ext.get_options_html())
        layout.addWidget(webview)

        dialog.exec_()

    def update_extensions_list(self):
        if hasattr(self, "extensions_list"):
            self.extensions_list.clear()
            for ext in self.extension_manager.get_all():
                status = "🟢" if ext.enabled else "🔴"
                item = QListWidgetItem(f"{status} {ext.name}")
                item.setData(Qt.UserRole, ext.id)
                self.extensions_list.addItem(item)

    def on_extension_double_clicked(self, item):
        eid = item.data(Qt.UserRole)
        if eid:
            self.show_extension_popup(eid)

    def update_extensions_indicator(self):
        count = len(self.extension_manager.get_enabled())
        if hasattr(self, "extensions_indicator"):
            self.extensions_indicator.setText(_("indicator_extensions", count=count))

    def install_extension_dialog(self):
        """Диалог установки расширения"""
        menu = QMenu(self)
        menu.addAction(_("extensions_install_zip"), self.install_from_zip)
        menu.addAction(_("extensions_install_folder"), self.install_from_folder)
        menu.addAction(_("extensions_install_js"), self.install_from_js)
        menu.exec_(QCursor.pos())

    def install_from_zip(self):
        """Установка расширения из ZIP"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите ZIP-архив", "",
            "ZIP архивы (*.zip);;Все файлы (*.*)"
        )
        if not filename:
            return

        ext = self.extension_manager.install_from_zip(filename)
        if ext:
            self.update_extensions_list()
            self.update_extensions_indicator()
            QMessageBox.information(self, "✅",
                                     _("extensions_installed", name=ext.name))
        else:
            QMessageBox.warning(self, "❌", "Не удалось установить расширение")

    def install_from_folder(self):
        """Установка расширения из папки"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку расширения")
        if not folder:
            return

        ext = self.extension_manager.install_from_folder(folder)
        if ext:
            self.update_extensions_list()
            self.update_extensions_indicator()
            QMessageBox.information(self, "✅",
                                     _("extensions_installed", name=ext.name))
        else:
            QMessageBox.warning(self, "❌", "Не удалось установить расширение")

    def install_from_js(self):
        """Установка расширения из JS-файла"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите JS-файл", "",
            "JavaScript файлы (*.js);;Все файлы (*.*)"
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()

            name = os.path.basename(filename).replace(".js", "")
            ext = self.extension_manager.install_from_js(name, code)

            if ext:
                self.update_extensions_list()
                self.update_extensions_indicator()
                QMessageBox.information(self, "✅",
                                         _("extensions_installed", name=ext.name))
        except Exception as e:
            QMessageBox.critical(self, "❌", f"Ошибка: {e}")
                # ========================================================================
    # 📥 ЗАГРУЗКИ И ФАЙЛЫ
    # ========================================================================

    def show_downloads_dialog(self):
        """Показывает менеджер загрузок"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("downloads_title"))
        dialog.resize(700, 500)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #1a1a2e;
            }
            QListWidget::item:hover { background: #1a1a2e; }
        """)

        for d in self.download_manager.get_downloads():
            status_icons = {
                "pending": "⏳", "downloading": "📥",
                "paused": "⏸️", "completed": "✅",
                "failed": "❌", "cancelled": "🚫"
            }
            icon = status_icons.get(d["status"], "❓")
            progress = f"{int(d['progress'])}%" if d["progress"] > 0 else "0%"
            size = self.file_manager.format_size(d["size"]) if d["size"] > 0 else "?"

            item_text = f"{icon} {d['filename']} - {progress} ({size})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, d["id"])
            list_widget.addItem(item)

        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()

        btn_open = QPushButton(_("downloads_open"))
        btn_open.clicked.connect(lambda: self._open_selected_download(list_widget))
        btn_layout.addWidget(btn_open)

        btn_folder = QPushButton(_("downloads_folder"))
        btn_folder.clicked.connect(lambda: self._open_download_folder(list_widget))
        btn_layout.addWidget(btn_folder)

        btn_remove = QPushButton(_("downloads_remove"))
        btn_remove.clicked.connect(lambda: self._remove_download(list_widget))
        btn_layout.addWidget(btn_remove)

        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)
        dialog.exec_()

    def _open_selected_download(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.open_file(current.data(Qt.UserRole))

    def _open_download_folder(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.open_folder(current.data(Qt.UserRole))

    def _remove_download(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.remove_download(current.data(Qt.UserRole))
            list_widget.takeItem(list_widget.row(current))

    def show_files_dialog(self):
        """Показывает менеджер файлов"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("files_title"))
        dialog.resize(800, 500)

        layout = QVBoxLayout(dialog)

        # Верхняя панель с категорией
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        top_layout.addWidget(QLabel(_("files_category")))
        category_combo = QComboBox()
        category_combo.addItems(self.file_manager.categories.keys())
        top_layout.addWidget(category_combo)

        top_layout.addSpacing(20)

        search_edit = QLineEdit()
        search_edit.setPlaceholderText(_("files_search"))
        top_layout.addWidget(search_edit)

        top_layout.addStretch()

        btn_open_folder = QPushButton(_("files_open_folder"))
        btn_open_folder.clicked.connect(self.file_manager.open_folder)
        top_layout.addWidget(btn_open_folder)

        layout.addWidget(top_widget)

        # Список файлов
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #1a1a2e;
            }
            QListWidget::item:hover { background: #1a1a2e; }
        """)

        def update_list():
            list_widget.clear()
            cat = category_combo.currentText()
            search = search_edit.text().lower()

            for f in self.file_manager.get_files(cat):
                if search and search not in f["name"].lower():
                    continue
                size = self.file_manager.format_size(f["size"])
                item_text = f"{f['category']} {f['name']} ({size})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, f["name"])
                list_widget.addItem(item)

        category_combo.currentTextChanged.connect(lambda: update_list())
        search_edit.textChanged.connect(lambda: update_list())
        update_list()

        list_widget.itemDoubleClicked.connect(
            lambda item: self.file_manager.open_file(item.data(Qt.UserRole))
        )

        layout.addWidget(list_widget)

        # Кнопки
        btn_layout = QHBoxLayout()

        btn_open = QPushButton(_("files_open"))
        btn_open.clicked.connect(
            lambda: self.file_manager.open_file(
                list_widget.currentItem().data(Qt.UserRole)
            ) if list_widget.currentItem() else None
        )
        btn_layout.addWidget(btn_open)

        btn_delete = QPushButton(_("files_delete"))
        btn_delete.clicked.connect(
            lambda: self._delete_file(list_widget)
        )
        btn_layout.addWidget(btn_delete)

        btn_close = QPushButton(_("files_close"))
        btn_close.clicked.connect(dialog.close)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)
        dialog.exec_()

    def _delete_file(self, list_widget):
        current = list_widget.currentItem()
        if not current:
            return

        filename = current.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, _("files_delete"),
            f"Удалить '{filename}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.file_manager.delete_file(filename):
                self.show_status(_("files_deleted", filename=filename))
                list_widget.takeItem(list_widget.row(current))

    # ========================================================================
    # 🎨 ТЕМЫ
    # ========================================================================

    def toggle_theme(self):
        """Переключает тему"""
        themes = list(ThemeManager.THEMES.keys())
        current = themes.index(ThemeManager.current)
        next_idx = (current + 1) % len(themes)
        ThemeManager.apply(self, themes[next_idx])
        self.show_status(_("notification_theme_changed"))

    def show_themes(self):
        """Диалог выбора темы"""
        theme_names = [ThemeManager.THEMES[k]["name"] for k in ThemeManager.THEMES]
        theme, ok = QInputDialog.getItem(
            self, _("themes_title"), _("themes_select"),
            theme_names, 0, False
        )

        if ok and theme:
            for key, value in ThemeManager.THEMES.items():
                if value["name"] == theme:
                    ThemeManager.apply(self, key)
                    self.show_status(_("notification_theme_changed"))
                    break

    # ========================================================================
    # 🛡️ ADBLOCK
    # ========================================================================

    def toggle_adblock(self):
        """Включает/выключает AdBlock"""
        enabled = self.adblock.toggle()
        if enabled:
            self.btn_adblock.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 212, 255, 0.3);
                    border: none;
                    border-radius: 6px;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            self.show_status(_("adblock_on"))
        else:
            self.btn_adblock.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 6px;
                    color: #c0c0d0;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            self.show_status(_("adblock_off"))

    # ========================================================================
    # 📋 БОКОВАЯ ПАНЕЛЬ
    # ========================================================================

    def toggle_sidebar(self):
        """Показывает/скрывает боковую панель"""
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()
            self.update_bookmarks_list()
            self.update_history_list()
            self.update_notes_list()
            self.update_rss_list()
            self.update_extensions_list()

    # ========================================================================
    # 🔍 ЗУМ И ПОИСК
    # ========================================================================

    def toggle_fullscreen(self):
        """Переключает полноэкранный режим"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

    def zoom(self, delta):
        """Изменяет масштаб"""
        self.zoom_factor += delta
        self.zoom_factor = max(0.25, min(5.0, self.zoom_factor))

        view = self.get_current_view()
        if view:
            view.setZoomFactor(self.zoom_factor)

        self.zoom_label.setText(f"{int(self.zoom_factor * 100)}%")

    def reset_zoom(self):
        """Сбрасывает масштаб"""
        self.zoom_factor = 1.0
        view = self.get_current_view()
        if view:
            view.setZoomFactor(1.0)
        self.zoom_label.setText("100%")

    def find_on_page(self):
        """Поиск на странице"""
        text, ok = QInputDialog.getText(self, _("find_title"), _("find_text"))
        if ok and text:
            view = self.get_current_view()
            if view:
                view.page().findText(text)
                self.show_status(_("find_result", text=text))

    # ========================================================================
    # 💾 СОХРАНЕНИЕ И ПЕЧАТЬ
    # ========================================================================

    def save_page(self):
        """Сохраняет страницу"""
        view = self.get_current_view()
        if not view:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, _("save_page_title"), "", _("save_page_filter")
        )

        if filename:
            def on_html(html):
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(html)
                    self.show_status(_("save_page_saved", filename=filename))
                except Exception as e:
                    self.show_status(_("save_page_error", error=str(e)))

            view.page().toHtml(on_html)

    def print_page(self):
        """Печатает страницу в PDF"""
        view = self.get_current_view()
        if view:
            view.page().printToPdf()
            self.show_status(_("print_started"))

    # ========================================================================
    # 🪟 НОВЫЕ ОКНА
    # ========================================================================

    def new_window(self):
        """Создает новое окно браузера"""
        window = InfinityBrowser()
        window.show()

    def new_incognito(self):
        """Создает окно инкогнито"""
        window = InfinityBrowser()
        window.setWindowTitle(_("incognito_title"))
        window.show()
        window.show_status(_("incognito_activated"))

    # ========================================================================
    # 🔧 КОНТЕКСТНОЕ МЕНЮ
    # ========================================================================

    def show_context_menu(self, pos):
        """Показывает контекстное меню на странице"""
        view = self.get_current_view()
        if not view:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item { padding: 8px 25px; border-radius: 4px; }
            QMenu::item:selected { background: #00d4ff; color: #000; }
        """)

        menu.addAction(_("back"), view.back)
        menu.addAction(_("forward"), view.forward)
        menu.addAction(_("reload"), view.reload)
        menu.addSeparator()
        menu.addAction(_("bookmark"), self.add_bookmark)
        menu.addAction("📋 " + _("notification_copied"),
                       lambda: QApplication.clipboard().setText(view.url().toString()))
        menu.addAction(_("menu_save"), self.save_page)
        menu.addSeparator()
        menu.addAction(_("find_title"), self.find_on_page)

        menu.exec_(view.mapToGlobal(pos))

    # ========================================================================
    # 🛠️ ИНСТРУМЕНТЫ РАЗРАБОТЧИКА (F12)
    # ========================================================================

    def show_devtools(self):
        """Открывает инструменты разработчика"""
        view = self.get_current_view()
        if not view:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"🛠️ DevTools - {view.page().title()}")
        dialog.resize(900, 600)

        layout = QVBoxLayout(dialog)
        tabs = QTabWidget()

        # ===== Вкладка "Элементы" =====
        elements_text = QTextEdit()
        elements_text.setFont(QFont("Courier New", 10))
        elements_text.setReadOnly(True)

        def load_html(html):
            elements_text.setPlainText(html)

        view.page().toHtml(load_html)
        tabs.addTab(elements_text, "📄 Элементы")

        # ===== Вкладка "Консоль" =====
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)

        console_output = QTextEdit()
        console_output.setFont(QFont("Courier New", 10))
        console_output.setReadOnly(True)
        console_layout.addWidget(console_output)

        console_input = QLineEdit()
        console_input.setPlaceholderText("Введите JavaScript...")

        def run_js():
            code = console_input.text().strip()
            if not code:
                return

            console_output.append(f">>> {code}")

            def on_result(result):
                console_output.append(f"<<< {result}")

            view.page().runJavaScript(code, on_result)
            console_input.clear()

        console_input.returnPressed.connect(run_js)
        console_layout.addWidget(console_input)

        tabs.addTab(console_widget, "🔧 Консоль")

        # ===== Вкладка "Сеть" =====
        network_list = QListWidget()
        tabs.addTab(network_list, "🌐 Сеть")

        # ===== Вкладка "Исходники" =====
        sources_text = QTextEdit()
        sources_text.setFont(QFont("Courier New", 10))
        sources_text.setReadOnly(True)
        view.page().toHtml(lambda h: sources_text.setPlainText(h))
        tabs.addTab(sources_text, "📁 Исходники")

        # ===== Вкладка "Приложение" =====
        app_info = QTextEdit()
        app_info.setReadOnly(True)
        app_info.setFont(QFont("Courier New", 10))

        url = view.url().toString()
        title = view.page().title()

        app_info.setPlainText(f"""
🌌 InfinityBrowser v{VERSION}
=====================================

🌐 URL: {url}
📝 Заголовок: {title}
🔒 SSL: {'Да' if url.startswith('https') else 'Нет'}
📅 Загружена: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 Информация:
- Движок: QtWebEngine / Chromium
- Версия: {VERSION}
- Сборка: {BUILD}

🧩 Расширений: {len(self.extension_manager.get_all())}
📥 Загрузок: {len(self.download_manager.get_downloads())}
📂 Файлов: {len(self.file_manager.get_files())}
📝 Заметок: {len(self.notes_manager.get_notes())}
📰 RSS: {len(self.rss_reader.get_feeds())}
        """)

        tabs.addTab(app_info, "💾 Приложение")

        layout.addWidget(tabs)

        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec_()

    # ========================================================================
    # ⚙️ ИНСТРУМЕНТЫ
    # ========================================================================

    def show_tools_menu(self):
        """Показывает меню инструментов"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item { padding: 8px 25px; border-radius: 4px; }
            QMenu::item:selected { background: #00d4ff; color: #000; }
        """)

        menu.addAction(_("menu_downloads"), self.show_downloads_dialog)
        menu.addAction(_("menu_files"), self.show_files_dialog)
        menu.addAction(_("menu_notes"), self.toggle_sidebar)
        menu.addAction(_("menu_rss"), self.toggle_sidebar)
        menu.addSeparator()
        menu.addAction(_("menu_extensions"), self.show_extensions_menu)
        menu.addAction(_("menu_permissions"), self.show_permissions_dialog)
        menu.addAction(_("menu_themes"), self.show_themes)
        menu.addAction(_("menu_settings"), self.show_settings)
        menu.addSeparator()
        menu.addAction(_("menu_help_item"), self.show_help)
        menu.addAction(_("menu_about"), self.show_about)

        menu.exec_(self.btn_tools.mapToGlobal(
            self.btn_tools.rect().bottomLeft()
        ))

    def show_permissions_dialog(self):
        """Диалог разрешений"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("permissions_title"))
        dialog.resize(600, 400)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for domain, perms in self.permission_manager.permissions.items():
            item = QListWidgetItem(f"🌐 {domain} ({len(perms)} разрешений)")
            item.setData(Qt.UserRole, domain)
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()

        btn_revoke = QPushButton(_("permissions_revoke"))
        def revoke():
            current = list_widget.currentItem()
            if current:
                domain = current.data(Qt.UserRole)
                self.permission_manager.revoke_all(domain)
                list_widget.takeItem(list_widget.row(current))
        btn_revoke.clicked.connect(revoke)
        btn_layout.addWidget(btn_revoke)

        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)
        dialog.exec_()

    def show_settings(self):
        """Диалог настроек"""
        dialog = QDialog(self)
        dialog.setWindowTitle(_("settings_title"))
        dialog.resize(600, 500)

        layout = QVBoxLayout(dialog)

        # ===== Общие =====
        general_group = QGroupBox(_("settings_general"))
        general_layout = QVBoxLayout(general_group)

        home_layout = QHBoxLayout()
        home_layout.addWidget(QLabel(_("settings_home")))
        home_edit = QLineEdit("https://www.google.com")
        home_layout.addWidget(home_edit)
        general_layout.addLayout(home_layout)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel(_("settings_search")))
        search_combo = QComboBox()
        search_combo.addItems(["Google", "Yandex", "Bing", "DuckDuckGo"])
        search_layout.addWidget(search_combo)
        general_layout.addLayout(search_layout)

        # Язык
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(_("settings_language")))
        lang_combo = QComboBox()

        current_lang = language_manager.get_current_language()
        for code, info in language_manager.get_languages().items():
            lang_combo.addItem(info["name"], code)
            if code == current_lang:
                lang_combo.setCurrentIndex(lang_combo.count() - 1)

        lang_layout.addWidget(lang_combo)
        general_layout.addLayout(lang_layout)

        layout.addWidget(general_group)

        # ===== Безопасность =====
        security_group = QGroupBox(_("settings_security"))
        security_layout = QVBoxLayout(security_group)

        adblock_check = QCheckBox(_("settings_adblock"))
        adblock_check.setChecked(self.adblock.enabled)
        security_layout.addWidget(adblock_check)

        layout.addWidget(security_group)

        # ===== Кнопки =====
        btn_layout = QHBoxLayout()

        btn_save = QPushButton(_("settings_save"))
        btn_save.clicked.connect(dialog.accept)
        btn_layout.addWidget(btn_save)

        btn_cancel = QPushButton(_("settings_cancel"))
        btn_cancel.clicked.connect(dialog.reject)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)

        if dialog.exec_() == QDialog.Accepted:
            self.adblock.enabled = adblock_check.isChecked()

            # Смена языка
            new_lang = lang_combo.currentData()
            if new_lang != language_manager.get_current_language():
                language_manager.set_language(new_lang)
                self.setWindowTitle(_("app_title"))

            self.show_status(_("settings_saved"))

    # ========================================================================
    # ❓ ПОМОЩЬ
    # ========================================================================

    def show_help(self):
        """Показывает справку"""
        help_text = f"""
        <h1>🌌 InfinityBrowser v{VERSION}</h1>

        <h2>⌨️ Горячие клавиши:</h2>
        <table style="width:100%;">
            <tr><td><b>Ctrl+T</b></td><td>Новая вкладка</td></tr>
            <tr><td><b>Ctrl+W</b></td><td>Закрыть вкладку</td></tr>
            <tr><td><b>Ctrl+Shift+T</b></td><td>Восстановить вкладку</td></tr>
            <tr><td><b>Ctrl+Tab</b></td><td>Следующая вкладка</td></tr>
            <tr><td><b>Ctrl+Shift+Tab</b></td><td>Предыдущая вкладка</td></tr>
            <tr><td><b>Ctrl+D</b></td><td>Добавить закладку</td></tr>
            <tr><td><b>Ctrl+H</b></td><td>Боковая панель</td></tr>
            <tr><td><b>Ctrl+J</b></td><td>Загрузки</td></tr>
            <tr><td><b>Ctrl+F</b></td><td>Поиск на странице</td></tr>
            <tr><td><b>F5</b></td><td>Обновить</td></tr>
            <tr><td><b>F11</b></td><td>Полный экран</td></tr>
            <tr><td><b>F12</b></td><td>DevTools</td></tr>
            <tr><td><b>Ctrl++</b></td><td>Увеличить</td></tr>
            <tr><td><b>Ctrl+-</b></td><td>Уменьшить</td></tr>
            <tr><td><b>Ctrl+0</b></td><td>Сбросить масштаб</td></tr>
            <tr><td><b>Alt+Home</b></td><td>Домой</td></tr>
        </table>

        <h2>🆕 v{VERSION} - Открытие ссылок:</h2>
        <ul>
            <li><b>Ctrl + клик</b> по ссылке → новая вкладка</li>
            <li><b>Клик колёсиком</b> по ссылке → новая вкладка</li>
            <li><b>target="_blank"</b> → автоматически новая вкладка</li>
        </ul>
        """

        QMessageBox.information(self, _("help_title"), help_text)

    def show_about(self):
        """Показывает информацию о программе"""
        about_text = f"""
        <h1>🌌 InfinityBrowser v{VERSION}</h1>
        <p><b>Версия:</b> {VERSION}</p>
        <p><b>Сборка:</b> {BUILD}</p>
        <hr>
        <p><b>🚀 ФУНКЦИИ:</b></p>
        <ul>
            <li>🆕 Открытие ссылок в новой вкладке</li>
            <li>🌍 15+ языков интерфейса</li>
            <li>🛠️ F12 DevTools</li>
            <li>📥 Менеджер загрузок</li>
            <li>📂 Менеджер файлов</li>
            <li>🧩 Расширения (ZIP/папка/JS)</li>
            <li>🛡️ AdBlock</li>
            <li>⭐ Закладки</li>
            <li>⏳ История</li>
            <li>📝 Заметки</li>
            <li>📰 RSS-агрегатор</li>
            <li>🔒 Разрешения</li>
            <li>🎨 5 тем оформления</li>
        </ul>
        <hr>
        <p>© 2026 InfinitySoft</p>
        """

        QMessageBox.about(self, _("about_title"), about_text)

    def show_welcome(self):
        """Показывает приветствие при первом запуске"""
        flag_file = f".first_run_v{VERSION}"

        if os.path.exists(flag_file):
            return

        QMessageBox.information(
            self,
            _("welcome_title"),
            _("welcome_text")
        )

        try:
            with open(flag_file, "w") as f:
                f.write("ok")
        except:
            pass

    # ========================================================================
    # 🔄 ОБРАБОТЧИКИ СОБЫТИЙ
    # ========================================================================

    def on_url_changed(self, url):
        """Обработка изменения URL"""
        self.current_url = url.toString()

        if hasattr(self, "url_bar"):
            self.url_bar.setText(self.current_url)

        if hasattr(self, "ssl_label"):
            if self.current_url.startswith("https://"):
                self.ssl_label.setText("🔒")
                self.ssl_label.setToolTip(_("ssl_secure"))
            else:
                self.ssl_label.setText("🔓")
                self.ssl_label.setToolTip(_("ssl_insecure"))

    def on_title_changed(self, title):
        """Обработка изменения заголовка"""
        idx = self.tab_widget.currentIndex()

        if idx >= 0:
            display_title = title[:25] + "..." if len(title) > 25 else title
            self.tab_widget.setTabText(idx, display_title)

        self.setWindowTitle(_("window_title", title=title))

    def on_icon_changed(self, icon):
        """Обработка изменения иконки сайта"""
        idx = self.tab_widget.currentIndex()
        if idx >= 0:
            self.tab_widget.setTabIcon(idx, QIcon(icon))

    def on_load_progress(self, progress):
        """Обработка прогресса загрузки"""
        if hasattr(self, "progress_bar"):
            self.progress_bar.setValue(progress)

        if progress == 100:
            QTimer.singleShot(500, lambda: self.progress_bar.setValue(0))
            self.show_status(_("status_loaded"))
        elif progress < 20:
            self.show_status(_("status_connecting", progress=progress))
        elif progress < 50:
            self.show_status(_("status_loading", progress=progress))
        else:
            self.show_status(_("status_rendering", progress=progress))

    def on_fullscreen_request(self, request):
        """Обработка запроса полноэкранного режима"""
        self.toggle_fullscreen()
        request.accept()

    def on_feature_permission(self, url, feature):
        """Обработка запроса разрешения от сайта"""
        permission_map = {
            QWebEnginePage.Geolocation: "geolocation",
            QWebEnginePage.Notifications: "notifications",
            QWebEnginePage.MediaAudioCapture: "microphone",
            QWebEnginePage.MediaVideoCapture: "camera",
        }

        permission = permission_map.get(feature, "unknown")
        domain = url.host()

        allowed = self.permission_manager.request_permission(
            domain, permission, self
        )

        page = self.get_current_page()
        if page:
            if allowed:
                page.setFeaturePermission(
                    url, feature,
                    QWebEnginePage.PermissionGrantedByUser
                )
            else:
                page.setFeaturePermission(
                    url, feature,
                    QWebEnginePage.PermissionDeniedByUser
                )

    def on_download_requested(self, download):
        """Обработка запроса на скачивание"""
        url = download.url().toString()
        filename = download.suggestedFileName() or "download"

        self.download_manager.add_download(url, filename)
        download.accept()

        self.update_download_indicator()
        self.show_status(_("status_download_started", filename=filename))

    def update_download_indicator(self):
        """Обновляет индикатор загрузок"""
        if hasattr(self, "download_indicator"):
            total = len(self.download_manager.get_downloads())
            active = len(self.download_manager.get_active_downloads())
            self.download_indicator.setText(
                _("indicator_downloads", total=total, active=active)
            )

    def show_status(self, message, timeout=3000):
        """Показывает сообщение в статусбаре"""
        if hasattr(self, "status_label"):
            self.status_label.setText(message)
            if timeout > 0:
                QTimer.singleShot(
                    timeout,
                    lambda: self.status_label.setText(_("status_ready"))
                )

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.save_bookmarks()
        self.save_history()
        self.permission_manager.save_permissions()
        self.extension_manager.save_extensions()
        self.download_manager.save_downloads()

        event.accept()


# ============================================================================
# 🚀 ЗАПУСК
# ============================================================================
def main():
    """Точка входа в приложение"""
    import traceback

    try:
        # Создаем приложение
        app = QApplication(sys.argv)
        app.setApplicationName("InfinityBrowser")
        app.setOrganizationName("InfinitySoft")
        app.setApplicationVersion(VERSION)
        app.setStyle("Fusion")

        # Создаем окно браузера
        browser = InfinityBrowser()
        browser.show()

        # Запускаем основной цикл
        sys.exit(app.exec_())

    except Exception as e:
        # Если что-то пошло не так - показываем ошибку
        print("=" * 60)
        print("❌ ОШИБКА ЗАПУСКА INFINITYBROWSER:")
        print("=" * 60)
        traceback.print_exc()
        print("=" * 60)

        try:
            input("Нажми Enter чтобы закрыть...")
        except:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()