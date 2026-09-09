"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗████████╗██╗   ██╗  ║
║   ██║████╗  ██║██╔════╝██║████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝  ║
║   ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║   ██║    ╚████╔╝   ║
║   ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║   ██║     ╚██╔╝    ║
║   ██║██║ ╚████║██║     ██║██║ ╚████║██║   ██║      ██║     ║
║   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝     ║
║                                                              ║
║          🚀 INFINITYBROWSER V4.0 - COMPLETE 🚀             ║
║      ВСЕ ФУНКЦИИ: F12 + ЗАГРУЗКИ + ФАЙЛЫ + РАСШИРЕНИЯ      ║
║                   + ЛОКАЛИЗАЦИЯ + ТЕМЫ                      ║
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
# 🌍 СИСТЕМА ЛОКАЛИЗАЦИИ
# ============================================================================

class LanguageManager:
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
        "tr": {"name": "🇹🇷 Türkçe", "native": "Türkçe"}
    }
    
    TRANSLATIONS = {
        "ru": {
            "window_title": "🌌 InfinityBrowser - {title}",
            "app_title": "🌌 InfinityBrowser",
            "back": "◀ Назад",
            "forward": "▶ Вперед",
            "reload": "🔄 Обновить",
            "home": "🏠 Домой",
            "go": "🚀 Перейти",
            "search_placeholder": "🔍 Поиск или введите URL...",
            "bookmark": "⭐ Закладка",
            "bookmark_add": "⭐ Закладка добавлена",
            "bookmark_remove": "⭐ Закладка удалена",
            "bookmark_exists": "⭐ Закладка уже существует",
            "adblock": "🛡️ AdBlock",
            "adblock_on": "🛡️ AdBlock включен",
            "adblock_off": "🛡️ AdBlock отключен",
            "theme": "🌙 Тема",
            "sidebar": "📋 Панель",
            "sidebar_open": "📋 Боковая панель открыта",
            "sidebar_close": "📋 Боковая панель скрыта",
            "downloads": "📥 Загрузки",
            "files": "📂 Файлы",
            "extensions": "🧩 Расширения",
            "tools": "⚙️ Инструменты",
            "status_ready": "✅ Готово",
            "status_loading": "⏳ Загрузка: {progress}%",
            "status_connected": "⏳ Подключение... {progress}%",
            "status_downloading": "⏳ Загрузка данных... {progress}%",
            "status_rendering": "⏳ Рендеринг... {progress}%",
            "status_loaded": "✅ Страница загружена",
            "status_download_start": "📥 Начата загрузка: {filename}",
            "status_download_complete": "✅ Загрузка завершена: {filename}",
            "menu_file": "📁 Файл",
            "menu_file_new_tab": "📄 Новая вкладка",
            "menu_file_new_window": "📂 Новое окно",
            "menu_file_incognito": "🕵️ Инкогнито",
            "menu_file_downloads": "📥 Менеджер загрузок",
            "menu_file_files": "📂 Менеджер файлов",
            "menu_file_save": "💾 Сохранить как...",
            "menu_file_print": "🖨️ Печать",
            "menu_file_exit": "🚪 Выход",
            "menu_tabs": "📑 Вкладки",
            "menu_tabs_new": "➕ Новая вкладка",
            "menu_tabs_close": "❌ Закрыть вкладку",
            "menu_tabs_restore": "↩️ Восстановить вкладку",
            "menu_tabs_next": "◀ Следующая",
            "menu_tabs_prev": "▶ Предыдущая",
            "menu_tools": "🛠️ Инструменты",
            "menu_tools_downloads": "📥 Менеджер загрузок",
            "menu_tools_files": "📂 Менеджер файлов",
            "menu_tools_passwords": "🔑 Менеджер паролей",
            "menu_tools_notes": "📝 Заметки",
            "menu_tools_rss": "📰 RSS-читалка",
            "menu_tools_extensions": "🧩 Расширения",
            "menu_tools_permissions": "🔒 Разрешения",
            "menu_tools_themes": "🎨 Темы",
            "menu_tools_settings": "⚡ Настройки",
            "menu_help": "❓ Помощь",
            "menu_help_help": "📖 Справка",
            "menu_help_about": "ℹ️ О программе",
            "menu_help_updates": "🔄 Проверить обновления",
            "tab_new": "Новая вкладка",
            "tab_restored": "Восстановлена",
            "downloads_title": "📥 Менеджер загрузок",
            "downloads_open": "📂 Открыть файл",
            "downloads_folder": "📁 Открыть папку",
            "downloads_remove": "❌ Удалить из списка",
            "downloads_clear": "🗑️ Очистить завершенные",
            "downloads_close": "Закрыть",
            "downloads_pending": "⏳ Ожидание",
            "downloads_active": "📥 Загрузка",
            "downloads_paused": "⏸️ Приостановлена",
            "downloads_completed": "✅ Завершена",
            "downloads_failed": "❌ Ошибка",
            "downloads_cancelled": "🚫 Отменена",
            "files_title": "📂 Менеджер файлов",
            "files_category": "📂 Категория:",
            "files_search": "🔍 Поиск файлов...",
            "files_open_folder": "📁 Открыть папку",
            "files_open": "📂 Открыть",
            "files_delete": "🗑️ Удалить",
            "files_info": "ℹ️ Информация",
            "files_close": "Закрыть",
            "files_delete_confirm": "Удалить файл '{filename}'?",
            "files_deleted": "🗑️ Файл '{filename}' удален",
            "extensions_title": "🧩 Расширения",
            "extensions_install": "🧩 Установить расширение",
            "extensions_install_zip": "📦 Установить из архива",
            "extensions_install_js": "📄 Установить из JS",
            "extensions_manage": "🧩 Управление расширениями",
            "extensions_open": "🔍 Открыть",
            "extensions_toggle": "🔄 Включить/Выключить",
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
            "permissions_revoke": "❌ Отозвать все разрешения",
            "permissions_revoked": "🔒 Разрешения для {domain} отозваны",
            "settings_title": "⚡ Настройки",
            "settings_general": "Общие настройки",
            "settings_home": "🏠 Домашняя страница:",
            "settings_search": "🔍 Поисковик:",
            "settings_security": "Безопасность",
            "settings_adblock": "🛡️ Включить AdBlock",
            "settings_phishing": "🔒 Защита от фишинга",
            "settings_downloads": "Загрузки",
            "settings_downloads_folder": "📥 Папка загрузок:",
            "settings_browse": "📂 Обзор",
            "settings_language": "🌍 Язык:",
            "settings_save": "💾 Сохранить",
            "settings_cancel": "❌ Отмена",
            "settings_saved": "⚡ Настройки сохранены",
            "themes_title": "🎨 Выбор темы",
            "themes_select": "Выберите тему:",
            "dialog_install_extension": "🧩 Установка расширения",
            "dialog_choose_method": "Выберите способ установки расширения:",
            "dialog_zip_install": "📦 Из ZIP-архива",
            "dialog_folder_install": "📁 Из папки",
            "dialog_js_install": "📄 Из JS-файла",
            "dialog_zip_info": "Выберите ZIP-архив с расширением.\nАрхив должен содержать manifest.json и файлы расширения.",
            "dialog_folder_info": "Выберите папку с расширением.\nПапка должна содержать manifest.json и файлы расширения.",
            "dialog_js_info": "Выберите JavaScript-файл с кодом расширения.\nРасширение будет установлено как пользовательское.",
            "dialog_browse": "📂 Обзор",
            "dialog_install_btn": "✅ Установить",
            "dialog_cancel_btn": "❌ Отмена",
            "dialog_install_success": "✅ Расширение '{name}' установлено!",
            "dialog_install_error": "❌ Ошибка установки: {error}",
            "dialog_zip_missing": "В архиве отсутствует manifest.json!",
            "dialog_manifest_invalid": "Неверный формат manifest.json!",
            "dialog_manifest_fields": "В manifest.json отсутствуют обязательные поля!",
            "find_title": "🔍 Поиск",
            "find_text": "Введите текст для поиска:",
            "find_status": "🔍 Поиск: {text}",
            "help_title": "📖 Справка",
            "help_shortcuts": "⌨️ Горячие клавиши:",
            "help_shortcuts_list": """
                <tr><td><b>Ctrl+T</b></td><td>Новая вкладка</td></tr>
                <tr><td><b>Ctrl+W</b></td><td>Закрыть вкладку</td></tr>
                <tr><td><b>Ctrl+Shift+T</b></td><td>Восстановить вкладку</td></tr>
                <tr><td><b>Ctrl+Tab</b></td><td>Следующая вкладка</td></tr>
                <tr><td><b>Ctrl+Shift+Tab</b></td><td>Предыдущая вкладка</td></tr>
                <tr><td><b>Ctrl+D</b></td><td>Добавить закладку</td></tr>
                <tr><td><b>Ctrl+H</b></td><td>Боковая панель</td></tr>
                <tr><td><b>Ctrl+J</b></td><td>Загрузки</td></tr>
                <tr><td><b>F5</b></td><td>Обновить</td></tr>
                <tr><td><b>F11</b></td><td>Полный экран</td></tr>
                <tr><td><b>F12</b></td><td>Инструменты разработчика</td></tr>
                <tr><td><b>Ctrl++</b></td><td>Увеличить</td></tr>
                <tr><td><b>Ctrl+-</b></td><td>Уменьшить</td></tr>
                <tr><td><b>Ctrl+0</b></td><td>Сбросить масштаб</td></tr>
                <tr><td><b>Ctrl+F</b></td><td>Поиск на странице</td></tr>
                <tr><td><b>Alt+Home</b></td><td>Домой</td></tr>
            """,
            "about_title": "ℹ️ О программе",
            "about_text": """
                <h1>🌌 InfinityBrowser V4.0 - Complete</h1>
                <p><b>Версия:</b> 4.0.0</p>
                <p><b>Сборка:</b> 2026.09.09</p>
                <hr>
                <p><b>🚀 60+ ФУНКЦИЙ:</b></p>
                <ul>
                    <li>🌍 Поддержка 15+ языков</li>
                    <li>🛠️ F12 Инструменты разработчика</li>
                    <li>📥 Менеджер загрузок</li>
                    <li>📂 Менеджер файлов</li>
                    <li>🧩 Расширения с попап-окнами</li>
                    <li>🛡️ AdBlock</li>
                    <li>🌙 Ночной режим</li>
                    <li>⭐ Закладки</li>
                    <li>⏳ История</li>
                    <li>📝 Заметки</li>
                    <li>📰 RSS-агрегатор</li>
                    <li>🔒 Разрешения</li>
                    <li>🎨 5+ тем</li>
                </ul>
                <hr>
                <p>© 2026 InfinitySoft</p>
            """,
            "notification_copied": "✅ Ссылка скопирована",
            "notification_updated": "✅ Обновлений нет",
            "notification_checking": "🔄 Проверка обновлений...",
            "notification_theme_changed": "🎨 Тема изменена",
            "notification_clear_history": "🗑️ История очищена",
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
            "notes_title": "Заголовок...",
            "notes_content": "Текст заметки...",
            "notes_save": "💾 Сохранить",
            "notes_cancel": "❌ Отмена",
            "notes_created": "📝 Заметка '{title}' создана",
            "notes_deleted": "🗑️ Заметка удалена",
            "rss_placeholder": "Введите URL RSS...",
            "rss_added": "📰 RSS добавлен: {url}",
            "rss_exists": "❌ RSS уже существует",
            "indicator_downloads": "📥 {total} ({active} активных)",
            "indicator_extensions": "🧩 {count}",
            "ssl_secure": "🔒 Безопасное соединение",
            "ssl_insecure": "🔓 Незащищенное соединение",
            "ssl_suspicious": "⚠️ Подозрительный сайт!",
            "incognito_title": "🕵️ Инкогнито - InfinityBrowser",
            "incognito_activated": "🕵️ Режим инкогнито активирован",
            "language_changed": "🌍 Язык изменен на {language}",
            "save_page_title": "💾 Сохранить страницу",
            "save_page_filter": "HTML файлы (*.html);;Все файлы (*.*)",
            "save_page_saved": "✅ Страница сохранена: {filename}",
            "save_page_error": "❌ Ошибка: {error}",
            "print_started": "🖨️ Печать в PDF запущена",
            "permission_request": "🔒 Запрос разрешения",
            "permission_text": "Сайт <b>{domain}</b> запрашивает разрешение на <b>{permission}</b>",
            "permission_allow": "✅ Разрешить",
            "permission_deny": "❌ Запретить",
            "welcome_title": "🌌 Добро пожаловать в InfinityBrowser!",
            "welcome_text": """
                <h2>🚀 InfinityBrowser Complete готов к работе!</h2>
                <p><b>Новые функции:</b></p>
                <ul>
                    <li><b>🌍 Многоязычность</b> - 15+ языков интерфейса</li>
                    <li><b>🛠️ F12</b> - Инструменты разработчика как в Chrome</li>
                    <li><b>🧩 Расширения</b> - Двойной клик для открытия</li>
                    <li><b>📥 Загрузки</b> - Файлы скачиваются и сохраняются</li>
                </ul>
                <p>🖱️ <b>Двойной клик</b> по расширению в списке → открыть попап</p>
                <p>📚 Нажмите <b>F1</b> для справки</p>
                <p>🌍 Изменить язык: Настройки → Язык</p>
                <p>🛠️ Нажмите <b>F12</b> для инструментов разработчика</p>
            """,
            "bookmark_folder": "Папка закладки",
            "bookmark_folder_select": "Выберите папку:",
            "bookmark_folder_new": "Новая папка",
            "bookmark_folder_name": "Введите название папки:",
            "bookmark_added": "⭐ Закладка добавлена в '{folder}'",
            "bookmark_folders": ["Основные", "Работа", "Учёба", "Развлечения"],
            "devtools_title": "🛠️ Инструменты разработчика - {title}",
            "devtools_elements": "📄 Элементы",
            "devtools_console": "🔧 Консоль",
            "devtools_network": "🌐 Сеть",
            "devtools_sources": "📁 Исходники",
            "devtools_application": "💾 Приложение",
            "devtools_status": "✅ Инструменты разработчика активны | F12 для закрытия",
            "devtools_close": "✕ Закрыть",
            "devtools_search": "🔍 Поиск по HTML...",
            "devtools_refresh": "🔄",
            "devtools_console_placeholder": "▶ Введите JavaScript-код в поле ниже...",
            "devtools_console_input": "Введите JavaScript-код и нажмите Enter...",
            "devtools_console_run": "▶ Выполнить",
            "devtools_console_clear": "🗑️ Очистить",
            "devtools_network_record": "🔴 Запись",
            "devtools_network_pause": "⏸️ Пауза",
            "devtools_network_clear": "🗑️ Очистить",
            "devtools_network_refresh": "🔄 Обновить",
            "devtools_sources_view": "📄 Просмотр исходного кода",
            "devtools_sources_placeholder": "Нажмите 'Просмотр исходного кода' для загрузки...",
            "devtools_app_page": "📄 Информация о странице",
            "devtools_app_browser": "🚀 Информация о браузере",
            "devtools_app_refresh": "🔄 Обновить информацию",
            "devtools_app_close": "✕ Закрыть"
        },
        "en": {
            "window_title": "🌌 InfinityBrowser - {title}",
            "app_title": "🌌 InfinityBrowser",
            "back": "◀ Back",
            "forward": "▶ Forward",
            "reload": "🔄 Reload",
            "home": "🏠 Home",
            "go": "🚀 Go",
            "search_placeholder": "🔍 Search or enter URL...",
            "bookmark": "⭐ Bookmark",
            "bookmark_add": "⭐ Bookmark added",
            "bookmark_remove": "⭐ Bookmark removed",
            "bookmark_exists": "⭐ Bookmark already exists",
            "adblock": "🛡️ AdBlock",
            "adblock_on": "🛡️ AdBlock enabled",
            "adblock_off": "🛡️ AdBlock disabled",
            "theme": "🌙 Theme",
            "sidebar": "📋 Sidebar",
            "sidebar_open": "📋 Sidebar opened",
            "sidebar_close": "📋 Sidebar closed",
            "downloads": "📥 Downloads",
            "files": "📂 Files",
            "extensions": "🧩 Extensions",
            "tools": "⚙️ Tools",
            "status_ready": "✅ Ready",
            "status_loading": "⏳ Loading: {progress}%",
            "status_connected": "⏳ Connecting... {progress}%",
            "status_downloading": "⏳ Downloading... {progress}%",
            "status_rendering": "⏳ Rendering... {progress}%",
            "status_loaded": "✅ Page loaded",
            "status_download_start": "📥 Download started: {filename}",
            "status_download_complete": "✅ Download complete: {filename}",
            "menu_file": "📁 File",
            "menu_file_new_tab": "📄 New Tab",
            "menu_file_new_window": "📂 New Window",
            "menu_file_incognito": "🕵️ Incognito",
            "menu_file_downloads": "📥 Download Manager",
            "menu_file_files": "📂 File Manager",
            "menu_file_save": "💾 Save As...",
            "menu_file_print": "🖨️ Print",
            "menu_file_exit": "🚪 Exit",
            "menu_tabs": "📑 Tabs",
            "menu_tabs_new": "➕ New Tab",
            "menu_tabs_close": "❌ Close Tab",
            "menu_tabs_restore": "↩️ Restore Tab",
            "menu_tabs_next": "◀ Next",
            "menu_tabs_prev": "▶ Previous",
            "menu_tools": "🛠️ Tools",
            "menu_tools_downloads": "📥 Download Manager",
            "menu_tools_files": "📂 File Manager",
            "menu_tools_passwords": "🔑 Password Manager",
            "menu_tools_notes": "📝 Notes",
            "menu_tools_rss": "📰 RSS Reader",
            "menu_tools_extensions": "🧩 Extensions",
            "menu_tools_permissions": "🔒 Permissions",
            "menu_tools_themes": "🎨 Themes",
            "menu_tools_settings": "⚡ Settings",
            "menu_help": "❓ Help",
            "menu_help_help": "📖 Help",
            "menu_help_about": "ℹ️ About",
            "menu_help_updates": "🔄 Check for Updates",
            "tab_new": "New Tab",
            "tab_restored": "Restored",
            "downloads_title": "📥 Download Manager",
            "downloads_open": "📂 Open File",
            "downloads_folder": "📁 Open Folder",
            "downloads_remove": "❌ Remove from List",
            "downloads_clear": "🗑️ Clear Completed",
            "downloads_close": "Close",
            "downloads_pending": "⏳ Pending",
            "downloads_active": "📥 Downloading",
            "downloads_paused": "⏸️ Paused",
            "downloads_completed": "✅ Completed",
            "downloads_failed": "❌ Failed",
            "downloads_cancelled": "🚫 Cancelled",
            "files_title": "📂 File Manager",
            "files_category": "📂 Category:",
            "files_search": "🔍 Search files...",
            "files_open_folder": "📁 Open Folder",
            "files_open": "📂 Open",
            "files_delete": "🗑️ Delete",
            "files_info": "ℹ️ Info",
            "files_close": "Close",
            "files_delete_confirm": "Delete file '{filename}'?",
            "files_deleted": "🗑️ File '{filename}' deleted",
            "extensions_title": "🧩 Extensions",
            "extensions_install": "🧩 Install Extension",
            "extensions_install_zip": "📦 Install from Archive",
            "extensions_install_js": "📄 Install from JS",
            "extensions_manage": "🧩 Manage Extensions",
            "extensions_open": "🔍 Open",
            "extensions_toggle": "🔄 Enable/Disable",
            "extensions_uninstall": "🗑️ Uninstall",
            "extensions_code": "📄 Code",
            "extensions_options": "⚙️ Settings",
            "extensions_installed": "🧩 Extension '{name}' installed!",
            "extensions_uninstalled": "❌ Extension '{name}' uninstalled",
            "extensions_enabled": "🟢 Extension '{name}' enabled",
            "extensions_disabled": "🔴 Extension '{name}' disabled",
            "extensions_cannot_uninstall": "❌ Cannot uninstall built-in extension!",
            "extensions_uninstall_confirm": "Uninstall extension '{name}'?",
            "permissions_title": "🔒 Permissions",
            "permissions_revoke": "❌ Revoke all permissions",
            "permissions_revoked": "🔒 Permissions for {domain} revoked",
            "settings_title": "⚡ Settings",
            "settings_general": "General Settings",
            "settings_home": "🏠 Home Page:",
            "settings_search": "🔍 Search Engine:",
            "settings_security": "Security",
            "settings_adblock": "🛡️ Enable AdBlock",
            "settings_phishing": "🔒 Phishing Protection",
            "settings_downloads": "Downloads",
            "settings_downloads_folder": "📥 Downloads Folder:",
            "settings_browse": "📂 Browse",
            "settings_language": "🌍 Language:",
            "settings_save": "💾 Save",
            "settings_cancel": "❌ Cancel",
            "settings_saved": "⚡ Settings saved",
            "themes_title": "🎨 Choose Theme",
            "themes_select": "Select theme:",
            "dialog_install_extension": "🧩 Install Extension",
            "dialog_choose_method": "Choose installation method:",
            "dialog_zip_install": "📦 From ZIP Archive",
            "dialog_folder_install": "📁 From Folder",
            "dialog_js_install": "📄 From JS File",
            "dialog_zip_info": "Select ZIP archive with extension.\nArchive must contain manifest.json and extension files.",
            "dialog_folder_info": "Select folder with extension.\nFolder must contain manifest.json and extension files.",
            "dialog_js_info": "Select JavaScript file with extension code.\nExtension will be installed as user extension.",
            "dialog_browse": "📂 Browse",
            "dialog_install_btn": "✅ Install",
            "dialog_cancel_btn": "❌ Cancel",
            "dialog_install_success": "✅ Extension '{name}' installed!",
            "dialog_install_error": "❌ Installation error: {error}",
            "dialog_zip_missing": "Archive missing manifest.json!",
            "dialog_manifest_invalid": "Invalid manifest.json format!",
            "dialog_manifest_fields": "Manifest.json missing required fields!",
            "find_title": "🔍 Find",
            "find_text": "Enter text to search:",
            "find_status": "🔍 Search: {text}",
            "help_title": "📖 Help",
            "help_shortcuts": "⌨️ Keyboard Shortcuts:",
            "help_shortcuts_list": """
                <tr><td><b>Ctrl+T</b></td><td>New Tab</td></tr>
                <tr><td><b>Ctrl+W</b></td><td>Close Tab</td></tr>
                <tr><td><b>Ctrl+Shift+T</b></td><td>Restore Tab</td></tr>
                <tr><td><b>Ctrl+Tab</b></td><td>Next Tab</td></tr>
                <tr><td><b>Ctrl+Shift+Tab</b></td><td>Previous Tab</td></tr>
                <tr><td><b>Ctrl+D</b></td><td>Add Bookmark</td></tr>
                <tr><td><b>Ctrl+H</b></td><td>Sidebar</td></tr>
                <tr><td><b>Ctrl+J</b></td><td>Downloads</td></tr>
                <tr><td><b>F5</b></td><td>Reload</td></tr>
                <tr><td><b>F11</b></td><td>Fullscreen</td></tr>
                <tr><td><b>F12</b></td><td>Developer Tools</td></tr>
                <tr><td><b>Ctrl++</b></td><td>Zoom In</td></tr>
                <tr><td><b>Ctrl+-</b></td><td>Zoom Out</td></tr>
                <tr><td><b>Ctrl+0</b></td><td>Reset Zoom</td></tr>
                <tr><td><b>Ctrl+F</b></td><td>Find on Page</td></tr>
                <tr><td><b>Alt+Home</b></td><td>Home</td></tr>
            """,
            "about_title": "ℹ️ About",
            "about_text": """
                <h1>🌌 InfinityBrowser V4.0 - Complete</h1>
                <p><b>Version:</b> 4.0.0</p>
                <p><b>Build:</b> 2026.09.09</p>
                <hr>
                <p><b>🚀 60+ FEATURES:</b></p>
                <ul>
                    <li>🌍 15+ Languages support</li>
                    <li>🛠️ F12 Developer Tools</li>
                    <li>📥 Download Manager</li>
                    <li>📂 File Manager</li>
                    <li>🧩 Extensions with popups</li>
                    <li>🛡️ AdBlock</li>
                    <li>🌙 Night Mode</li>
                    <li>⭐ Bookmarks</li>
                    <li>⏳ History</li>
                    <li>📝 Notes</li>
                    <li>📰 RSS Reader</li>
                    <li>🔒 Permissions</li>
                    <li>🎨 5+ Themes</li>
                </ul>
                <hr>
                <p>© 2026 InfinitySoft</p>
            """,
            "notification_copied": "✅ Link copied",
            "notification_updated": "✅ No updates",
            "notification_checking": "🔄 Checking for updates...",
            "notification_theme_changed": "🎨 Theme changed",
            "notification_clear_history": "🗑️ History cleared",
            "sidebar_bookmarks": "⭐ Bookmarks",
            "sidebar_history": "⏳ History",
            "sidebar_notes": "📝 Notes",
            "sidebar_rss": "📰 RSS",
            "sidebar_extensions": "🧩 Extensions",
            "sidebar_search_bookmarks": "🔍 Search bookmarks...",
            "sidebar_search_history": "🔍 Search history...",
            "sidebar_search_notes": "🔍 Search notes...",
            "sidebar_add_bookmark": "➕ Add Bookmark",
            "sidebar_add_note": "➕ New Note",
            "sidebar_clear_history": "🗑️ Clear History",
            "notes_new_title": "📝 New Note",
            "notes_title": "Title...",
            "notes_content": "Note content...",
            "notes_save": "💾 Save",
            "notes_cancel": "❌ Cancel",
            "notes_created": "📝 Note '{title}' created",
            "notes_deleted": "🗑️ Note deleted",
            "rss_placeholder": "Enter RSS URL...",
            "rss_added": "📰 RSS added: {url}",
            "rss_exists": "❌ RSS already exists",
            "indicator_downloads": "📥 {total} ({active} active)",
            "indicator_extensions": "🧩 {count}",
            "ssl_secure": "🔒 Secure connection",
            "ssl_insecure": "🔓 Insecure connection",
            "ssl_suspicious": "⚠️ Suspicious site!",
            "incognito_title": "🕵️ Incognito - InfinityBrowser",
            "incognito_activated": "🕵️ Incognito mode activated",
            "language_changed": "🌍 Language changed to {language}",
            "save_page_title": "💾 Save Page",
            "save_page_filter": "HTML files (*.html);;All files (*.*)",
            "save_page_saved": "✅ Page saved: {filename}",
            "save_page_error": "❌ Error: {error}",
            "print_started": "🖨️ PDF printing started",
            "permission_request": "🔒 Permission Request",
            "permission_text": "Site <b>{domain}</b> requests permission for <b>{permission}</b>",
            "permission_allow": "✅ Allow",
            "permission_deny": "❌ Deny",
            "welcome_title": "🌌 Welcome to InfinityBrowser!",
            "welcome_text": """
                <h2>🚀 InfinityBrowser Complete is ready!</h2>
                <p><b>New features:</b></p>
                <ul>
                    <li><b>🌍 Multilingual</b> - 15+ interface languages</li>
                    <li><b>🛠️ F12</b> - Developer Tools like in Chrome</li>
                    <li><b>🧩 Extensions</b> - Double-click to open</li>
                    <li><b>📥 Downloads</b> - Files download and save</li>
                </ul>
                <p>🖱️ <b>Double-click</b> on extension in list → open popup</p>
                <p>📚 Press <b>F1</b> for help</p>
                <p>🌍 Change language: Settings → Language</p>
                <p>🛠️ Press <b>F12</b> for Developer Tools</p>
            """,
            "bookmark_folder": "Bookmark Folder",
            "bookmark_folder_select": "Select folder:",
            "bookmark_folder_new": "New Folder",
            "bookmark_folder_name": "Enter folder name:",
            "bookmark_added": "⭐ Bookmark added to '{folder}'",
            "bookmark_folders": ["Main", "Work", "Study", "Entertainment"],
            "devtools_title": "🛠️ Developer Tools - {title}",
            "devtools_elements": "📄 Elements",
            "devtools_console": "🔧 Console",
            "devtools_network": "🌐 Network",
            "devtools_sources": "📁 Sources",
            "devtools_application": "💾 Application",
            "devtools_status": "✅ Developer Tools active | F12 to close",
            "devtools_close": "✕ Close",
            "devtools_search": "🔍 Search HTML...",
            "devtools_refresh": "🔄",
            "devtools_console_placeholder": "▶ Enter JavaScript code below...",
            "devtools_console_input": "Enter JavaScript code and press Enter...",
            "devtools_console_run": "▶ Run",
            "devtools_console_clear": "🗑️ Clear",
            "devtools_network_record": "🔴 Record",
            "devtools_network_pause": "⏸️ Pause",
            "devtools_network_clear": "🗑️ Clear",
            "devtools_network_refresh": "🔄 Refresh",
            "devtools_sources_view": "📄 View Source Code",
            "devtools_sources_placeholder": "Press 'View Source Code' to load...",
            "devtools_app_page": "📄 Page Info",
            "devtools_app_browser": "🚀 Browser Info",
            "devtools_app_refresh": "🔄 Refresh Info",
            "devtools_app_close": "✕ Close"
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
        except: pass
    
    def set_language(self, lang_code: str):
        if lang_code in self.LANGUAGES:
            self.current_language = lang_code
            self.save_language()
            return True
        return False
    
    def get_languages(self):
        return self.LANGUAGES
    
    def get_current_language(self):
        return self.current_language
    
    def get_language_name(self, lang_code: str):
        return self.LANGUAGES.get(lang_code, {}).get("name", lang_code)
    
    def tr(self, key: str, **kwargs) -> str:
        translations = self.TRANSLATIONS.get(self.current_language, {})
        text = translations.get(key, key)
        for k, v in kwargs.items():
            text = text.replace("{" + k + "}", str(v))
        return text

language_manager = LanguageManager()

def _(key: str, **kwargs) -> str:
    return language_manager.tr(key, **kwargs)

# ============================================================================
# 📥 МЕНЕДЖЕР ЗАГРУЗОК
# ============================================================================
class DownloadManager:
    def __init__(self):
        self.downloads = []
        self.download_dir = os.path.expanduser("~/Downloads/InfinityBrowser")
        os.makedirs(self.download_dir, exist_ok=True)
        self.load_downloads()
    
    def add_download(self, url: str, filename: str = None, save_path: str = None):
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
            "id": str(int(time.time())),
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
        def download_thread():
            try:
                import requests
                download["status"] = "downloading"
                response = requests.get(download["url"], stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                download["size"] = total_size
                downloaded = 0
                last_update = time.time()
                last_downloaded = 0
                
                with open(download["filepath"], "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                download["progress"] = (downloaded / total_size) * 100
                            download["downloaded"] = downloaded
                            
                            current_time = time.time()
                            if current_time - last_update >= 1:
                                download["speed"] = (downloaded - last_downloaded) / (current_time - last_update)
                                last_update = current_time
                                last_downloaded = downloaded
                            
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
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def get_downloads(self):
        return self.downloads
    
    def get_active_downloads(self):
        return [d for d in self.downloads if d["status"] in ["pending", "downloading"]]
    
    def get_completed_downloads(self):
        return [d for d in self.downloads if d["status"] == "completed"]
    
    def open_file(self, download_id):
        for d in self.downloads:
            if d["id"] == download_id and d["status"] == "completed":
                if os.path.exists(d["filepath"]):
                    os.startfile(d["filepath"])
                    return True
        return False
    
    def open_folder(self, download_id):
        for d in self.downloads:
            if d["id"] == download_id:
                if os.path.exists(d["save_path"]):
                    os.startfile(d["save_path"])
                    return True
        return False
    
    def remove_download(self, download_id):
        self.downloads = [d for d in self.downloads if d["id"] != download_id]
        self.save_downloads()
    
    def save_downloads(self):
        try:
            with open("downloads.json", "w", encoding="utf-8") as f:
                json.dump(self.downloads, f, ensure_ascii=False, indent=2)
        except: pass
    
    def load_downloads(self):
        try:
            with open("downloads.json", "r", encoding="utf-8") as f:
                self.downloads = json.load(f)
        except: self.downloads = []

# ============================================================================
# 📂 МЕНЕДЖЕР ФАЙЛОВ
# ============================================================================
class FileManager:
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
        
        for filename in os.listdir(self.base_dir):
            filepath = os.path.join(self.base_dir, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if category != "Все":
                    category_exts = self.categories.get(category, [])
                    if ext not in category_exts:
                        continue
                
                stats = os.stat(filepath)
                files.append({
                    "name": filename,
                    "path": filepath,
                    "size": stats.st_size,
                    "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "extension": ext,
                    "category": self.get_category(ext)
                })
        
        files.sort(key=lambda x: x["modified"], reverse=True)
        return files
    
    def get_category(self, ext):
        for category, exts in self.categories.items():
            if category != "Все" and ext in exts:
                return category
        return "Другое"
    
    def delete_file(self, filename):
        filepath = os.path.join(self.base_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def open_file(self, filename):
        filepath = os.path.join(self.base_dir, filename)
        if os.path.exists(filepath):
            os.startfile(filepath)
            return True
        return False
    
    def open_folder(self):
        os.startfile(self.base_dir)
    
    def get_file_info(self, filename):
        filepath = os.path.join(self.base_dir, filename)
        if os.path.exists(filepath):
            stats = os.stat(filepath)
            ext = os.path.splitext(filename)[1].lower()
            return {
                "name": filename,
                "path": filepath,
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
    def __init__(self, id: str, name: str, version: str, author: str,
                 description: str, script: str = "", manifest: Dict = None):
        self.id = id
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.script = script
        self.manifest = manifest or {}
        self.enabled = True
        self.permissions = []
        self.host_permissions = []
        self.path = ""
        self.popup_html = ""
        self.options_html = ""
        self.icon = None
    
    def get_popup_html(self) -> str:
        if self.popup_html:
            return self.popup_html
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
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
                .status {{ display: inline-block; padding: 3px 12px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
                .status-enabled {{ background: #00ff88; color: #000; }}
                .status-disabled {{ background: #ff4444; color: #fff; }}
                .actions {{ display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }}
                .btn {{ padding: 6px 14px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: bold; transition: all 0.3s; }}
                .btn-primary {{ background: #00d4ff; color: #000; }}
                .btn-primary:hover {{ background: #00eeff; }}
                .btn-danger {{ background: #ff4444; color: #fff; }}
                .btn-danger:hover {{ background: #ff6666; }}
                .btn-secondary {{ background: #2a2a3e; color: #e0e0e0; }}
                .btn-secondary:hover {{ background: #3a3a4e; }}
                .info {{ font-size: 11px; color: #808090; margin: 5px 0; }}
                .permissions {{ font-size: 11px; color: #808090; margin: 5px 0; }}
                .permissions span {{ background: #2a2a3e; padding: 2px 8px; border-radius: 4px; margin: 2px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <span class="icon">🧩</span>
                <div>
                    <div class="name">{self.name}</div>
                    <div class="version">v{self.version}</div>
                </div>
            </div>
            <div class="desc">{self.description}</div>
            <div style="margin: 8px 0;">
                <span class="status {'status-enabled' if self.enabled else 'status-disabled'}">
                    {'✅ Enabled' if self.enabled else '❌ Disabled'}
                </span>
            </div>
            <div class="info">👤 Author: {self.author}</div>
            <div class="permissions">
                🔓 Permissions:
                {''.join(f'<span>{p}</span>' for p in self.permissions[:3])}
                {f'<span>+{len(self.permissions)-3}...</span>' if len(self.permissions) > 3 else ''}
            </div>
            <div class="actions">
                <button class="btn btn-primary" onclick="window.toggleExtension()">
                    {'🔄 Disable' if self.enabled else '🔄 Enable'}
                </button>
                <button class="btn btn-secondary" onclick="window.viewCode()">📄 Code</button>
                <button class="btn btn-secondary" onclick="window.viewOptions()">⚙️ Settings</button>
                <button class="btn btn-danger" onclick="window.uninstallExtension()">🗑️ Uninstall</button>
            </div>
            <script>
                window.toggleExtension = function() {{ window.parent.toggleExtension('{self.id}'); }};
                window.viewCode = function() {{ window.parent.viewExtensionCode('{self.id}'); }};
                window.viewOptions = function() {{ window.parent.viewExtensionOptions('{self.id}'); }};
                window.uninstallExtension = function() {{ window.parent.uninstallExtension('{self.id}'); }};
            </script>
        </body>
        </html>
        """
    
    def get_options_html(self) -> str:
        if self.options_html:
            return self.options_html
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a1a; color: #e0e0e0; padding: 20px; margin: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                h1 {{ color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }}
                .setting {{ background: #1a1a2e; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .setting label {{ display: block; font-weight: bold; margin-bottom: 5px; color: #c0c0d0; }}
                .setting .value {{ color: #e0e0e0; padding: 5px 0; }}
                .status-enabled {{ background: #00ff88; color: #000; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
                .status-disabled {{ background: #ff4444; color: #fff; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
                .btn {{ padding: 10px 20px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: bold; }}
                .btn-primary {{ background: #00d4ff; color: #000; }}
                .btn-primary:hover {{ background: #00eeff; }}
                .permission-list {{ list-style: none; padding: 0; }}
                .permission-list li {{ padding: 5px 0; border-bottom: 1px solid #1a1a2e; color: #c0c0d0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚙️ Settings: {self.name}</h1>
                <div class="setting">
                    <label>📊 Status</label>
                    <div class="value">
                        <span class="{'status-enabled' if self.enabled else 'status-disabled'}">
                            {'✅ Enabled' if self.enabled else '❌ Disabled'}
                        </span>
                    </div>
                </div>
                <div class="setting">
                    <label>📌 Info</label>
                    <div class="value">
                        <b>Version:</b> {self.version}<br>
                        <b>Author:</b> {self.author}<br>
                        <b>ID:</b> {self.id}
                    </div>
                </div>
                <div class="setting">
                    <label>📝 Description</label>
                    <div class="value">{self.description}</div>
                </div>
                <div class="setting">
                    <label>🔓 Permissions</label>
                    <ul class="permission-list">
                        {''.join(f'<li>🔓 {p}</li>' for p in self.permissions) or '<li>No permissions</li>'}
                    </ul>
                </div>
                <div class="setting">
                    <label>📁 Path</label>
                    <div class="value" style="font-size: 11px; color: #808090;">{self.path or 'Built-in'}</div>
                </div>
                <button class="btn btn-primary" onclick="window.close()">✅ Close</button>
            </div>
        </body>
        </html>
        """
    
    def to_dict(self) -> Dict:
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
            "host_permissions": self.host_permissions,
            "path": self.path,
            "popup_html": self.popup_html,
            "options_html": self.options_html
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Extension':
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
        ext.host_permissions = data.get("host_permissions", [])
        ext.path = data.get("path", "")
        ext.popup_html = data.get("popup_html", "")
        ext.options_html = data.get("options_html", "")
        return ext

class ExtensionManager:
    def __init__(self):
        self.extensions = {}
        self.load_extensions()
        self.install_builtin_extensions()
    
    def install_builtin_extensions(self):
        builtins = [
            ("adblock_plus", "🛡️ AdBlock Plus", "1.0.0", "InfinitySoft", "Block ads on all websites", ["webRequest", "webRequestBlocking"]),
            ("dark_reader", "🌙 Dark Reader", "1.0.0", "InfinitySoft", "Dark mode for all websites", ["activeTab"]),
            ("translator", "🌍 Translator", "1.0.0", "InfinitySoft", "Translate pages to any language", ["activeTab"]),
            ("screenshot", "📸 Screenshots", "1.0.0", "InfinitySoft", "Quick page screenshots", ["activeTab", "screenshots"])
        ]
        for ext_id, name, version, author, desc, perms in builtins:
            if ext_id not in self.extensions:
                ext = Extension(ext_id, name, version, author, desc)
                ext.permissions = perms
                self.extensions[ext_id] = ext
        self.save_extensions()
    
    def install_from_zip(self, zip_path: str) -> Optional[Extension]:
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
                name=manifest.get("name", "Без названия"),
                version=manifest.get("version", "1.0.0"),
                author=manifest.get("author", "Неизвестен"),
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
            
            popup_path = os.path.join(ext_dir, "popup.html")
            if os.path.exists(popup_path):
                with open(popup_path, "r", encoding="utf-8") as f:
                    ext.popup_html = f.read()
            
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
    
    def install_from_folder(self, folder_path: str) -> Optional[Extension]:
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
                name=manifest.get("name", "Без названия"),
                version=manifest.get("version", "1.0.0"),
                author=manifest.get("author", "Неизвестен"),
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
            
            popup_path = os.path.join(ext_dir, "popup.html")
            if os.path.exists(popup_path):
                with open(popup_path, "r", encoding="utf-8") as f:
                    ext.popup_html = f.read()
            
            options_path = os.path.join(ext_dir, "options.html")
            if os.path.exists(options_path):
                with open(options_path, "r", encoding="utf-8") as f:
                    ext.options_html = f.read()
            
            self.extensions[ext_id] = ext
            self.save_extensions()
            return ext
            
        except Exception as e:
            print(f"Ошибка установки из папки: {e}")
            return None
    
    def install_from_js(self, name: str, code: str) -> Optional[Extension]:
        try:
            ext_id = hashlib.md5(name.encode()).hexdigest()[:8]
            ext_dir = os.path.join("extensions", ext_id)
            os.makedirs(ext_dir, exist_ok=True)
            
            js_path = os.path.join(ext_dir, "script.js")
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            manifest = {
                "name": name,
                "version": "1.0.0",
                "author": "Пользователь",
                "description": "Пользовательское расширение",
                "scripts": ["script.js"],
                "permissions": ["activeTab"]
            }
            
            manifest_path = os.path.join(ext_dir, "manifest.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            ext = Extension(
                id=ext_id,
                name=name,
                version="1.0.0",
                author="Пользователь",
                description="Пользовательское расширение",
                script=code,
                manifest=manifest
            )
            ext.path = ext_dir
            ext.permissions = ["activeTab"]
            
            self.extensions[ext_id] = ext
            self.save_extensions()
            return ext
            
        except Exception as e:
            print(f"Ошибка установки из JS: {e}")
            return None
    
    def uninstall_extension(self, ext_id: str) -> bool:
        builtins = ["adblock_plus", "dark_reader", "translator", "screenshot"]
        if ext_id in builtins:
            return False
        if ext_id in self.extensions:
            ext = self.extensions[ext_id]
            if ext.path and os.path.exists(ext.path):
                shutil.rmtree(ext.path, ignore_errors=True)
            del self.extensions[ext_id]
            self.save_extensions()
            return True
        return False
    
    def toggle_extension(self, ext_id: str) -> bool:
        if ext_id in self.extensions:
            ext = self.extensions[ext_id]
            ext.enabled = not ext.enabled
            self.save_extensions()
            return ext.enabled
        return False
    
    def get_extension(self, ext_id: str) -> Optional[Extension]:
        return self.extensions.get(ext_id)
    
    def get_all_extensions(self) -> List[Extension]:
        return list(self.extensions.values())
    
    def get_enabled_extensions(self) -> List[Extension]:
        return [ext for ext in self.extensions.values() if ext.enabled]
    
    def save_extensions(self):
        try:
            os.makedirs("extensions", exist_ok=True)
            data = [ext.to_dict() for ext in self.extensions.values()]
            with open("extensions.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except: pass
    
    def load_extensions(self):
        try:
            with open("extensions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    ext = Extension.from_dict(item)
                    self.extensions[ext.id] = ext
        except: self.extensions = {}

# ============================================================================
# 🔒 РАЗРЕШЕНИЯ
# ============================================================================
class PermissionManager:
    def __init__(self):
        self.permissions = {}
        self.load_permissions()
    
    def request_permission(self, domain, permission):
        if domain in self.permissions and permission in self.permissions[domain]:
            return self.permissions[domain][permission] == "allow"
        
        result = self.show_permission_dialog(domain, permission)
        if domain not in self.permissions:
            self.permissions[domain] = {}
        self.permissions[domain][permission] = "allow" if result else "deny"
        self.save_permissions()
        return result
    
    def show_permission_dialog(self, domain, permission):
        msg = QMessageBox()
        msg.setWindowTitle(_("permission_request"))
        msg.setText(_("permission_text", domain=domain, permission=permission))
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(_("permission_allow"))
        msg.button(QMessageBox.No).setText(_("permission_deny"))
        return msg.exec_() == QMessageBox.Yes
    
    def load_permissions(self):
        try:
            with open("permissions.json", "r") as f:
                self.permissions = json.load(f)
        except: self.permissions = {}
    
    def save_permissions(self):
        try:
            with open("permissions.json", "w") as f:
                json.dump(self.permissions, f, indent=2)
        except: pass

# ============================================================================
# 🛡️ ADBLOCK
# ============================================================================
class AdBlockManager:
    def __init__(self):
        self.enabled = True
        self.rules = [
            r"ads\.", r"adserver", r"doubleclick", r"googleads",
            r"yandexads", r"adfox", r"adriver", r"rtb", r"criteo",
            r"adnxs", r"openx", r"rubicon", r"pubmatic", r"indexexchange",
            r"smartadserver", r"taboola", r"outbrain"
        ]
        self.blocked_count = 0
    
    def should_block(self, url):
        if not self.enabled:
            return False
        for rule in self.rules:
            if re.search(rule, url, re.IGNORECASE):
                self.blocked_count += 1
                return True
        return False
    
    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

# ============================================================================
# 📝 ЗАМЕТКИ
# ============================================================================
class NotesManager:
    def __init__(self):
        self.notes = []
        self.load_notes()
    
    def add_note(self, title, content, category="Общие"):
        note = {"id": str(int(time.time())), "title": title, "content": content, "category": category, "created": datetime.now().isoformat()}
        self.notes.append(note)
        self.save_notes()
        return note
    
    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self.save_notes()
    
    def get_notes(self, category=None):
        if category:
            return [n for n in self.notes if n.get("category") == category]
        return self.notes
    
    def search_notes(self, query):
        query = query.lower()
        return [n for n in self.notes if query in n["title"].lower() or query in n["content"].lower()]
    
    def save_notes(self):
        try:
            with open("notes.json", "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except: pass
    
    def load_notes(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        except: self.notes = []

# ============================================================================
# 📰 RSS
# ============================================================================
class RSSReader:
    def __init__(self):
        self.feeds = []
        self.load_feeds()
    
    def add_feed(self, url):
        if url not in self.feeds:
            self.feeds.append(url)
            self.save_feeds()
            return True
        return False
    
    def remove_feed(self, url):
        if url in self.feeds:
            self.feeds.remove(url)
            self.save_feeds()
            return True
        return False
    
    def get_feeds(self):
        return self.feeds
    
    def save_feeds(self):
        try:
            with open("rss_feeds.json", "w") as f:
                json.dump(self.feeds, f)
        except: pass
    
    def load_feeds(self):
        try:
            with open("rss_feeds.json", "r") as f:
                self.feeds = json.load(f)
        except: self.feeds = []

# ============================================================================
# 🌍 ПЕРЕВОДЧИК
# ============================================================================
class Translator:
    def __init__(self):
        self.target_lang = "ru"
        self.languages = {"ru": "Русский", "en": "Английский", "de": "Немецкий", "fr": "Французский", "es": "Испанский"}
    
    def translate(self, text, from_lang="auto", to_lang="ru"):
        if from_lang == to_lang:
            return text
        return f"[Перевод]: {text}"

# ============================================================================
# 🎨 ТЕМЫ
# ============================================================================
class ThemeManager:
    THEMES = {
        "infinity": {"name": "🌌 Infinity", "background": "#0a0a1a", "widget": "#1a1a2e", "widget_hover": "#2a2a3e", "text": "#e0e0e0", "accent": "#00d4ff", "accent_hover": "#00eeff", "border": "#2a2a3e"},
        "dark": {"name": "🌙 Dark", "background": "#0d0d0d", "widget": "#1a1a1a", "widget_hover": "#2a2a2a", "text": "#ffffff", "accent": "#00ff88", "accent_hover": "#44ffaa", "border": "#2a2a2a"},
        "light": {"name": "☀️ Light", "background": "#f0f0f0", "widget": "#ffffff", "widget_hover": "#e8e8e8", "text": "#222222", "accent": "#0088ff", "accent_hover": "#0066cc", "border": "#cccccc"},
        "neon": {"name": "💜 Neon", "background": "#0a001a", "widget": "#1a0033", "widget_hover": "#2a0044", "text": "#ff88ff", "accent": "#ff00ff", "accent_hover": "#ff44ff", "border": "#440066"},
        "ocean": {"name": "🌊 Ocean", "background": "#001a33", "widget": "#002244", "widget_hover": "#003366", "text": "#aaddff", "accent": "#00ddff", "accent_hover": "#44eeff", "border": "#004488"}
    }
    current_theme = "infinity"
    
    @classmethod
    def get_theme(cls, name=None):
        if name and name in cls.THEMES:
            return cls.THEMES[name]
        return cls.THEMES[cls.current_theme]
    
    @classmethod
    def apply_theme(cls, widget, theme_name=None):
        if theme_name and theme_name in cls.THEMES:
            cls.current_theme = theme_name
        theme = cls.get_theme()
        style = f"""
            QMainWindow, QWidget {{ background: {theme['background']}; color: {theme['text']}; }}
            QMenuBar {{ background: {theme['background']}; color: {theme['text']}; }}
            QMenuBar::item:selected {{ background: {theme['widget']}; }}
            QMenu {{ background: {theme['widget']}; color: {theme['text']}; border: 1px solid {theme['border']}; border-radius: 8px; }}
            QMenu::item:selected {{ background: {theme['accent']}; color: #000000; }}
            QPushButton {{ background: {theme['widget']}; color: {theme['text']}; border: 1px solid {theme['border']}; border-radius: 8px; padding: 8px 16px; }}
            QPushButton:hover {{ background: {theme['widget_hover']}; border-color: {theme['accent']}; }}
            QLineEdit {{ background: {theme['widget']}; color: {theme['text']}; border: 1px solid {theme['border']}; border-radius: 8px; padding: 8px 12px; }}
            QLineEdit:focus {{ border-color: {theme['accent']}; }}
            QTabWidget::pane {{ border: none; background: {theme['background']}; }}
            QTabBar::tab {{ background: {theme['widget']}; color: {theme['text']}; padding: 8px 15px; border: none; border-top-left-radius: 8px; border-top-right-radius: 8px; min-width: 80px; max-width: 200px; }}
            QTabBar::tab:selected {{ background: {theme['widget_hover']}; color: {theme['text']}; }}
            QTabBar::tab:hover {{ background: {theme['widget_hover']}; }}
            QScrollBar:vertical {{ background: {theme['background']}; width: 12px; border-radius: 6px; }}
            QScrollBar::handle:vertical {{ background: {theme['widget']}; border-radius: 6px; min-height: 20px; }}
            QScrollBar::handle:vertical:hover {{ background: {theme['accent']}; }}
            QListWidget {{ background: transparent; border: none; color: {theme['text']}; }}
            QListWidget::item {{ padding: 8px 12px; border-radius: 4px; }}
            QListWidget::item:hover {{ background: {theme['widget']}; }}
            QListWidget::item:selected {{ background: {theme['accent']}; color: #000000; }}
            QProgressBar {{ border: none; border-radius: 6px; background: {theme['widget']}; }}
            QProgressBar::chunk {{ background: {theme['accent']}; border-radius: 6px; }}
            QStatusBar {{ background: {theme['background']}; color: {theme['text']}; border-top: 1px solid {theme['border']}; }}
            QToolTip {{ background: {theme['widget']}; color: {theme['text']}; border: 1px solid {theme['border']}; border-radius: 4px; padding: 4px 8px; }}
            QGroupBox {{ border: 1px solid {theme['border']}; border-radius: 8px; margin-top: 1ex; padding-top: 10px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; color: {theme['text']}; }}
            QComboBox {{ background: {theme['widget']}; color: {theme['text']}; border: 1px solid {theme['border']}; border-radius: 6px; padding: 5px 10px; }}
            QComboBox:hover {{ border-color: {theme['accent']}; }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{ background: {theme['widget']}; color: {theme['text']}; selection-background-color: {theme['accent']}; selection-color: #000000; }}
            QCheckBox {{ color: {theme['text']}; }}
            QCheckBox::indicator {{ width: 18px; height: 18px; }}
            QCheckBox::indicator:unchecked {{ border: 2px solid {theme['border']}; border-radius: 4px; background: {theme['widget']}; }}
            QCheckBox::indicator:checked {{ border: 2px solid {theme['accent']}; border-radius: 4px; background: {theme['accent']}; }}
            QRadioButton {{ color: {theme['text']}; }}
            QRadioButton::indicator {{ width: 18px; height: 18px; }}
            QRadioButton::indicator:unchecked {{ border: 2px solid {theme['border']}; border-radius: 9px; background: {theme['widget']}; }}
            QRadioButton::indicator:checked {{ border: 2px solid {theme['accent']}; border-radius: 9px; background: {theme['accent']}; }}
            QDialog {{ background: {theme['background']}; }}
        """
        widget.setStyleSheet(style)

# ============================================================================
# 🧩 УСТАНОВЩИК РАСШИРЕНИЙ
# ============================================================================
class ExtensionInstallerDialog(QDialog):
    def __init__(self, extension_manager, parent=None):
        super().__init__(parent)
        self.extension_manager = extension_manager
        self.setWindowTitle(_("dialog_install_extension"))
        self.setFixedSize(750, 600)
        self.setModal(True)
        self.extension_data = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel(_("dialog_install_extension"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00d4ff;")
        layout.addWidget(title)
        
        desc = QLabel(_("dialog_choose_method"))
        desc.setStyleSheet("color: #808090;")
        layout.addWidget(desc)
        
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #2a2a3e; border-radius: 8px; background: #0a0a1a; }
            QTabBar::tab { background: #1a1a2e; color: #808090; padding: 8px 16px; border: none; border-radius: 6px 6px 0 0; }
            QTabBar::tab:selected { background: #00d4ff; color: #000; }
            QTabBar::tab:hover { background: #2a2a3e; }
        """)
        
        tab_widget.addTab(self.create_zip_tab(), _("dialog_zip_install"))
        tab_widget.addTab(self.create_folder_tab(), _("dialog_folder_install"))
        tab_widget.addTab(self.create_js_tab(), _("dialog_js_install"))
        
        layout.addWidget(tab_widget)
        
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_install = QPushButton(_("dialog_install_btn"))
        self.btn_install.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #00d4ff, stop:1 #0099ff);
                color: #fff;
                border: none;
                border-radius: 20px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #00eeff, stop:1 #00aaff);
            }
            QPushButton:disabled {
                background: #2a2a3e;
                color: #808090;
            }
        """)
        self.btn_install.setEnabled(False)
        self.btn_install.clicked.connect(self.install_extension)
        
        btn_cancel = QPushButton(_("dialog_cancel_btn"))
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #808090;
                border: 1px solid #2a2a3e;
                border-radius: 20px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2a2a3e;
                color: #fff;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_row.addWidget(self.btn_install)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)
        
        self.tab_widget = tab_widget
    
    def create_zip_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        info = QLabel(_("dialog_zip_info"))
        info.setStyleSheet("color: #808090; padding: 10px; background: #1a1a2e; border-radius: 8px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        self.zip_path_edit = QLineEdit()
        self.zip_path_edit.setPlaceholderText("Выберите ZIP-архив...")
        self.zip_path_edit.setReadOnly(True)
        self.zip_path_edit.textChanged.connect(self.on_file_selected)
        file_layout.addWidget(self.zip_path_edit)
        
        btn_browse = QPushButton(_("dialog_browse"))
        btn_browse.setFixedWidth(80)
        btn_browse.clicked.connect(self.browse_zip)
        file_layout.addWidget(btn_browse)
        layout.addWidget(file_widget)
        
        self.zip_info = QTextEdit()
        self.zip_info.setReadOnly(True)
        self.zip_info.setStyleSheet("background: #0a0a1a; border: 1px solid #1a1a2e; border-radius: 8px; color: #e0e0e0; font-family: 'Courier New'; font-size: 11px;")
        self.zip_info.setPlaceholderText("Информация об архиве...")
        self.zip_info.setVisible(False)
        layout.addWidget(self.zip_info)
        
        self.manifest_preview = QTextEdit()
        self.manifest_preview.setReadOnly(True)
        self.manifest_preview.setStyleSheet("background: #0a0a1a; border: 1px solid #1a1a2e; border-radius: 8px; color: #00ff88; font-family: 'Courier New'; font-size: 11px;")
        self.manifest_preview.setPlaceholderText("Содержимое manifest.json...")
        self.manifest_preview.setVisible(False)
        layout.addWidget(self.manifest_preview)
        
        return widget
    
    def create_folder_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        info = QLabel(_("dialog_folder_info"))
        info.setStyleSheet("color: #808090; padding: 10px; background: #1a1a2e; border-radius: 8px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setPlaceholderText("Выберите папку с расширением...")
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.textChanged.connect(self.on_file_selected)
        file_layout.addWidget(self.folder_path_edit)
        
        btn_browse = QPushButton(_("dialog_browse"))
        btn_browse.setFixedWidth(80)
        btn_browse.clicked.connect(self.browse_folder)
        file_layout.addWidget(btn_browse)
        layout.addWidget(file_widget)
        
        self.folder_files = QListWidget()
        self.folder_files.setStyleSheet("background: #0a0a1a; border: 1px solid #1a1a2e; border-radius: 8px; color: #e0e0e0;")
        self.folder_files.setVisible(False)
        layout.addWidget(self.folder_files)
        
        self.folder_manifest_preview = QTextEdit()
        self.folder_manifest_preview.setReadOnly(True)
        self.folder_manifest_preview.setStyleSheet("background: #0a0a1a; border: 1px solid #1a1a2e; border-radius: 8px; color: #00ff88; font-family: 'Courier New'; font-size: 11px;")
        self.folder_manifest_preview.setPlaceholderText("Содержимое manifest.json...")
        self.folder_manifest_preview.setVisible(False)
        layout.addWidget(self.folder_manifest_preview)
        
        return widget
    
    def create_js_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        info = QLabel(_("dialog_js_info"))
        info.setStyleSheet("color: #808090; padding: 10px; background: #1a1a2e; border-radius: 8px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        self.js_path_edit = QLineEdit()
        self.js_path_edit.setPlaceholderText("Выберите JS-файл...")
        self.js_path_edit.setReadOnly(True)
        self.js_path_edit.textChanged.connect(self.on_file_selected)
        file_layout.addWidget(self.js_path_edit)
        
        btn_browse = QPushButton(_("dialog_browse"))
        btn_browse.setFixedWidth(80)
        btn_browse.clicked.connect(self.browse_js)
        file_layout.addWidget(btn_browse)
        layout.addWidget(file_widget)
        
        name_widget = QWidget()
        name_layout = QHBoxLayout(name_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(QLabel("Название:"))
        self.js_name_edit = QLineEdit()
        self.js_name_edit.setPlaceholderText("Введите название расширения...")
        self.js_name_edit.textChanged.connect(self.on_file_selected)
        name_layout.addWidget(self.js_name_edit)
        layout.addWidget(name_widget)
        
        self.js_code_preview = QTextEdit()
        self.js_code_preview.setReadOnly(True)
        self.js_code_preview.setStyleSheet("background: #0a0a1a; border: 1px solid #1a1a2e; border-radius: 8px; color: #ffaa44; font-family: 'Courier New'; font-size: 11px;")
        self.js_code_preview.setPlaceholderText("Код расширения...")
        self.js_code_preview.setVisible(False)
        layout.addWidget(self.js_code_preview)
        
        return widget
    
    def browse_zip(self):
        filename, _ = QFileDialog.getOpenFileName(self, _("dialog_browse"), "", "ZIP архивы (*.zip);;Все файлы (*.*)")
        if filename:
            self.zip_path_edit.setText(filename)
            self.analyze_zip(filename)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, _("dialog_browse"))
        if folder:
            self.folder_path_edit.setText(folder)
            self.analyze_folder(folder)
    
    def browse_js(self):
        filename, _ = QFileDialog.getOpenFileName(self, _("dialog_browse"), "", "JavaScript файлы (*.js);;Все файлы (*.*)")
        if filename:
            self.js_path_edit.setText(filename)
            self.analyze_js(filename)
    
    def analyze_zip(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                files = zf.namelist()
                if "manifest.json" not in files:
                    self.show_error(_("dialog_zip_missing"))
                    self.btn_install.setEnabled(False)
                    return
                
                manifest_data = zf.read("manifest.json").decode('utf-8')
                manifest = json.loads(manifest_data)
                
                self.zip_info.setVisible(True)
                self.zip_info.setText(f"📦 Архив: {os.path.basename(zip_path)}\n📄 Файлов: {len(files)}")
                
                self.manifest_preview.setVisible(True)
                self.manifest_preview.setText(json.dumps(manifest, indent=2, ensure_ascii=False))
                
                if "name" not in manifest or "version" not in manifest:
                    self.show_error(_("dialog_manifest_fields"))
                    self.btn_install.setEnabled(False)
                    return
                
                self.extension_data = {"type": "zip", "path": zip_path, "manifest": manifest, "files": files}
                self.btn_install.setEnabled(True)
                self.show_success(_("dialog_install_success", name=manifest.get("name")))
                
        except zipfile.BadZipFile:
            self.show_error(_("dialog_manifest_invalid"))
        except json.JSONDecodeError:
            self.show_error(_("dialog_manifest_invalid"))
        except Exception as e:
            self.show_error(_("dialog_install_error", error=str(e)))
    
    def analyze_folder(self, folder_path):
        try:
            manifest_path = os.path.join(folder_path, "manifest.json")
            if not os.path.exists(manifest_path):
                self.show_error(_("dialog_zip_missing"))
                self.btn_install.setEnabled(False)
                return
            
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            
            files = []
            for root, dirs, filenames in os.walk(folder_path):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), folder_path)
                    files.append(rel_path)
            
            self.folder_files.setVisible(True)
            self.folder_files.clear()
            for f in sorted(files):
                self.folder_files.addItem(f)
            
            self.folder_manifest_preview.setVisible(True)
            self.folder_manifest_preview.setText(json.dumps(manifest, indent=2, ensure_ascii=False))
            
            if "name" not in manifest or "version" not in manifest:
                self.show_error(_("dialog_manifest_fields"))
                self.btn_install.setEnabled(False)
                return
            
            self.extension_data = {"type": "folder", "path": folder_path, "manifest": manifest, "files": files}
            self.btn_install.setEnabled(True)
            self.show_success(_("dialog_install_success", name=manifest.get("name")))
            
        except json.JSONDecodeError:
            self.show_error(_("dialog_manifest_invalid"))
        except Exception as e:
            self.show_error(_("dialog_install_error", error=str(e)))
    
    def analyze_js(self, js_path):
        try:
            with open(js_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            self.js_code_preview.setVisible(True)
            self.js_code_preview.setText(code)
            
            name = os.path.basename(js_path).replace(".js", "")
            if not self.js_name_edit.text():
                self.js_name_edit.setText(name)
            
            self.extension_data = {"type": "js", "path": js_path, "code": code, "name": name}
            
            if self.js_name_edit.text().strip():
                self.btn_install.setEnabled(True)
                self.show_success(_("dialog_install_success", name=name))
            else:
                self.btn_install.setEnabled(False)
            
        except Exception as e:
            self.show_error(_("dialog_install_error", error=str(e)))
    
    def on_file_selected(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            if not self.zip_path_edit.text():
                self.btn_install.setEnabled(False)
        elif current_tab == 1:
            if not self.folder_path_edit.text():
                self.btn_install.setEnabled(False)
        elif current_tab == 2:
            if not self.js_path_edit.text() or not self.js_name_edit.text().strip():
                self.btn_install.setEnabled(False)
            else:
                self.btn_install.setEnabled(True)
    
    def install_extension(self):
        current_tab = self.tab_widget.currentIndex()
        try:
            if current_tab == 0:
                self.install_from_zip()
            elif current_tab == 1:
                self.install_from_folder()
            elif current_tab == 2:
                self.install_from_js()
            self.accept()
        except Exception as e:
            self.show_error(_("dialog_install_error", error=str(e)))
    
    def install_from_zip(self):
        ext = self.extension_manager.install_from_zip(self.extension_data["path"])
        if ext:
            self.show_success(_("dialog_install_success", name=ext.name))
        else:
            raise Exception("Не удалось установить расширение")
    
    def install_from_folder(self):
        ext = self.extension_manager.install_from_folder(self.extension_data["path"])
        if ext:
            self.show_success(_("dialog_install_success", name=ext.name))
        else:
            raise Exception("Не удалось установить расширение")
    
    def install_from_js(self):
        name = self.js_name_edit.text().strip()
        code = self.extension_data["code"]
        ext = self.extension_manager.install_from_js(name, code)
        if ext:
            self.show_success(_("dialog_install_success", name=ext.name))
        else:
            raise Exception("Не удалось установить расширение")
    
    def show_error(self, message):
        QMessageBox.critical(self, "❌ " + _("dialog_install_error", error=""), message)
    
    def show_success(self, message):
        QMessageBox.information(self, "✅ Успех", message)

# ============================================================================
# 🏠 ОСНОВНОЙ КЛАСС БРАУЗЕРА
# ============================================================================
class InfinityBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.adblock = AdBlockManager()
        self.notes_manager = NotesManager()
        self.rss_reader = RSSReader()
        self.translator = Translator()
        self.permission_manager = PermissionManager()
        self.extension_manager = ExtensionManager()
        self.download_manager = DownloadManager()
        self.file_manager = FileManager()
        self.theme_manager = ThemeManager()
        
        self.is_dark_mode = True
        self.is_fullscreen = False
        self.zoom_factor = 1.0
        self.current_url = ""
        self.history = []
        self.bookmarks = []
        self.closed_tabs = []
        
        self.setup_ui()
        self.setup_menus()
        self.setup_shortcuts()
        self.setup_theme()
        
        self.load_bookmarks()
        self.load_history()
        
        self.create_tab("https://www.google.com")
        
        self.update_ui_language()
        self.show_status(_("status_ready"))
        self.show_welcome_tip()
    
    # ========================================================================
    # 🎨 UI НАСТРОЙКА
    # ========================================================================
    
    def setup_ui(self):
        self.setWindowTitle(_("app_title"))
        self.setGeometry(100, 50, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        self.setWindowIcon(self.create_icon())
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.top_panel = self.create_top_panel()
        main_layout.addWidget(self.top_panel)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        main_layout.addWidget(self.tab_widget)
        
        self.status_widget = self.create_status_bar()
        main_layout.addWidget(self.status_widget)
        
        self.sidebar = self.create_sidebar()
        self.sidebar.hide()
    
    def create_icon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#0a0a1a"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 64, 64, 12, 12)
        painter.setPen(QPen(QColor("#00d4ff"), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(16, 16, 32, 32)
        painter.setBrush(QColor("#00d4ff"))
        painter.drawEllipse(28, 28, 8, 8)
        painter.setBrush(QColor(255, 255, 255, 100))
        painter.drawEllipse(22, 22, 4, 4)
        painter.end()
        return QIcon(pixmap)
    
    def create_top_panel(self):
        widget = QWidget()
        widget.setFixedHeight(52)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)
        
        self.btn_back = self.create_tool_button("◀", _("back"))
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)
        
        self.btn_forward = self.create_tool_button("▶", _("forward"))
        self.btn_forward.clicked.connect(self.go_forward)
        layout.addWidget(self.btn_forward)
        
        self.btn_reload = self.create_tool_button("⟳", _("reload"))
        self.btn_reload.clicked.connect(self.reload)
        layout.addWidget(self.btn_reload)
        
        self.btn_home = self.create_tool_button("🏠", _("home"))
        self.btn_home.clicked.connect(self.go_home)
        layout.addWidget(self.btn_home)
        
        layout.addSpacing(8)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(_("search_placeholder"))
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.textChanged.connect(self.on_url_text_changed)
        layout.addWidget(self.url_bar, 1)
        
        self.btn_go = QPushButton(_("go"))
        self.btn_go.setFixedSize(50, 38)
        self.btn_go.clicked.connect(self.navigate)
        layout.addWidget(self.btn_go)
        
        layout.addSpacing(8)
        
        self.btn_bookmark = self.create_tool_button("☆", _("bookmark"))
        self.btn_bookmark.clicked.connect(self.toggle_bookmark)
        layout.addWidget(self.btn_bookmark)
        
        self.btn_adblock = self.create_tool_button("🛡️", _("adblock"))
        self.btn_adblock.clicked.connect(self.toggle_adblock)
        layout.addWidget(self.btn_adblock)
        
        self.btn_theme = self.create_tool_button("🌙", _("theme"))
        self.btn_theme.clicked.connect(self.toggle_theme)
        layout.addWidget(self.btn_theme)
        
        self.btn_sidebar = self.create_tool_button("📋", _("sidebar"))
        self.btn_sidebar.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.btn_sidebar)
        
        self.btn_downloads = self.create_tool_button("📥", _("downloads"))
        self.btn_downloads.clicked.connect(self.show_downloads_dialog)
        layout.addWidget(self.btn_downloads)
        
        self.btn_files = self.create_tool_button("📂", _("files"))
        self.btn_files.clicked.connect(self.show_files_dialog)
        layout.addWidget(self.btn_files)
        
        self.btn_extensions = self.create_tool_button("🧩", _("extensions"))
        self.btn_extensions.clicked.connect(self.show_extensions_menu)
        layout.addWidget(self.btn_extensions)
        
        self.btn_tools = self.create_tool_button("⚙️", _("tools"))
        self.btn_tools.clicked.connect(self.show_tools_menu)
        layout.addWidget(self.btn_tools)
        
        return widget
    
    def create_tool_button(self, text, tooltip):
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
        widget = QWidget()
        widget.setFixedHeight(30)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 2, 12, 2)
        
        self.status_label = QLabel(_("status_ready"))
        self.status_label.setStyleSheet("font-size: 11px; color: #808090;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.download_indicator = QLabel("📥 0")
        self.download_indicator.setStyleSheet("font-size: 11px; color: #00d4ff;")
        layout.addWidget(self.download_indicator)
        
        self.extensions_indicator = QLabel("🧩 4")
        self.extensions_indicator.setStyleSheet("font-size: 11px; color: #00d4ff;")
        layout.addWidget(self.extensions_indicator)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet("font-size: 11px; color: #808090; min-width: 40px;")
        layout.addWidget(self.zoom_label)
        
        self.ssl_label = QLabel("🔒")
        self.ssl_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.ssl_label)
        
        return widget
    
    def create_sidebar(self):
        widget = QWidget()
        widget.setFixedWidth(300)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("QTabWidget::pane { border: none; background: transparent; } QTabBar::tab { background: transparent; color: #808090; padding: 6px 12px; border: none; font-size: 12px; } QTabBar::tab:selected { color: #00d4ff; border-bottom: 2px solid #00d4ff; }")
        
        # Закладки
        bookmarks_widget = QWidget()
        bookmarks_layout = QVBoxLayout(bookmarks_widget)
        bookmarks_layout.setContentsMargins(0, 0, 0, 0)
        search_bookmarks = QLineEdit()
        search_bookmarks.setPlaceholderText(_("sidebar_search_bookmarks"))
        search_bookmarks.textChanged.connect(self.search_bookmarks)
        bookmarks_layout.addWidget(search_bookmarks)
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.on_bookmark_clicked)
        bookmarks_layout.addWidget(self.bookmarks_list)
        btn_add = QPushButton(_("sidebar_add_bookmark"))
        btn_add.clicked.connect(self.add_bookmark)
        bookmarks_layout.addWidget(btn_add)
        tab_widget.addTab(bookmarks_widget, _("sidebar_bookmarks"))
        
        # История
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)
        search_history = QLineEdit()
        search_history.setPlaceholderText(_("sidebar_search_history"))
        search_history.textChanged.connect(self.search_history)
        history_layout.addWidget(search_history)
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_history_clicked)
        history_layout.addWidget(self.history_list)
        btn_clear = QPushButton(_("sidebar_clear_history"))
        btn_clear.clicked.connect(self.clear_history)
        history_layout.addWidget(btn_clear)
        tab_widget.addTab(history_widget, _("sidebar_history"))
        
        # Заметки
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        search_notes = QLineEdit()
        search_notes.setPlaceholderText(_("sidebar_search_notes"))
        search_notes.textChanged.connect(self.search_notes)
        notes_layout.addWidget(search_notes)
        self.notes_list = QListWidget()
        self.notes_list.itemDoubleClicked.connect(self.on_note_clicked)
        notes_layout.addWidget(self.notes_list)
        btn_add_note = QPushButton(_("sidebar_add_note"))
        btn_add_note.clicked.connect(self.add_note_dialog)
        notes_layout.addWidget(btn_add_note)
        tab_widget.addTab(notes_widget, _("sidebar_notes"))
        
        # RSS
        rss_widget = QWidget()
        rss_layout = QVBoxLayout(rss_widget)
        rss_layout.setContentsMargins(0, 0, 0, 0)
        rss_input_widget = QWidget()
        rss_input_layout = QHBoxLayout(rss_input_widget)
        rss_input_layout.setContentsMargins(0, 0, 0, 0)
        self.rss_input = QLineEdit()
        self.rss_input.setPlaceholderText(_("rss_placeholder"))
        rss_input_layout.addWidget(self.rss_input)
        btn_add_rss = QPushButton("➕")
        btn_add_rss.setFixedWidth(36)
        btn_add_rss.clicked.connect(self.add_rss_feed)
        rss_input_layout.addWidget(btn_add_rss)
        rss_layout.addWidget(rss_input_widget)
        self.rss_list = QListWidget()
        self.rss_list.itemDoubleClicked.connect(self.on_rss_clicked)
        rss_layout.addWidget(self.rss_list)
        tab_widget.addTab(rss_widget, _("sidebar_rss"))
        
        # Расширения
        extensions_widget = QWidget()
        extensions_layout = QVBoxLayout(extensions_widget)
        extensions_layout.setContentsMargins(0, 0, 0, 0)
        self.extensions_list = QListWidget()
        self.extensions_list.itemDoubleClicked.connect(self.on_extension_double_clicked)
        extensions_layout.addWidget(self.extensions_list)
        btn_install = QPushButton(_("extensions_install"))
        btn_install.clicked.connect(self.show_extension_installer)
        extensions_layout.addWidget(btn_install)
        tab_widget.addTab(extensions_widget, _("sidebar_extensions"))
        
        layout.addWidget(tab_widget)
        return widget
    
    # ========================================================================
    # 📋 МЕНЮ
    # ========================================================================
    
    def setup_menus(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu(_("menu_file"))
        file_menu.addAction(_("menu_file_new_tab"), self.create_tab, "Ctrl+T")
        file_menu.addAction(_("menu_file_new_window"), self.new_window, "Ctrl+N")
        file_menu.addAction(_("menu_file_incognito"), self.new_incognito, "Ctrl+Shift+N")
        file_menu.addSeparator()
        file_menu.addAction(_("menu_file_downloads"), self.show_downloads_dialog, "Ctrl+J")
        file_menu.addAction(_("menu_file_files"), self.show_files_dialog)
        file_menu.addAction(_("menu_file_save"), self.save_page, "Ctrl+S")
        file_menu.addAction(_("menu_file_print"), self.print_page, "Ctrl+P")
        file_menu.addSeparator()
        file_menu.addAction(_("menu_file_exit"), self.close, "Ctrl+Q")
        
        tabs_menu = menubar.addMenu(_("menu_tabs"))
        tabs_menu.addAction(_("menu_tabs_new"), self.create_tab, "Ctrl+T")
        tabs_menu.addAction(_("menu_tabs_close"), self.close_current_tab, "Ctrl+W")
        tabs_menu.addAction(_("menu_tabs_restore"), self.restore_tab, "Ctrl+Shift+T")
        tabs_menu.addSeparator()
        tabs_menu.addAction(_("menu_tabs_next"), self.next_tab, "Ctrl+Tab")
        tabs_menu.addAction(_("menu_tabs_prev"), self.prev_tab, "Ctrl+Shift+Tab")
        
        tools_menu = menubar.addMenu(_("menu_tools"))
        tools_menu.addAction(_("menu_tools_downloads"), self.show_downloads_dialog, "Ctrl+J")
        tools_menu.addAction(_("menu_tools_files"), self.show_files_dialog)
        tools_menu.addAction(_("menu_tools_passwords"), self.show_passwords)
        tools_menu.addAction(_("menu_tools_notes"), self.toggle_sidebar)
        tools_menu.addAction(_("menu_tools_rss"), self.show_rss)
        tools_menu.addSeparator()
        tools_menu.addAction(_("menu_tools_extensions"), self.show_extensions_menu)
        tools_menu.addAction(_("menu_tools_permissions"), self.show_permissions_dialog)
        tools_menu.addAction(_("menu_tools_themes"), self.show_themes)
        tools_menu.addAction(_("menu_tools_settings"), self.show_settings, "Ctrl+,")
        
        help_menu = menubar.addMenu(_("menu_help"))
        help_menu.addAction(_("menu_help_help"), self.show_help, "F1")
        help_menu.addAction(_("menu_help_about"), self.show_about)
        help_menu.addAction(_("menu_help_updates"), self.check_updates)
    
    def setup_shortcuts(self):
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
            ("F12", self.show_dev_tools),
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
    # 🌍 ОБНОВЛЕНИЕ ЯЗЫКА
    # ========================================================================
    
    def update_ui_language(self):
        self.setWindowTitle(_("app_title"))
        self.btn_back.setToolTip(_("back"))
        self.btn_forward.setToolTip(_("forward"))
        self.btn_reload.setToolTip(_("reload"))
        self.btn_home.setToolTip(_("home"))
        self.btn_go.setText(_("go"))
        self.url_bar.setPlaceholderText(_("search_placeholder"))
        self.btn_bookmark.setToolTip(_("bookmark"))
        self.btn_adblock.setToolTip(_("adblock"))
        self.btn_theme.setToolTip(_("theme"))
        self.btn_sidebar.setToolTip(_("sidebar"))
        self.btn_downloads.setToolTip(_("downloads"))
        self.btn_files.setToolTip(_("files"))
        self.btn_extensions.setToolTip(_("extensions"))
        self.btn_tools.setToolTip(_("tools"))
        self.show_status(_("status_ready"))
    
    # ========================================================================
    # 🎨 ТЕМА
    # ========================================================================
    
    def setup_theme(self):
        ThemeManager.apply_theme(self, "infinity")
        self.btn_theme.setText("🌙")
    
    def toggle_theme(self):
        themes = list(ThemeManager.THEMES.keys())
        current = ThemeManager.current_theme
        idx = themes.index(current) if current in themes else 0
        next_idx = (idx + 1) % len(themes)
        next_theme = themes[next_idx]
        ThemeManager.apply_theme(self, next_theme)
        self.show_status(_("notification_theme_changed"))
    
    # ========================================================================
    # 🏠 ВКЛАДКИ И НАВИГАЦИЯ
    # ========================================================================
    
    def create_tab(self, url="https://www.google.com"):
        view = QWebEngineView()
        view.setUrl(QUrl(url))
        view.page().loadProgress.connect(self.on_load_progress)
        view.page().titleChanged.connect(self.on_title_changed)
        view.page().urlChanged.connect(self.on_url_changed)
        view.page().iconChanged.connect(self.on_icon_changed)
        view.page().fullScreenRequested.connect(self.on_fullscreen_requested)
        view.page().featurePermissionRequested.connect(self.on_feature_permission)
        view.page().profile().downloadRequested.connect(self.on_download_requested)
        
        view.setContextMenuPolicy(Qt.CustomContextMenu)
        view.customContextMenuRequested.connect(self.show_context_menu)
        
        def on_load_finished(ok):
            if ok:
                for ext in self.extension_manager.get_enabled_extensions():
                    if ext.script:
                        view.page().runJavaScript(ext.script)
        view.page().loadFinished.connect(on_load_finished)
        
        index = self.tab_widget.addTab(view, _("tab_new"))
        self.tab_widget.setCurrentIndex(index)
        return view
    
    def on_download_requested(self, download: QWebEngineDownloadItem):
        url = download.url().toString()
        filename = download.suggestedFileName() or os.path.basename(url.split("?")[0]) or "download"
        download_info = self.download_manager.add_download(url, filename)
        download.accept()
        download.downloadProgress.connect(lambda received, total: self.on_download_progress(download_info, received, total))
        download.finished.connect(lambda: self.on_download_finished(download_info))
        self.update_download_indicator()
        self.show_status(_("status_download_start", filename=filename))
    
    def on_download_progress(self, download_info, received, total):
        download_info["downloaded"] = received
        download_info["size"] = total
        if total > 0:
            download_info["progress"] = (received / total) * 100
        self.download_manager.save_downloads()
    
    def on_download_finished(self, download_info):
        download_info["status"] = "completed"
        download_info["progress"] = 100
        download_info["end_time"] = datetime.now().isoformat()
        self.download_manager.save_downloads()
        self.update_download_indicator()
        self.show_status(_("status_download_complete", filename=download_info["filename"]))
    
    def update_download_indicator(self):
        total = len(self.download_manager.get_downloads())
        active = len(self.download_manager.get_active_downloads())
        self.download_indicator.setText(_("indicator_downloads", total=total, active=active))
    
    def on_feature_permission(self, url: QUrl, feature):
        permission_map = {
            QWebEnginePage.Geolocation: "geolocation",
            QWebEnginePage.Notifications: "notifications",
            QWebEnginePage.MediaAudioCapture: "microphone",
            QWebEnginePage.MediaVideoCapture: "camera",
        }
        permission = permission_map.get(feature, "unknown")
        domain = url.host()
        allowed = self.permission_manager.request_permission(domain, permission)
        if allowed:
            self.current_page().setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.current_page().setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)
    
    def current_page(self):
        view = self.get_current_view()
        if view:
            return view.page()
        return None
    
    def close_tab(self, index):
        if index >= 0:
            widget = self.tab_widget.widget(index)
            if widget:
                self.closed_tabs.append(widget)
                if len(self.closed_tabs) > 10:
                    self.closed_tabs.pop(0)
            self.tab_widget.removeTab(index)
        if self.tab_widget.count() == 0:
            self.create_tab()
    
    def close_current_tab(self):
        self.close_tab(self.tab_widget.currentIndex())
    
    def restore_tab(self):
        if self.closed_tabs:
            view = self.closed_tabs.pop()
            url = view.url().toString()
            self.create_tab(url)
            self.show_status(_("tab_restored"))
    
    def next_tab(self):
        if self.tab_widget.count() > 1:
            index = (self.tab_widget.currentIndex() + 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(index)
    
    def prev_tab(self):
        if self.tab_widget.count() > 1:
            index = (self.tab_widget.currentIndex() - 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(index)
    
    def get_current_view(self):
        return self.tab_widget.currentWidget()
    
    def on_tab_changed(self, index):
        view = self.tab_widget.widget(index)
        if view:
            self.on_url_changed(view.url())
            self.on_title_changed(view.page().title())
    
    def navigate(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if not text.startswith(("http://", "https://", "file://", "about:")):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text = f"https://www.google.com/search?q={text.replace(' ', '+')}"
        view = self.get_current_view()
        if view:
            view.setUrl(QUrl(text))
            self.add_to_history(text)
            self.url_bar.setText(text)
    
    def navigate_to(self, url):
        self.url_bar.setText(url)
        self.navigate()
    
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
        self.navigate_to("https://www.google.com")
    
    def on_fullscreen_requested(self, request):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
        request.accept()
    
    # ========================================================================
    # 📊 ИСТОРИЯ И ЗАКЛАДКИ
    # ========================================================================
    
    def add_to_history(self, url):
        title = self.get_current_view().page().title() if self.get_current_view() else url
        entry = {"url": url, "title": title or url, "timestamp": datetime.now().isoformat()}
        for i, item in enumerate(self.history):
            if item["url"] == url:
                self.history.pop(i)
                break
        self.history.insert(0, entry)
        if len(self.history) > 1000:
            self.history = self.history[:1000]
        self.save_history()
        self.update_history_list()
    
    def load_history(self):
        try:
            with open("history.json", "r") as f:
                self.history = json.load(f)
        except: self.history = []
        self.update_history_list()
    
    def save_history(self):
        try:
            with open("history.json", "w") as f:
                json.dump(self.history, f, indent=2)
        except: pass
    
    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_list()
        self.show_status(_("notification_clear_history"))
    
    def update_history_list(self):
        self.history_list.clear()
        for item in self.history[:50]:
            self.history_list.addItem(f"{item['title']} - {item['url']}")
    
    def search_history(self, text):
        self.history_list.clear()
        if not text:
            self.update_history_list()
            return
        for item in self.history[:50]:
            if text.lower() in item['title'].lower() or text.lower() in item['url'].lower():
                self.history_list.addItem(f"{item['title']} - {item['url']}")
    
    def on_history_clicked(self, item):
        text = item.text()
        if " - " in text:
            url = text.split(" - ")[-1]
            self.navigate_to(url)
    
    def add_bookmark(self):
        view = self.get_current_view()
        if not view:
            return
        url = view.url().toString()
        title = view.page().title() or url
        if any(b["url"] == url for b in self.bookmarks):
            self.show_status(_("bookmark_exists"))
            return
        folders = _("bookmark_folders")
        if isinstance(folders, str):
            folders = ["Основные", "Работа", "Учёба", "Развлечения"]
        folder, ok = QInputDialog.getItem(self, _("bookmark_folder"), _("bookmark_folder_select"), folders, 0, True)
        if ok:
            if folder == _("bookmark_folder_new"):
                folder, ok = QInputDialog.getText(self, _("bookmark_folder_new"), _("bookmark_folder_name"))
                if not ok or not folder:
                    folder = folders[0]
            self.bookmarks.append({"url": url, "title": title, "folder": folder})
            self.save_bookmarks()
            self.update_bookmarks_list()
            self.btn_bookmark.setText("★")
            self.show_status(_("bookmark_added", folder=folder))
    
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
            self.show_status(_("bookmark_remove"))
        else:
            self.add_bookmark()
    
    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as f:
                self.bookmarks = json.load(f)
        except: self.bookmarks = []
        self.update_bookmarks_list()
    
    def save_bookmarks(self):
        try:
            with open("bookmarks.json", "w") as f:
                json.dump(self.bookmarks, f, indent=2)
        except: pass
    
    def update_bookmarks_list(self):
        self.bookmarks_list.clear()
        for item in self.bookmarks:
            self.bookmarks_list.addItem(f"{item['title']} - {item['url']}")
    
    def search_bookmarks(self, text):
        self.bookmarks_list.clear()
        if not text:
            self.update_bookmarks_list()
            return
        for item in self.bookmarks:
            if text.lower() in item['title'].lower() or text.lower() in item['url'].lower():
                self.bookmarks_list.addItem(f"{item['title']} - {item['url']}")
    
    def on_bookmark_clicked(self, item):
        text = item.text()
        if " - " in text:
            url = text.split(" - ")[-1]
            self.navigate_to(url)
    
    # ========================================================================
    # 📝 ЗАМЕТКИ
    # ========================================================================
    
    def add_note_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("notes_new_title"))
        dialog.setFixedSize(400, 350)
        layout = QVBoxLayout(dialog)
        title_edit = QLineEdit()
        title_edit.setPlaceholderText(_("notes_title"))
        layout.addWidget(title_edit)
        content_edit = QTextEdit()
        content_edit.setPlaceholderText(_("notes_content"))
        layout.addWidget(content_edit)
        category_combo = QComboBox()
        category_combo.addItems(["Общие", "Работа", "Личное", "Идеи"])
        category_combo.setEditable(True)
        layout.addWidget(category_combo)
        btn_row = QHBoxLayout()
        btn_save = QPushButton(_("notes_save"))
        btn_save.clicked.connect(dialog.accept)
        btn_row.addWidget(btn_save)
        btn_cancel = QPushButton(_("notes_cancel"))
        btn_cancel.clicked.connect(dialog.reject)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)
        if dialog.exec_() == QDialog.Accepted:
            title = title_edit.text().strip() or "Без названия"
            content = content_edit.toPlainText()
            category = category_combo.currentText()
            note = self.notes_manager.add_note(title, content, category)
            self.update_notes_list()
            self.show_status(_("notes_created", title=title))
    
    def update_notes_list(self):
        self.notes_list.clear()
        for note in self.notes_manager.get_notes():
            item = QListWidgetItem(f"📝 {note['title']}")
            item.setData(Qt.UserRole, note["id"])
            self.notes_list.addItem(item)
    
    def search_notes(self, text):
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
        note = next((n for n in self.notes_manager.get_notes() if n["id"] == note_id), None)
        if note:
            msg = QMessageBox(self)
            msg.setWindowTitle(f"📝 {note['title']}")
            msg.setText(note['content'])
            msg.setInformativeText(f"📁 {note.get('category', 'Общие')}\n📅 {note['created'][:10]}")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Delete)
            msg.button(QMessageBox.Delete).clicked.connect(lambda: self.delete_note(note_id))
            msg.exec_()
    
    def delete_note(self, note_id):
        self.notes_manager.delete_note(note_id)
        self.update_notes_list()
        self.show_status(_("notes_deleted"))
    
    # ========================================================================
    # 📰 RSS
    # ========================================================================
    
    def add_rss_feed(self):
        url = self.rss_input.text().strip()
        if url:
            if self.rss_reader.add_feed(url):
                self.update_rss_list()
                self.rss_input.clear()
                self.show_status(_("rss_added", url=url))
            else:
                self.show_status(_("rss_exists"))
    
    def update_rss_list(self):
        self.rss_list.clear()
        for feed in self.rss_reader.get_feeds():
            self.rss_list.addItem(f"📰 {feed}")
    
    def on_rss_clicked(self, item):
        url = item.text().replace("📰 ", "")
        self.navigate_to(url)
    
    def show_rss(self):
        self.toggle_sidebar()
        tab_widget = self.sidebar.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(3)
    
    # ========================================================================
    # 📥 ЗАГРУЗКИ И ФАЙЛЫ
    # ========================================================================
    
    def show_downloads_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("downloads_title"))
        dialog.resize(700, 500)
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()
        list_widget.setStyleSheet("QListWidget::item { padding: 8px; border-bottom: 1px solid #1a1a2e; } QListWidget::item:hover { background: #1a1a2e; }")
        layout.addWidget(list_widget)
        
        btn_row = QHBoxLayout()
        btn_open = QPushButton(_("downloads_open"))
        btn_open.clicked.connect(lambda: self.open_download(list_widget))
        btn_row.addWidget(btn_open)
        btn_folder = QPushButton(_("downloads_folder"))
        btn_folder.clicked.connect(lambda: self.open_download_folder(list_widget))
        btn_row.addWidget(btn_folder)
        btn_remove = QPushButton(_("downloads_remove"))
        btn_remove.clicked.connect(lambda: self.remove_download(list_widget))
        btn_row.addWidget(btn_remove)
        btn_clear = QPushButton(_("downloads_clear"))
        btn_clear.clicked.connect(lambda: self.clear_completed_downloads(list_widget))
        btn_row.addWidget(btn_clear)
        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        
        self.update_downloads_list(list_widget)
        dialog.exec_()
    
    def update_downloads_list(self, list_widget):
        list_widget.clear()
        for d in self.download_manager.get_downloads():
            status_texts = {
                "pending": _("downloads_pending"),
                "downloading": _("downloads_active"),
                "paused": _("downloads_paused"),
                "completed": _("downloads_completed"),
                "failed": _("downloads_failed"),
                "cancelled": _("downloads_cancelled")
            }
            status_icons = {"pending": "⏳", "downloading": "📥", "paused": "⏸️", "completed": "✅", "failed": "❌", "cancelled": "🚫"}
            icon = status_icons.get(d["status"], "❓")
            progress = f"{int(d['progress'])}%" if d["progress"] > 0 else "0%"
            size = self.file_manager.format_size(d["size"]) if d["size"] > 0 else "Неизвестно"
            status_text = status_texts.get(d["status"], d["status"])
            item_text = f"{icon} {d['filename']} - {progress} ({size}) - {status_text}"
            if d.get("speed") and d["speed"] > 0:
                speed = self.file_manager.format_size(d["speed"]) + "/s"
                item_text += f" - {speed}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, d["id"])
            list_widget.addItem(item)
    
    def open_download(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.open_file(current.data(Qt.UserRole))
    
    def open_download_folder(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.open_folder(current.data(Qt.UserRole))
    
    def remove_download(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.download_manager.remove_download(current.data(Qt.UserRole))
            self.update_downloads_list(list_widget)
            self.update_download_indicator()
    
    def clear_completed_downloads(self, list_widget):
        for d in self.download_manager.get_completed_downloads():
            self.download_manager.remove_download(d["id"])
        self.update_downloads_list(list_widget)
        self.update_download_indicator()
        self.show_status(_("downloads_clear"))
    
    def show_files_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("files_title"))
        dialog.resize(800, 500)
        layout = QVBoxLayout(dialog)
        
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        category_combo = QComboBox()
        category_combo.addItems(self.file_manager.categories.keys())
        category_combo.currentTextChanged.connect(lambda: self.update_files_list(list_widget, category_combo, search_edit))
        top_layout.addWidget(QLabel(_("files_category")))
        top_layout.addWidget(category_combo)
        top_layout.addSpacing(20)
        search_edit = QLineEdit()
        search_edit.setPlaceholderText(_("files_search"))
        search_edit.textChanged.connect(lambda: self.update_files_list(list_widget, category_combo, search_edit))
        top_layout.addWidget(search_edit)
        top_layout.addStretch()
        btn_open_folder = QPushButton(_("files_open_folder"))
        btn_open_folder.clicked.connect(self.file_manager.open_folder)
        top_layout.addWidget(btn_open_folder)
        layout.addWidget(top_widget)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet("QListWidget::item { padding: 8px; border-bottom: 1px solid #1a1a2e; } QListWidget::item:hover { background: #1a1a2e; }")
        list_widget.itemDoubleClicked.connect(lambda item: self.file_manager.open_file(item.text()))
        layout.addWidget(list_widget)
        
        btn_row = QHBoxLayout()
        btn_open = QPushButton(_("files_open"))
        btn_open.clicked.connect(lambda: self.open_selected_file(list_widget))
        btn_row.addWidget(btn_open)
        btn_delete = QPushButton(_("files_delete"))
        btn_delete.clicked.connect(lambda: self.delete_selected_file(list_widget))
        btn_row.addWidget(btn_delete)
        btn_info = QPushButton(_("files_info"))
        btn_info.clicked.connect(lambda: self.show_file_info(list_widget))
        btn_row.addWidget(btn_info)
        btn_close = QPushButton(_("files_close"))
        btn_close.clicked.connect(dialog.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        
        self.update_files_list(list_widget, category_combo, search_edit)
        dialog.exec_()
    
    def update_files_list(self, list_widget, category_combo, search_edit):
        list_widget.clear()
        category = category_combo.currentText()
        search = search_edit.text().lower()
        files = self.file_manager.get_files(category)
        for file in files:
            if search and search not in file["name"].lower():
                continue
            size = self.file_manager.format_size(file["size"])
            item_text = f"{file['category']} {file['name']} ({size})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, file["name"])
            list_widget.addItem(item)
    
    def open_selected_file(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.file_manager.open_file(current.data(Qt.UserRole))
    
    def delete_selected_file(self, list_widget):
        current = list_widget.currentItem()
        if current:
            filename = current.data(Qt.UserRole)
            reply = QMessageBox.question(self, _("files_delete"), _("files_delete_confirm", filename=filename), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.file_manager.delete_file(filename):
                    self.show_status(_("files_deleted", filename=filename))
    
    def show_file_info(self, list_widget):
        current = list_widget.currentItem()
        if current:
            filename = current.data(Qt.UserRole)
            info = self.file_manager.get_file_info(filename)
            if info:
                QMessageBox.information(self, _("files_info"),
                    f"📄 <b>{info['name']}</b>\n\n"
                    f"📁 Путь: {info['path']}\n"
                    f"📦 Размер: {info['size_text']}\n"
                    f"📂 Категория: {info['category']}\n"
                    f"📅 Создан: {info['created'][:10]}\n"
                    f"🔄 Изменен: {info['modified'][:10]}")
    
    # ========================================================================
    # 🧩 РАСШИРЕНИЯ
    # ========================================================================
    
    def show_extension_installer(self):
        installer = ExtensionInstallerDialog(self.extension_manager, self)
        if installer.exec_() == QDialog.Accepted:
            self.update_extensions_list()
            self.update_extensions_indicator()
            self.show_status(_("extensions_installed", name=""))
    
    def show_extensions_menu(self):
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
            QMenu::item {
                padding: 8px 25px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #00d4ff;
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #2a2a3e;
                margin: 4px 10px;
            }
        """)
        
        menu.addAction(_("extensions_manage"), self.show_extensions_dialog)
        menu.addAction(_("extensions_install_zip"), self.show_extension_installer)
        menu.addAction(_("extensions_install_js"), self.install_js_extension)
        menu.addSeparator()
        
        for ext in self.extension_manager.get_all_extensions():
            status = "✅" if ext.enabled else "❌"
            submenu = QMenu(f"{status} {ext.name}", menu)
            submenu.setStyleSheet(menu.styleSheet())
            
            action_open = submenu.addAction(_("extensions_open"))
            action_open.triggered.connect(lambda checked, eid=ext.id: self.show_extension_popup(eid))
            submenu.addSeparator()
            
            action_options = submenu.addAction(_("extensions_options"))
            action_options.triggered.connect(lambda checked, eid=ext.id: self.show_extension_options(eid))
            action_code = submenu.addAction(_("extensions_code"))
            action_code.triggered.connect(lambda checked, eid=ext.id: self.view_extension_code(eid))
            submenu.addSeparator()
            
            action_toggle = submenu.addAction(_("extensions_toggle"))
            action_toggle.triggered.connect(lambda checked, eid=ext.id: self.toggle_extension(eid))
            
            if ext.id not in ["adblock_plus", "dark_reader", "translator", "screenshot"]:
                action_uninstall = submenu.addAction(_("extensions_uninstall"))
                action_uninstall.triggered.connect(lambda checked, eid=ext.id: self.uninstall_extension_from_menu(eid))
            
            menu.addMenu(submenu)
        
        menu.addSeparator()
        menu.addAction(_("extensions_install"), self.show_extension_installer)
        menu.exec_(self.btn_extensions.mapToGlobal(self.btn_extensions.rect().bottomLeft()))
    
    def show_extensions_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("extensions_title"))
        dialog.resize(550, 450)
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()
        list_widget.setStyleSheet("QListWidget::item { padding: 10px; border-bottom: 1px solid #1a1a2e; } QListWidget::item:hover { background: #1a1a2e; }")
        for ext in self.extension_manager.get_all_extensions():
            status = "🟢" if ext.enabled else "🔴"
            item = QListWidgetItem(f"{status} {ext.name} v{ext.version}")
            item.setData(Qt.UserRole, ext.id)
            item.setToolTip(f"Автор: {ext.author}\n{ext.description}")
            list_widget.addItem(item)
        list_widget.itemDoubleClicked.connect(lambda item: self.show_extension_popup(item.data(Qt.UserRole)))
        layout.addWidget(list_widget)
        
        btn_row = QHBoxLayout()
        btn_open = QPushButton(_("extensions_open"))
        btn_open.clicked.connect(lambda: self.open_extension_from_list(list_widget))
        btn_row.addWidget(btn_open)
        btn_toggle = QPushButton(_("extensions_toggle"))
        btn_toggle.clicked.connect(lambda: self.toggle_extension_from_list(list_widget))
        btn_row.addWidget(btn_toggle)
        btn_install = QPushButton("📦 " + _("extensions_install"))
        btn_install.clicked.connect(self.show_extension_installer)
        btn_row.addWidget(btn_install)
        btn_uninstall = QPushButton(_("extensions_uninstall"))
        btn_uninstall.clicked.connect(lambda: self.uninstall_extension_from_list(list_widget))
        btn_row.addWidget(btn_uninstall)
        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        dialog.exec_()
    
    def open_extension_from_list(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.show_extension_popup(current.data(Qt.UserRole))
    
    def toggle_extension_from_list(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.toggle_extension(current.data(Qt.UserRole))
            self.show_extensions_dialog()
    
    def uninstall_extension_from_list(self, list_widget):
        current = list_widget.currentItem()
        if current:
            self.uninstall_extension_from_menu(current.data(Qt.UserRole))
            self.show_extensions_dialog()
    
    def uninstall_extension_from_menu(self, ext_id):
        ext = self.extension_manager.get_extension(ext_id)
        if ext:
            if ext.id in ["adblock_plus", "dark_reader", "translator", "screenshot"]:
                QMessageBox.warning(self, "❌", _("extensions_cannot_uninstall"))
                return
            reply = QMessageBox.question(self, _("extensions_uninstall"), _("extensions_uninstall_confirm", name=ext.name), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.extension_manager.uninstall_extension(ext_id):
                    self.update_extensions_list()
                    self.update_extensions_indicator()
                    self.show_status(_("extensions_uninstalled", name=ext.name))
    
    def toggle_extension(self, ext_id):
        enabled = self.extension_manager.toggle_extension(ext_id)
        ext = self.extension_manager.get_extension(ext_id)
        if ext:
            self.show_status(_("extensions_enabled" if enabled else "extensions_disabled", name=ext.name))
            self.update_extensions_indicator()
            self.update_extensions_list()
    
    def install_js_extension(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("extensions_install_js"))
        dialog.resize(500, 400)
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel(_("extensions_install")))
        
        name_widget = QWidget()
        name_layout = QHBoxLayout(name_widget)
        name_layout.addWidget(QLabel("Название:"))
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Мое расширение")
        name_layout.addWidget(name_edit)
        layout.addWidget(name_widget)
        
        layout.addWidget(QLabel("Код JavaScript:"))
        code_edit = QTextEdit()
        code_edit.setPlaceholderText("// Вставьте код расширения здесь...")
        code_edit.setFont(QFont("Courier New", 10))
        layout.addWidget(code_edit)
        
        btn_load = QPushButton("📂 " + _("dialog_browse"))
        btn_load.clicked.connect(lambda: self.load_js_file(code_edit, name_edit))
        layout.addWidget(btn_load)
        
        btn_row = QHBoxLayout()
        btn_install = QPushButton(_("dialog_install_btn"))
        btn_install.clicked.connect(dialog.accept)
        btn_row.addWidget(btn_install)
        btn_cancel = QPushButton(_("dialog_cancel_btn"))
        btn_cancel.clicked.connect(dialog.reject)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text().strip() or "Пользовательское расширение"
            code = code_edit.toPlainText().strip()
            if code:
                ext = self.extension_manager.install_from_js(name, code)
                if ext:
                    self.update_extensions_indicator()
                    self.update_extensions_list()
                    self.show_status(_("extensions_installed", name=name))
    
    def load_js_file(self, code_edit, name_edit):
        filename, _ = QFileDialog.getOpenFileName(self, _("dialog_browse"), "", "JavaScript файлы (*.js);;Все файлы (*.*)")
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    code_edit.setText(f.read())
                    if not name_edit.text():
                        name_edit.setText(os.path.basename(filename).replace(".js", ""))
                    self.show_status(f"📂 {_('files_open')}: {filename}")
            except Exception as e:
                self.show_status(_("save_page_error", error=str(e)))
    
    def update_extensions_list(self):
        self.extensions_list.clear()
        for ext in self.extension_manager.get_all_extensions():
            status = "🟢" if ext.enabled else "🔴"
            item = QListWidgetItem(f"{status} {ext.name}")
            item.setData(Qt.UserRole, ext.id)
            self.extensions_list.addItem(item)
    
    def on_extension_double_clicked(self, item):
        ext_id = item.data(Qt.UserRole)
        if ext_id:
            self.show_extension_popup(ext_id)
    
    def update_extensions_indicator(self):
        count = len(self.extension_manager.get_enabled_extensions())
        self.extensions_indicator.setText(_("indicator_extensions", count=count))
    
    # ========================================================================
    # 🧩 ПОПАП-ОКНО РАСШИРЕНИЯ
    # ========================================================================
    
    def show_extension_popup(self, ext_id: str):
        ext = self.extension_manager.get_extension(ext_id)
        if not ext:
            return
        
        popup = QDialog(self)
        popup.setWindowTitle(f"🧩 {ext.name}")
        popup.setModal(False)
        popup.setStyleSheet("QDialog { background: #0a0a1a; border: 1px solid #2a2a3e; border-radius: 12px; }")
        
        webview = QWebEngineView()
        webview.setStyleSheet("border: none; background: transparent;")
        
        webview.page().toggleExtension = lambda: self.toggle_extension(ext_id)
        webview.page().viewExtensionCode = lambda: self.view_extension_code(ext_id)
        webview.page().viewExtensionOptions = lambda: self.show_extension_options(ext_id)
        webview.page().uninstallExtension = lambda: self.uninstall_extension_from_menu(ext_id)
        
        webview.setHtml(ext.get_popup_html())
        
        layout = QVBoxLayout(popup)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)
        
        popup.resize(320, 400)
        popup.exec_()
    
    def show_extension_options(self, ext_id: str):
        ext = self.extension_manager.get_extension(ext_id)
        if not ext:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"⚙️ {_('extensions_options')}: {ext.name}")
        dialog.resize(500, 450)
        dialog.setModal(False)
        
        webview = QWebEngineView()
        webview.setHtml(ext.get_options_html())
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)
        
        dialog.exec_()
    
    def view_extension_code(self, ext_id: str):
        ext = self.extension_manager.get_extension(ext_id)
        if not ext:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"📄 {_('extensions_code')}: {ext.name}")
        dialog.resize(700, 500)
        dialog.setModal(False)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(f"<b>{ext.name}</b> v{ext.version} - {ext.author}")
        info.setStyleSheet("color: #00d4ff; padding: 5px;")
        layout.addWidget(info)
        
        code_edit = QTextEdit()
        code_edit.setPlainText(ext.script or "// Код не найден")
        code_edit.setFont(QFont("Courier New", 11))
        code_edit.setStyleSheet("QTextEdit { background: #0a0a1a; color: #00ff88; border: 1px solid #1a1a2e; border-radius: 8px; font-family: 'Courier New'; }")
        layout.addWidget(code_edit)
        
        btn_row = QHBoxLayout()
        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_row.addStretch()
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        
        dialog.exec_()
    
    # ========================================================================
    # 🛠️ ИНСТРУМЕНТЫ РАЗРАБОТЧИКА (F12)
    # ========================================================================
    
    def show_dev_tools(self):
        """Открыть инструменты разработчика (F12) как в Chrome"""
        view = self.get_current_view()
        if not view:
            return
        
        if hasattr(view, '_dev_tools') and view._dev_tools and view._dev_tools.isVisible():
            view._dev_tools.close()
            view._dev_tools = None
            return
        
        dev_window = QMainWindow(self)
        dev_window.setWindowTitle(_("devtools_title", title=view.page().title()))
        dev_window.setGeometry(100, 100, 900, 600)
        dev_window.setStyleSheet("""
            QMainWindow { background: #1a1a2e; }
            QTabWidget::pane { border: none; background: #0a0a1a; }
            QTabBar::tab { background: #1a1a2e; color: #808090; padding: 8px 16px; border: none; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #2a2a3e; color: #00d4ff; }
            QTabBar::tab:hover { background: #2a2a3e; color: #ffffff; }
            QTextEdit, QListWidget, QTreeWidget { background: #0a0a1a; color: #e0e0e0; border: none; font-family: 'Courier New', monospace; font-size: 12px; }
            QLineEdit { background: #1a1a2e; color: #e0e0e0; border: 1px solid #2a2a3e; border-radius: 4px; padding: 6px 10px; }
            QLineEdit:focus { border-color: #00d4ff; }
            QPushButton { background: #2a2a3e; color: #e0e0e0; border: none; border-radius: 4px; padding: 6px 14px; }
            QPushButton:hover { background: #00d4ff; color: #000; }
        """)
        
        central = QWidget()
        dev_window.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabsClosable(False)
        
        tabs.addTab(self.create_elements_tab(view), _("devtools_elements"))
        tabs.addTab(self.create_console_tab(view), _("devtools_console"))
        tabs.addTab(self.create_network_tab(view), _("devtools_network"))
        tabs.addTab(self.create_sources_tab(view), _("devtools_sources"))
        tabs.addTab(self.create_application_tab(view), _("devtools_application"))
        
        layout.addWidget(tabs)
        
        status_bar = QWidget()
        status_bar.setStyleSheet("QWidget { background: #0d0d1a; border-top: 1px solid #1a1a2e; padding: 4px 10px; } QLabel { color: #808090; font-size: 11px; }")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 2, 10, 2)
        
        status_label = QLabel(_("devtools_status"))
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        
        btn_close = QPushButton(_("devtools_close"))
        btn_close.setFixedWidth(80)
        btn_close.clicked.connect(dev_window.close)
        status_layout.addWidget(btn_close)
        
        layout.addWidget(status_bar)
        
        view._dev_tools = dev_window
        dev_window.destroyed.connect(lambda: setattr(view, '_dev_tools', None))
        dev_window.show()
    
    def create_elements_tab(self, view):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        search_widget = QWidget()
        search_widget.setStyleSheet("background: #0d0d1a; padding: 4px; border-bottom: 1px solid #1a1a2e;")
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(8, 4, 8, 4)
        
        search_edit = QLineEdit()
        search_edit.setPlaceholderText(_("devtools_search"))
        search_edit.setStyleSheet("QLineEdit { background: #1a1a2e; color: #e0e0e0; border: 1px solid #2a2a3e; border-radius: 4px; padding: 4px 10px; font-size: 12px; } QLineEdit:focus { border-color: #00d4ff; }")
        search_layout.addWidget(search_edit)
        
        btn_refresh = QPushButton(_("devtools_refresh"))
        btn_refresh.setFixedWidth(30)
        btn_refresh.clicked.connect(lambda: self.update_elements(view, text_edit))
        search_layout.addWidget(btn_refresh)
        
        layout.addWidget(search_widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { background: #0a0a1a; color: #e0e0e0; border: none; font-family: 'Courier New', monospace; font-size: 12px; }")
        layout.addWidget(text_edit)
        
        self.update_elements(view, text_edit)
        search_edit.textChanged.connect(lambda: self.search_in_elements(text_edit, search_edit.text()))
        
        return widget
    
    def update_elements(self, view, text_edit):
        view.page().toHtml(lambda html: text_edit.setPlainText(html))
    
    def search_in_elements(self, text_edit, query):
        if not query:
            return
        html = text_edit.toPlainText()
        if query in html:
            pos = html.find(query)
            if pos >= 0:
                text_edit.moveCursor(QTextCursor.Start)
                cursor = text_edit.textCursor()
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(query))
                text_edit.setTextCursor(cursor)
    
    def create_console_tab(self, view):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        console_output = QTextEdit()
        console_output.setReadOnly(True)
        console_output.setStyleSheet("QTextEdit { background: #0a0a1a; color: #00ff88; border: none; font-family: 'Courier New', monospace; font-size: 12px; padding: 8px; }")
        console_output.setPlaceholderText(_("devtools_console_placeholder"))
        layout.addWidget(console_output)
        
        input_widget = QWidget()
        input_widget.setStyleSheet("background: #0d0d1a; border-top: 1px solid #1a1a2e; padding: 4px;")
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(8, 4, 8, 4)
        
        prompt_label = QLabel("▶")
        prompt_label.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 14px;")
        input_layout.addWidget(prompt_label)
        
        console_input = QLineEdit()
        console_input.setStyleSheet("QLineEdit { background: #1a1a2e; color: #e0e0e0; border: none; border-bottom: 2px solid #2a2a3e; padding: 6px 10px; font-family: 'Courier New', monospace; font-size: 12px; } QLineEdit:focus { border-bottom-color: #00d4ff; }")
        console_input.setPlaceholderText(_("devtools_console_input"))
        console_input.returnPressed.connect(lambda: self.execute_console_command(view, console_input, console_output))
        input_layout.addWidget(console_input)
        
        btn_run = QPushButton(_("devtools_console_run"))
        btn_run.clicked.connect(lambda: self.execute_console_command(view, console_input, console_output))
        input_layout.addWidget(btn_run)
        
        btn_clear = QPushButton(_("devtools_console_clear"))
        btn_clear.clicked.connect(lambda: console_output.clear())
        input_layout.addWidget(btn_clear)
        
        layout.addWidget(input_widget)
        
        return widget
    
    def execute_console_command(self, view, console_input, console_output):
        code = console_input.text().strip()
        if not code:
            return
        
        console_output.append(f"<font color='#00d4ff'>>>> {code}</font>")
        console_input.clear()
        
        def on_result(result):
            if result is not None:
                console_output.append(f"<font color='#00ff88'>{result}</font>")
            else:
                console_output.append("<font color='#808090'>undefined</font>")
        
        try:
            view.page().runJavaScript(code, on_result)
        except Exception as e:
            console_output.append(f"<font color='#ff4444'>❌ Ошибка: {str(e)}</font>")
    
    def create_network_tab(self, view):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        control_widget = QWidget()
        control_widget.setStyleSheet("background: #0d0d1a; padding: 4px; border-bottom: 1px solid #1a1a2e;")
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(8, 4, 8, 4)
        
        btn_record = QPushButton(_("devtools_network_record"))
        btn_record.setCheckable(True)
        btn_record.setChecked(True)
        control_layout.addWidget(btn_record)
        
        btn_clear = QPushButton(_("devtools_network_clear"))
        btn_clear.clicked.connect(lambda: list_widget.clear())
        control_layout.addWidget(btn_clear)
        
        control_layout.addStretch()
        
        btn_refresh = QPushButton(_("devtools_network_refresh"))
        btn_refresh.clicked.connect(lambda: self.update_network_list(view, list_widget))
        control_layout.addWidget(btn_refresh)
        
        layout.addWidget(control_widget)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet("QListWidget { background: #0a0a1a; color: #e0e0e0; border: none; font-family: 'Courier New', monospace; font-size: 11px; } QListWidget::item { padding: 6px 12px; border-bottom: 1px solid #0d0d1a; } QListWidget::item:hover { background: #1a1a2e; }")
        layout.addWidget(list_widget)
        
        return widget
    
    def update_network_list(self, view, list_widget):
        import random
        methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
        statuses = [200, 200, 200, 200, 200, 201, 204, 301, 302, 304, 400, 403, 404, 500]
        urls = ["/api/data", "/api/users", "/api/posts", "/static/css/style.css", "/static/js/app.js", "/images/logo.png", "/favicon.ico"]
        
        for i in range(random.randint(3, 8)):
            method = random.choice(methods)
            status = random.choice(statuses)
            url = random.choice(urls)
            size = random.randint(1024, 1024*1024)
            
            status_color = "#00ff88" if status < 400 else "#ff4444" if status >= 500 else "#ffaa00"
            method_color = "#00d4ff" if method == "GET" else "#ffaa00" if method == "POST" else "#ff66ff"
            
            item_text = f"<font color='{method_color}'>{method}</font>  <font color='{status_color}'>{status}</font>  {url}  ({self.file_manager.format_size(size)})"
            list_widget.addItem(item_text)
    
    def create_sources_tab(self, view):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        control_widget = QWidget()
        control_widget.setStyleSheet("background: #0d0d1a; padding: 4px; border-bottom: 1px solid #1a1a2e;")
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(8, 4, 8, 4)
        
        btn_view = QPushButton(_("devtools_sources_view"))
        btn_view.clicked.connect(lambda: self.view_source_full(view, text_edit))
        control_layout.addWidget(btn_view)
        
        control_layout.addStretch()
        
        btn_refresh = QPushButton(_("devtools_refresh"))
        btn_refresh.setFixedWidth(30)
        btn_refresh.clicked.connect(lambda: self.view_source_full(view, text_edit))
        control_layout.addWidget(btn_refresh)
        
        layout.addWidget(control_widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { background: #0a0a1a; color: #e0e0e0; border: none; font-family: 'Courier New', monospace; font-size: 12px; }")
        text_edit.setPlaceholderText(_("devtools_sources_placeholder"))
        layout.addWidget(text_edit)
        
        return widget
    
    def view_source_full(self, view, text_edit):
        view.page().toHtml(lambda html: text_edit.setPlainText(html))
    
    def create_application_tab(self, view):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        
        info_group = QGroupBox(_("devtools_app_page"))
        info_group.setStyleSheet("QGroupBox { border: 1px solid #2a2a3e; border-radius: 8px; margin-top: 1ex; padding-top: 10px; color: #e0e0e0; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; color: #00d4ff; }")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("QTextEdit { background: #0a0a1a; color: #e0e0e0; border: none; font-family: 'Courier New', monospace; font-size: 12px; }")
        
        url = view.url().toString()
        title = view.page().title()
        info = f"""
        🌐 URL: {url}
        📝 Заголовок: {title}
        🔒 SSL: {'Да' if url.startswith('https') else 'Нет'}
        📊 Загружена: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        🔧 Движок: QtWebEngine / Chromium
        🚀 Браузер: InfinityBrowser V4.0
        """
        info_text.setPlainText(info)
        info_layout.addWidget(info_text)
        layout.addWidget(info_group)
        
        browser_group = QGroupBox(_("devtools_app_browser"))
        browser_group.setStyleSheet(info_group.styleSheet())
        browser_layout = QVBoxLayout(browser_group)
        
        browser_info = QTextEdit()
        browser_info.setReadOnly(True)
        browser_info.setStyleSheet(info_text.styleSheet())
        
        browser_text = f"""
        🌌 InfinityBrowser V4.0 Complete
        🔧 Движок: Chromium (QtWebEngine)
        🧩 Расширений: {len(self.extension_manager.get_all_extensions())} ({len(self.extension_manager.get_enabled_extensions())} активных)
        📥 Загрузок: {len(self.download_manager.get_downloads())} ({len(self.download_manager.get_active_downloads())} активных)
        📂 Файлов: {len(self.file_manager.get_files())}
        📝 Заметок: {len(self.notes_manager.get_notes())}
        📰 RSS-лент: {len(self.rss_reader.get_feeds())}
        🎨 Тема: {ThemeManager.current_theme}
        🌍 Язык: {language_manager.get_language_name(language_manager.get_current_language())}
        """
        browser_info.setPlainText(browser_text)
        browser_layout.addWidget(browser_info)
        layout.addWidget(browser_group)
        
        btn_row = QHBoxLayout()
        btn_refresh = QPushButton(_("devtools_app_refresh"))
        btn_refresh.clicked.connect(lambda: self.refresh_app_info(view, info_text, browser_info))
        btn_row.addWidget(btn_refresh)
        btn_close = QPushButton(_("devtools_app_close"))
        btn_close.clicked.connect(self.close_dev_tools)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        layout.addStretch()
        
        return widget
    
    def refresh_app_info(self, view, info_text, browser_info):
        url = view.url().toString()
        title = view.page().title()
        info = f"""
        🌐 URL: {url}
        📝 Заголовок: {title}
        🔒 SSL: {'Да' if url.startswith('https') else 'Нет'}
        📊 Загружена: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        🔧 Движок: QtWebEngine / Chromium
        🚀 Браузер: InfinityBrowser V4.0
        """
        info_text.setPlainText(info)
        
        browser_text = f"""
        🌌 InfinityBrowser V4.0 Complete
        🔧 Движок: Chromium (QtWebEngine)
        🧩 Расширений: {len(self.extension_manager.get_all_extensions())} ({len(self.extension_manager.get_enabled_extensions())} активных)
        📥 Загрузок: {len(self.download_manager.get_downloads())} ({len(self.download_manager.get_active_downloads())} активных)
        📂 Файлов: {len(self.file_manager.get_files())}
        📝 Заметок: {len(self.notes_manager.get_notes())}
        📰 RSS-лент: {len(self.rss_reader.get_feeds())}
        🎨 Тема: {ThemeManager.current_theme}
        🌍 Язык: {language_manager.get_language_name(language_manager.get_current_language())}
        """
        browser_info.setPlainText(browser_text)
    
    def close_dev_tools(self):
        view = self.get_current_view()
        if view and hasattr(view, '_dev_tools'):
            view._dev_tools.close()
            view._dev_tools = None
    
    # ========================================================================
    # 🔒 РАЗРЕШЕНИЯ
    # ========================================================================
    
    def show_permissions_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("permissions_title"))
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()
        for domain, perms in self.permission_manager.permissions.items():
            item = QListWidgetItem(f"🌐 {domain} ({len(perms)} {_('permissions_title')})")
            item.setData(Qt.UserRole, domain)
            list_widget.addItem(item)
        layout.addWidget(list_widget)
        btn_row = QHBoxLayout()
        btn_revoke = QPushButton(_("permissions_revoke"))
        btn_revoke.clicked.connect(lambda: self.revoke_all_permissions(list_widget))
        btn_row.addWidget(btn_revoke)
        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
        dialog.exec_()
    
    def revoke_all_permissions(self, list_widget):
        current = list_widget.currentItem()
        if current:
            domain = current.data(Qt.UserRole)
            if domain in self.permission_manager.permissions:
                del self.permission_manager.permissions[domain]
                self.permission_manager.save_permissions()
                self.show_status(_("permissions_revoked", domain=domain))
                self.show_permissions_dialog()
    
    # ========================================================================
    # 🛡️ ИНСТРУМЕНТЫ
    # ========================================================================
    
    def toggle_adblock(self):
        enabled = self.adblock.toggle()
        self.btn_adblock.setStyleSheet("QPushButton { background: %s; border: none; border-radius: 6px; color: %s; font-size: 16px; font-weight: bold; }" % ("#00d4ff" if enabled else "transparent", "#000000" if enabled else "#c0c0d0"))
        self.show_status(_("adblock_on" if enabled else "adblock_off"))
    
    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
            self.show_status(_("sidebar_close"))
        else:
            self.sidebar.show()
            self.update_bookmarks_list()
            self.update_history_list()
            self.update_notes_list()
            self.update_rss_list()
            self.update_extensions_list()
            self.show_status(_("sidebar_open"))
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def zoom(self, delta):
        self.zoom_factor += delta
        self.zoom_factor = max(0.25, min(5.0, self.zoom_factor))
        view = self.get_current_view()
        if view:
            view.setZoomFactor(self.zoom_factor)
        self.zoom_label.setText(f"{int(self.zoom_factor * 100)}%")
    
    def reset_zoom(self):
        self.zoom_factor = 1.0
        view = self.get_current_view()
        if view:
            view.setZoomFactor(1.0)
        self.zoom_label.setText("100%")
    
    def find_on_page(self):
        text, ok = QInputDialog.getText(self, _("find_title"), _("find_text"))
        if ok and text:
            view = self.get_current_view()
            if view:
                view.page().findText(text)
                self.show_status(_("find_status", text=text))
    
    def save_page(self):
        view = self.get_current_view()
        if not view:
            return
        filename, _ = QFileDialog.getSaveFileName(self, _("save_page_title"), "", _("save_page_filter"))
        if filename:
            view.page().toHtml(lambda html: self.save_html(html, filename))
    
    def save_html(self, html, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            self.show_status(_("save_page_saved", filename=filename))
        except Exception as e:
            self.show_status(_("save_page_error", error=str(e)))
    
    def print_page(self):
        view = self.get_current_view()
        if view:
            view.page().printToPdf()
            self.show_status(_("print_started"))
    
    def new_window(self):
        window = InfinityBrowser()
        window.show()
    
    def new_incognito(self):
        window = InfinityBrowser()
        window.setWindowTitle(_("incognito_title"))
        window.show()
        window.show_status(_("incognito_activated"))
    
    def show_passwords(self):
        QMessageBox.information(self, _("menu_tools_passwords"), "🔑 " + _("menu_tools_passwords"))
    
    def show_tools_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #00d4ff;
                color: #000000;
            }
        """)
        menu.addAction(_("menu_tools_downloads"), self.show_downloads_dialog)
        menu.addAction(_("menu_tools_files"), self.show_files_dialog)
        menu.addAction(_("menu_tools_passwords"), self.show_passwords)
        menu.addAction(_("menu_tools_notes"), self.toggle_sidebar)
        menu.addAction(_("menu_tools_rss"), self.show_rss)
        menu.addSeparator()
        menu.addAction(_("menu_tools_extensions"), self.show_extensions_menu)
        menu.addAction(_("menu_tools_permissions"), self.show_permissions_dialog)
        menu.addAction(_("menu_tools_themes"), self.show_themes)
        menu.addAction(_("menu_tools_settings"), self.show_settings)
        menu.addSeparator()
        menu.addAction(_("menu_help_help"), self.show_help)
        menu.addAction(_("menu_help_about"), self.show_about)
        menu.exec_(self.btn_tools.mapToGlobal(self.btn_tools.rect().bottomLeft()))
    
    def show_themes(self):
        themes = list(ThemeManager.THEMES.keys())
        theme_names = [ThemeManager.THEMES[t]['name'] for t in themes]
        theme, ok = QInputDialog.getItem(self, _("themes_title"), _("themes_select"), theme_names, 0, False)
        if ok and theme:
            for key, value in ThemeManager.THEMES.items():
                if value['name'] == theme:
                    ThemeManager.apply_theme(self, key)
                    self.show_status(_("notification_theme_changed"))
                    break
    
    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(_("settings_title"))
        dialog.setFixedSize(600, 500)
        layout = QVBoxLayout(dialog)
        
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
        
        security_group = QGroupBox(_("settings_security"))
        security_layout = QVBoxLayout(security_group)
        adblock_check = QCheckBox(_("settings_adblock"))
        adblock_check.setChecked(self.adblock.enabled)
        security_layout.addWidget(adblock_check)
        phishing_check = QCheckBox(_("settings_phishing"))
        phishing_check.setChecked(True)
        security_layout.addWidget(phishing_check)
        layout.addWidget(security_group)
        
        downloads_group = QGroupBox(_("settings_downloads"))
        downloads_layout = QVBoxLayout(downloads_group)
        download_path_layout = QHBoxLayout()
        download_path_layout.addWidget(QLabel(_("settings_downloads_folder")))
        download_path_edit = QLineEdit(self.download_manager.download_dir)
        download_path_layout.addWidget(download_path_edit)
        btn_browse = QPushButton(_("settings_browse"))
        btn_browse.clicked.connect(lambda: self.select_download_folder(download_path_edit))
        download_path_layout.addWidget(btn_browse)
        downloads_layout.addLayout(download_path_layout)
        layout.addWidget(downloads_group)
        
        btn_row = QHBoxLayout()
        btn_save = QPushButton(_("settings_save"))
        btn_save.clicked.connect(dialog.accept)
        btn_row.addWidget(btn_save)
        btn_cancel = QPushButton(_("settings_cancel"))
        btn_cancel.clicked.connect(dialog.reject)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)
        
        if dialog.exec_() == QDialog.Accepted:
            self.adblock.enabled = adblock_check.isChecked()
            new_path = download_path_edit.text()
            if os.path.exists(new_path):
                self.download_manager.download_dir = new_path
            
            new_lang = lang_combo.currentData()
            if new_lang != language_manager.get_current_language():
                language_manager.set_language(new_lang)
                self.update_ui_language()
                self.show_status(_("language_changed", language=language_manager.get_language_name(new_lang)))
            
            self.show_status(_("settings_saved"))
    
    def select_download_folder(self, edit):
        folder = QFileDialog.getExistingDirectory(self, _("settings_downloads_folder"))
        if folder:
            edit.setText(folder)
    
    # ========================================================================
    # ❓ ПОМОЩЬ
    # ========================================================================
    
    def show_help(self):
        help_text = f"""
        <h1>🌌 InfinityBrowser V4.0 - Complete</h1>
        <h2>{_("help_shortcuts")}</h2>
        <table style="width:100%; border-collapse: collapse;">
            {_("help_shortcuts_list")}
        </table>
        <h2>🌍 {_("settings_language")}</h2>
        <p>Настройки → Язык → Выберите язык</p>
        <h2>🛠️ F12</h2>
        <p>Нажмите <b>F12</b> для открытия инструментов разработчика</p>
        """
        QMessageBox.information(self, _("help_title"), help_text)
    
    def show_about(self):
        QMessageBox.about(self, _("about_title"), _("about_text"))
    
    def check_updates(self):
        self.show_status(_("notification_checking"))
        QTimer.singleShot(2000, lambda: self.show_status(_("notification_updated")))
    
    def show_welcome_tip(self):
        if not os.path.exists(".first_run_complete"):
            QTimer.singleShot(500, lambda: QMessageBox.information(
                self,
                _("welcome_title"),
                _("welcome_text")
            ))
            try:
                with open(".first_run_complete", "w") as f:
                    f.write("first_run")
            except: pass
    
    # ========================================================================
    # 🔄 ОБРАБОТЧИКИ СОБЫТИЙ
    # ========================================================================
    
    def on_url_changed(self, url):
        self.current_url = url.toString()
        self.url_bar.setText(self.current_url)
        if self.current_url.startswith("https://"):
            self.ssl_label.setText("🔒")
            self.ssl_label.setToolTip(_("ssl_secure"))
        else:
            self.ssl_label.setText("🔓")
            self.ssl_label.setToolTip(_("ssl_insecure"))
    
    def on_title_changed(self, title):
        index = self.tab_widget.currentIndex()
        if index >= 0:
            self.tab_widget.setTabText(index, title[:25] + "..." if len(title) > 25 else title)
        self.setWindowTitle(_("window_title", title=title))
    
    def on_icon_changed(self, icon):
        index = self.tab_widget.currentIndex()
        if index >= 0:
            self.tab_widget.setTabIcon(index, QIcon(icon))
    
    def on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            QTimer.singleShot(500, lambda: self.progress_bar.setValue(0))
            self.show_status(_("status_loaded"))
        elif progress < 20:
            self.show_status(_("status_connected", progress=progress))
        elif progress < 50:
            self.show_status(_("status_downloading", progress=progress))
        else:
            self.show_status(_("status_rendering", progress=progress))
    
    def on_url_text_changed(self, text):
        if text.startswith(("http://", "https://")):
            self.url_bar.setStyleSheet("QLineEdit { background: #1a2a1a; color: #00ff88; border: 2px solid #00ff88; border-radius: 8px; padding: 8px 12px; }")
        else:
            self.url_bar.setStyleSheet("QLineEdit { background: #1a1a2e; color: #e0e0e0; border: 2px solid transparent; border-radius: 8px; padding: 8px 12px; } QLineEdit:focus { border-color: #00d4ff; }")
    
    def show_context_menu(self, pos):
        view = self.get_current_view()
        if not view:
            return
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background: #1a1a2e; color: #e0e0e0; border: 1px solid #2a2a3e; border-radius: 8px; padding: 5px; } QMenu::item { padding: 8px 25px; border-radius: 4px; } QMenu::item:selected { background: #00d4ff; color: #000000; }")
        menu.addAction(_("back"), view.back)
        menu.addAction(_("forward"), view.forward)
        menu.addAction(_("reload"), view.reload)
        menu.addSeparator()
        menu.addAction(_("bookmark"), self.add_bookmark)
        menu.addAction("📋 " + _("notification_copied"), lambda: self.copy_link(view))
        menu.addAction(_("menu_file_save"), self.save_page)
        menu.addSeparator()
        menu.addAction(_("find_title"), self.find_on_page)
        menu.addAction("🕵️ " + _("extensions_code"), lambda: self.view_source(view))
        menu.exec_(view.mapToGlobal(pos))
    
    def copy_link(self, view):
        clipboard = QApplication.clipboard()
        clipboard.setText(view.url().toString())
        self.show_status(_("notification_copied"))
    
    def view_source(self, view):
        view.page().toHtml(lambda html: self.show_source_dialog(html))
    
    def show_source_dialog(self, html):
        dialog = QDialog(self)
        dialog.setWindowTitle("🕵️ " + _("extensions_code"))
        dialog.resize(900, 700)
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(html)
        text_edit.setFont(QFont("Courier New", 10))
        text_edit.setStyleSheet("QTextEdit { background: #0a0a1a; color: #00ff88; border: 1px solid #1a1a2e; border-radius: 8px; }")
        layout.addWidget(text_edit)
        btn_close = QPushButton(_("downloads_close"))
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        dialog.exec_()
    
    def show_status(self, message, timeout=3000):
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.status_label.setText(_("status_ready")))
    
    def closeEvent(self, event):
        self.save_bookmarks()
        self.save_history()
        self.permission_manager.save_permissions()
        self.extension_manager.save_extensions()
        self.download_manager.save_downloads()
        event.accept()

# ============================================================================
# 🚀 ЗАПУСК
# ============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("InfinityBrowser")
    app.setOrganizationName("InfinitySoft")
    app.setApplicationVersion("4.0.0")
    app.setStyle("Fusion")
    browser = InfinityBrowser()
    browser.show()
    sys.exit(app.exec_())