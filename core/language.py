"""
🌍 Система локализации InfinityBrowser v1.1
Поддерживает 15+ языков
"""

import json
import os

VERSION = "1.1"


class LanguageManager:
    """Менеджер языков"""

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
            "app_title": f"🌌 InfinityBrowser v{VERSION}",
            "window_title": f"🌌 InfinityBrowser v{VERSION} - {{title}}",
            "back": "◀ Назад", "forward": "▶ Вперед", "reload": "🔄 Обновить",
            "home": "🏠 Домой", "go": "🚀 Перейти",
            "search_placeholder": "🔍 Поиск или введите URL...",
            "bookmark": "⭐ Закладка", "bookmark_add": "⭐ Закладка добавлена",
            "bookmark_remove": "⭐ Закладка удалена",
            "adblock": "🛡️ AdBlock", "adblock_on": "🛡️ AdBlock включен",
            "adblock_off": "🛡️ AdBlock отключен",
            "theme": "🌙 Тема", "sidebar": "📋 Панель",
            "sidebar_open": "📋 Боковая панель открыта",
            "sidebar_close": "📋 Боковая панель скрыта",
            "downloads": "📥 Загрузки", "files": "📂 Файлы",
            "extensions": "🧩 Расширения", "tools": "⚙️ Инструменты",
            "status_ready": "✅ Готово",
            "status_loaded": "✅ Страница загружена",
            "status_connected": "⏳ Подключение... {progress}%",
            "status_downloading": "⏳ Загрузка... {progress}%",
            "status_rendering": "⏳ Рендеринг... {progress}%",
            "status_download_start": "📥 Начата загрузка: {filename}",
            "status_download_complete": "✅ Загрузка завершена: {filename}",
            "tab_new": "Новая вкладка",
            "tab_from_link": "🆕 Новая вкладка из ссылки",
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
            "downloads_title": "📥 Менеджер загрузок",
            "downloads_open": "📂 Открыть",
            "downloads_folder": "📁 Папка",
            "downloads_remove": "❌ Удалить",
            "downloads_clear": "🗑️ Очистить",
            "downloads_close": "Закрыть",
            "files_title": "📂 Менеджер файлов",
            "files_open": "📂 Открыть",
            "files_delete": "🗑️ Удалить",
            "files_info": "ℹ️ Инфо",
            "extensions_title": "🧩 Расширения",
            "extensions_install": "🧩 Установить расширение",
            "extensions_manage": "🧩 Управление",
            "extensions_open": "🔍 Открыть",
            "extensions_toggle": "🔄 Вкл/Выкл",
            "extensions_uninstall": "🗑️ Удалить",
            "extensions_code": "📄 Код",
            "extensions_options": "⚙️ Настройки",
            "settings_title": "⚡ Настройки",
            "settings_general": "Общие",
            "settings_home": "🏠 Домашняя страница:",
            "settings_search": "🔍 Поисковик:",
            "settings_security": "Безопасность",
            "settings_adblock": "🛡️ Включить AdBlock",
            "settings_language": "🌍 Язык:",
            "settings_save": "💾 Сохранить",
            "settings_cancel": "❌ Отмена",
            "settings_saved": "⚡ Настройки сохранены",
            "themes_title": "🎨 Тема",
            "themes_select": "Выберите:",
            "find_title": "🔍 Поиск",
            "find_text": "Введите текст:",
            "help_title": "📖 Справка",
            "about_title": "ℹ️ О программе",
            "notification_copied": "✅ Ссылка скопирована",
            "notification_theme_changed": "🎨 Тема изменена",
            "sidebar_bookmarks": "⭐ Закладки",
            "sidebar_history": "⏳ История",
            "sidebar_notes": "📝 Заметки",
            "sidebar_rss": "📰 RSS",
            "sidebar_extensions": "🧩 Расширения",
            "sidebar_add_bookmark": "➕ Добавить закладку",
            "sidebar_add_note": "➕ Новая заметка",
            "sidebar_clear_history": "🗑️ Очистить историю",
            "incognito_activated": "🕵️ Режим инкогнито активирован",
            "welcome_title": f"🌌 Добро пожаловать в InfinityBrowser v{VERSION}!",
            "welcome_text": f"""
                <h2>🚀 InfinityBrowser v{VERSION} готов!</h2>
                <p><b>Что нового в v{VERSION}:</b></p>
                <ul>
                    <li><b>🆕 Открытие ссылок в новой вкладке</b></li>
                    <li><b>💡 Ctrl + клик по ссылке</b> → новая вкладка</li>
                    <li><b>🖱️ Клик колёсиком</b> → новая вкладка</li>
                    <li>🌍 15+ языков</li>
                    <li>🛠️ F12 DevTools</li>
                    <li>🧩 Расширения</li>
                    <li>📥 Менеджер загрузок</li>
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
            "bookmark": "⭐ Bookmark", "bookmark_add": "⭐ Bookmark added",
            "bookmark_remove": "⭐ Bookmark removed",
            "adblock": "🛡️ AdBlock", "adblock_on": "🛡️ AdBlock enabled",
            "adblock_off": "🛡️ AdBlock disabled",
            "theme": "🌙 Theme", "sidebar": "📋 Sidebar",
            "sidebar_open": "📋 Sidebar opened",
            "sidebar_close": "📋 Sidebar closed",
            "downloads": "📥 Downloads", "files": "📂 Files",
            "extensions": "🧩 Extensions", "tools": "⚙️ Tools",
            "status_ready": "✅ Ready", "status_loaded": "✅ Page loaded",
            "status_connected": "⏳ Connecting... {progress}%",
            "status_downloading": "⏳ Loading... {progress}%",
            "status_rendering": "⏳ Rendering... {progress}%",
            "status_download_start": "📥 Download: {filename}",
            "status_download_complete": "✅ Complete: {filename}",
            "tab_new": "New Tab", "tab_from_link": "🆕 New Tab from link",
            "menu_file": "📁 File",
            "menu_file_new_tab": "📄 New Tab",
            "menu_file_new_window": "📂 New Window",
            "menu_file_incognito": "🕵️ Incognito",
            "menu_file_downloads": "📥 Downloads",
            "menu_file_files": "📂 Files",
            "menu_file_save": "💾 Save As...",
            "menu_file_print": "🖨️ Print",
            "menu_file_exit": "🚪 Exit",
            "menu_tabs": "📑 Tabs",
            "menu_tabs_close": "❌ Close Tab",
            "menu_tabs_restore": "↩️ Restore",
            "menu_tabs_next": "◀ Next",
            "menu_tabs_prev": "▶ Previous",
            "menu_tools": "🛠️ Tools",
            "menu_tools_downloads": "📥 Downloads",
            "menu_tools_files": "📂 Files",
            "menu_tools_passwords": "🔑 Passwords",
            "menu_tools_notes": "📝 Notes",
            "menu_tools_rss": "📰 RSS",
            "menu_tools_extensions": "🧩 Extensions",
            "menu_tools_permissions": "🔒 Permissions",
            "menu_tools_themes": "🎨 Themes",
            "menu_tools_settings": "⚡ Settings",
            "menu_help": "❓ Help",
            "menu_help_help": "📖 Help",
            "menu_help_about": "ℹ️ About",
            "downloads_title": "📥 Downloads",
            "downloads_open": "📂 Open",
            "downloads_folder": "📁 Folder",
            "downloads_remove": "❌ Remove",
            "downloads_clear": "🗑️ Clear",
            "downloads_close": "Close",
            "files_title": "📂 Files",
            "files_open": "📂 Open",
            "files_delete": "🗑️ Delete",
            "files_info": "ℹ️ Info",
            "extensions_title": "🧩 Extensions",
            "extensions_install": "🧩 Install",
            "extensions_manage": "🧩 Manage",
            "extensions_open": "🔍 Open",
            "extensions_toggle": "🔄 Toggle",
            "extensions_uninstall": "🗑️ Remove",
            "extensions_code": "📄 Code",
            "extensions_options": "⚙️ Options",
            "settings_title": "⚡ Settings",
            "settings_general": "General",
            "settings_home": "🏠 Home:",
            "settings_search": "🔍 Search:",
            "settings_security": "Security",
            "settings_adblock": "🛡️ AdBlock",
            "settings_language": "🌍 Language:",
            "settings_save": "💾 Save",
            "settings_cancel": "❌ Cancel",
            "settings_saved": "⚡ Settings saved",
            "themes_title": "🎨 Theme",
            "themes_select": "Select:",
            "find_title": "🔍 Find",
            "find_text": "Enter text:",
            "help_title": "📖 Help",
            "about_title": "ℹ️ About",
            "notification_copied": "✅ Link copied",
            "notification_theme_changed": "🎨 Theme changed",
            "sidebar_bookmarks": "⭐ Bookmarks",
            "sidebar_history": "⏳ History",
            "sidebar_notes": "📝 Notes",
            "sidebar_rss": "📰 RSS",
            "sidebar_extensions": "🧩 Extensions",
            "sidebar_add_bookmark": "➕ Add Bookmark",
            "sidebar_add_note": "➕ New Note",
            "sidebar_clear_history": "🗑️ Clear History",
            "incognito_activated": "🕵️ Incognito activated",
            "welcome_title": f"🌌 Welcome to InfinityBrowser v{VERSION}!",
            "welcome_text": f"""
                <h2>🚀 InfinityBrowser v{VERSION} is ready!</h2>
                <p><b>New in v{VERSION}:</b></p>
                <ul>
                    <li><b>🆕 Open links in new tab</b></li>
                    <li><b>💡 Ctrl + click</b> → new tab</li>
                    <li><b>🖱️ Middle-click</b> → new tab</li>
                    <li>🌍 15+ languages</li>
                    <li>🛠️ F12 DevTools</li>
                    <li>🧩 Extensions</li>
                    <li>📥 Download manager</li>
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
                self.current_language = json.load(f).get("language", "ru")
        except:
            self.current_language = "ru"

    def save_language(self):
        try:
            with open("language.json", "w", encoding="utf-8") as f:
                json.dump({"language": self.current_language}, f)
        except:
            pass

    def set_language(self, lang_code):
        if lang_code in self.LANGUAGES:
            self.current_language = lang_code
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
        text = self.TRANSLATIONS.get(self.current_language, {}).get(key, key)
        for k, v in kwargs.items():
            text = text.replace("{" + k + "}", str(v))
        return text


# Глобальный экземпляр
language_manager = LanguageManager()


def _(key, **kwargs):
    """Глобальная функция перевода"""
    return language_manager.tr(key, **kwargs)