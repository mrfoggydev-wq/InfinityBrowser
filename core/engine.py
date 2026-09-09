"""
Ядро браузера:
- Управление WebEngine
- Обработка запросов
- Управление сессиями
- Кэширование
- История
- Закладки
- Cookie
- Печать
- Поиск на странице
- Скриншоты
- Масштабирование
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from PyQt5.QtCore import (
    Qt, QUrl, QObject, pyqtSignal, QTimer, 
    QByteArray, QBuffer, QIODevice
)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEnginePage, QWebEngineProfile,
    QWebEngineSettings, QWebEngineScript, QWebEngineScriptCollection
)
from PyQt5.QtWebEngineCore import (
    QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo,
    QWebEngineCookieStore, QWebEngineDownloadItem,
    QWebEngineNotification, QWebEngineQuotaRequest
)

class SuperWebPage(QWebEnginePage):
    """Расширенная веб-страница"""
    
    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)
        
        self.features = {
            "javascript": True,
            "images": True,
            "plugins": True,
            "webgl": True,
            "webaudio": True,
            "webgl2": True,
            "webassembly": True,
            "local_storage": True,
            "session_storage": True,
            "indexed_db": True,
            "cache": True,
            "cookies": True
        }
        
        self.request_handlers = []
        self.intercept_requests = False
        self.blocked_resources = []
        
        # Настройка страницы
        self.init_settings()
        
        # Подключение сигналов
        self.loadProgress.connect(self.on_load_progress)
        self.loadFinished.connect(self.on_load_finished)
        self.titleChanged.connect(self.on_title_changed)
        self.iconChanged.connect(self.on_icon_changed)
        self.urlChanged.connect(self.on_url_changed)
        self.windowCloseRequested.connect(self.on_window_close)
        self.fullScreenRequested.connect(self.on_fullscreen_requested)
        self.featurePermissionRequested.connect(self.on_feature_permission)
        self.authenticationRequired.connect(self.on_authentication_required)
        self.proxyAuthenticationRequired.connect(self.on_proxy_authentication)
        self.downloadRequested.connect(self.on_download_requested)
        self.newWindowRequested.connect(self.on_new_window)
        self.createWindow = self.create_window
    
    def init_settings(self):
        """Настройка параметров страницы"""
        settings = self.settings()
        
        # Основные настройки
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAudioEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.ViewportEnabled, True)
        settings.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGL2Enabled, True)
        settings.setAttribute(QWebEngineSettings.WebAssemblyEnabled, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        settings.setAttribute(QWebEngineSettings.ReadingFromCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.ForceDarkMode, False)
        settings.setAttribute(QWebEngineSettings.DefaultFixedFontSize, 16)
        settings.setAttribute(QWebEngineSettings.DefaultFontSize, 16)
    
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """Обработка сообщений JavaScript консоли"""
        if level == QWebEnginePage.ErrorMessageLevel:
            print(f"[JS ERROR] {source_id}:{line_number} - {message}")
        elif level == QWebEnginePage.WarningMessageLevel:
            print(f"[JS WARNING] {source_id}:{line_number} - {message}")
        elif level == QWebEnginePage.InfoMessageLevel:
            print(f"[JS INFO] {source_id}:{line_number} - {message}")
        else:
            print(f"[JS LOG] {source_id}:{line_number} - {message}")
    
    def on_load_progress(self, progress: int):
        """Прогресс загрузки"""
        self.parent().load_progress.emit(progress) if self.parent() else None
    
    def on_load_finished(self, ok: bool):
        """Загрузка завершена"""
        self.parent().load_finished.emit(ok) if self.parent() else None
    
    def on_title_changed(self, title: str):
        """Изменение заголовка"""
        self.parent().title_changed.emit(title) if self.parent() else None
    
    def on_icon_changed(self, icon_url: QUrl):
        """Изменение иконки"""
        self.parent().icon_changed.emit(icon_url) if self.parent() else None
    
    def on_url_changed(self, url: QUrl):
        """Изменение URL"""
        self.parent().url_changed.emit(url) if self.parent() else None
    
    def on_window_close(self):
        """Закрытие окна"""
        self.parent().window_close_requested.emit() if self.parent() else None
    
    def on_fullscreen_requested(self, request):
        """Запрос полноэкранного режима"""
        self.parent().fullscreen_requested.emit(request) if self.parent() else None
        request.accept()
    
    def on_feature_permission(self, url: QUrl, feature: QWebEnginePage.Feature):
        """Запрос разрешения на функцию"""
        # Автоматически разрешаем
        self.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
    
    def on_authentication_required(self, url: QUrl, authenticator):
        """Запрос аутентификации"""
        self.parent().authentication_required.emit(url, authenticator) if self.parent() else None
    
    def on_proxy_authentication(self, url: QUrl, authenticator, proxy_host: str):
        """Запрос аутентификации прокси"""
        self.parent().proxy_authentication_required.emit(url, authenticator, proxy_host) if self.parent() else None
    
    def on_download_requested(self, download: QWebEngineDownloadItem):
        """Запрос на скачивание"""
        self.parent().download_requested.emit(download) if self.parent() else None
    
    def on_new_window(self, request):
        """Создание нового окна"""
        self.parent().new_window_requested.emit(request.requestedUrl()) if self.parent() else None
        return self.create_window(QWebEnginePage.WebBrowserTab)
    
    def create_window(self, type: QWebEnginePage.WebWindowType):
        """Создание окна"""
        if type == QWebEnginePage.WebBrowserTab:
            # Создаем новую вкладку
            return None
        elif type == QWebEnginePage.WebBrowserWindow:
            # Создаем новое окно
            return None
        return None
    
    def inject_css(self, css: str):
        """Инъекция CSS в страницу"""
        script = f"""
        (function() {{
            var style = document.createElement('style');
            style.textContent = `{css}`;
            document.head.appendChild(style);
        }})();
        """
        self.runJavaScript(script)
    
    def inject_javascript(self, code: str):
        """Инъекция JavaScript в страницу"""
        self.runJavaScript(code)
    
    def execute_javascript_with_result(self, code: str, callback):
        """Выполнение JavaScript с получением результата"""
        self.runJavaScript(code, callback)
    
    def find_text(self, text: str, flags: int = 0) -> bool:
        """Поиск текста на странице"""
        return self.findText(text, flags)
    
    def stop_find(self):
        """Остановка поиска"""
        self.findText("", QWebEnginePage.FindFlags())
    
    def print_page(self):
        """Печать страницы"""
        self.printToPdf()
    
    def take_screenshot(self, format: str = "png") -> Optional[QByteArray]:
        """Скриншот страницы"""
        if not self.view():
            return None
        
        pixmap = self.view().grab()
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, format.upper())
        buffer.close()
        return buffer.data()
    
    def get_page_source(self, callback):
        """Получение исходного кода страницы"""
        self.toHtml(callback)
    
    def get_page_text(self, callback):
        """Получение текста страницы"""
        self.toPlainText(callback)
    
    def scroll_to(self, x: int, y: int):
        """Прокрутка страницы"""
        script = f"window.scrollTo({x}, {y});"
        self.runJavaScript(script)
    
    def scroll_by(self, dx: int, dy: int):
        """Прокрутка страницы на смещение"""
        script = f"window.scrollBy({dx}, {dy});"
        self.runJavaScript(script)
    
    def get_scroll_position(self, callback):
        """Получение позиции прокрутки"""
        script = "({x: window.scrollX, y: window.scrollY})"
        self.runJavaScript(script, callback)

class SuperEngine(QObject):
    """Главное ядро браузера"""
    
    # Сигналы
    load_progress = pyqtSignal(int)
    load_finished = pyqtSignal(bool)
    title_changed = pyqtSignal(str)
    icon_changed = pyqtSignal(QUrl)
    url_changed = pyqtSignal(QUrl)
    window_close_requested = pyqtSignal()
    fullscreen_requested = pyqtSignal(object)
    authentication_required = pyqtSignal(QUrl, object)
    proxy_authentication_required = pyqtSignal(QUrl, object, str)
    download_requested = pyqtSignal(QWebEngineDownloadItem)
    new_window_requested = pyqtSignal(QUrl)
    
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        self.profile = self.create_profile()
        self.current_page = None
        self.current_view = None
        self.history = []
        self.bookmarks = []
        self.sessions = {}
        self.current_session = None
        self.cache = {}
        
        # Загрузка данных
        self.load_history()
        self.load_bookmarks()
        self.load_sessions()
        
        # Cookie
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)
        self.cookie_store.cookieRemoved.connect(self.on_cookie_removed)
        self.cookie_store.cookieChanged.connect(self.on_cookie_changed)
        
        # Таймеры
        self.load_timer = QTimer()
        self.load_timer.setSingleShot(True)
        self.load_timer.timeout.connect(self.on_load_timeout)
        
        # Создаем начальную страницу
        self.create_view()
    
    def create_profile(self) -> QWebEngineProfile:
        """Создание профиля браузера"""
        profile = QWebEngineProfile("SuperProfile", self)
        
        # Пути для данных
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        profile.setPersistentStoragePath(os.path.join(data_dir, "profile"))
        profile.setCachePath(os.path.join(data_dir, "cache"))
        
        # Настройка кэша
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        profile.setHttpCacheMaximumSize(200 * 1024 * 1024)  # 200 MB
        
        # User-Agent
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "SuperBrowser/4.0.0 Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Cookies
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        profile.setHttpAcceptLanguage("ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
        
        # Загрузки
        profile.downloadRequested.connect(self.on_download_requested)
        
        return profile
    
    def create_view(self, parent=None) -> QWebEngineView:
        """Создание нового WebView"""
        view = QWebEngineView(parent)
        page = SuperWebPage(self.profile, view)
        
        # Подключаем сигналы страницы
        page.loadProgress.connect(self.load_progress.emit)
        page.loadFinished.connect(self.load_finished.emit)
        page.titleChanged.connect(self.title_changed.emit)
        page.iconChanged.connect(self.icon_changed.emit)
        page.urlChanged.connect(self.url_changed.emit)
        page.windowCloseRequested.connect(self.window_close_requested.emit)
        page.fullScreenRequested.connect(self.fullscreen_requested.emit)
        page.authenticationRequired.connect(self.authentication_required.emit)
        page.proxyAuthenticationRequired.connect(self.proxy_authentication_required.emit)
        page.downloadRequested.connect(self.download_requested.emit)
        page.newWindowRequested.connect(self.new_window_requested.emit)
        
        view.setPage(page)
        view.setZoomFactor(1.0)
        
        self.current_page = page
        self.current_view = view
        
        return view
    
    def navigate(self, url: str) -> bool:
        """Навигация по URL"""
        if not url:
            return False
        
        # Добавляем протокол если нужно
        if not url.startswith(("http://", "https://", "file://", "about:", "data:")):
            url = "https://" + url
        
        qurl = QUrl(url)
        if not qurl.isValid():
            return False
        
        # Добавляем в историю
        self.add_to_history(url)
        
        # Загружаем
        self.current_page.setUrl(qurl)
        self.load_timer.start(30000)  # 30 секунд таймаут
        
        return True
    
    def navigate_back(self):
        """Назад"""
        if self.current_page:
            self.current_page.triggerAction(QWebEnginePage.Back)
    
    def navigate_forward(self):
        """Вперед"""
        if self.current_page:
            self.current_page.triggerAction(QWebEnginePage.Forward)
    
    def reload(self):
        """Обновить"""
        if self.current_page:
            self.current_page.triggerAction(QWebEnginePage.Reload)
    
    def reload_force(self):
        """Принудительное обновление"""
        if self.current_page:
            self.current_page.triggerAction(QWebEnginePage.ReloadAndBypassCache)
    
    def stop(self):
        """Остановить загрузку"""
        if self.current_page:
            self.current_page.triggerAction(QWebEnginePage.Stop)
            self.load_timer.stop()
    
    def go_home(self):
        """Перейти на домашнюю страницу"""
        home = self.settings.value("home_page", "https://www.google.com")
        self.navigate(home)
    
    def add_to_history(self, url: str, title: str = ""):
        """Добавление в историю"""
        entry = {
            "url": url,
            "title": title or url,
            "timestamp": datetime.now().isoformat(),
            "visits": 1
        }
        
        # Проверка дубликатов
        for i, item in enumerate(self.history):
            if item["url"] == url:
                item["visits"] += 1
                item["timestamp"] = entry["timestamp"]
                item["title"] = title or item["title"]
                self.history.pop(i)
                break
        
        self.history.insert(0, entry)
        
        # Ограничение размера истории
        max_history = self.settings.value("max_history", 1000, type=int)
        if len(self.history) > max_history:
            self.history = self.history[:max_history]
        
        self.save_history()
    
    def get_history(self, limit: int = None, search: str = None) -> List[Dict]:
        """Получение истории"""
        history = self.history
        
        if search:
            search_lower = search.lower()
            history = [item for item in history 
                      if search_lower in item["url"].lower() or 
                         search_lower in item["title"].lower()]
        
        if limit:
            history = history[:limit]
        
        return history
    
    def clear_history(self):
        """Очистка истории"""
        self.history = []
        self.save_history()
    
    def save_history(self):
        """Сохранение истории"""
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")
    
    def load_history(self):
        """Загрузка истории"""
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
    
    def add_bookmark(self, url: str, title: str, folder: str = "Основные") -> bool:
        """Добавление закладки"""
        # Проверка дубликатов
        for bookmark in self.bookmarks:
            if bookmark["url"] == url:
                return False
        
        bookmark = {
            "url": url,
            "title": title or url,
            "folder": folder,
            "timestamp": datetime.now().isoformat()
        }
        
        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        return True
    
    def remove_bookmark(self, url: str) -> bool:
        """Удаление закладки"""
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark["url"] == url:
                del self.bookmarks[i]
                self.save_bookmarks()
                return True
        return False
    
    def get_bookmarks(self, folder: str = None) -> List[Dict]:
        """Получение закладок"""
        if folder:
            return [b for b in self.bookmarks if b.get("folder") == folder]
        return self.bookmarks
    
    def get_bookmark_folders(self) -> List[str]:
        """Получение папок закладок"""
        folders = set()
        for bookmark in self.bookmarks:
            folders.add(bookmark.get("folder", "Основные"))
        return sorted(list(folders))
    
    def save_bookmarks(self):
        """Сохранение закладок"""
        try:
            with open("bookmarks.json", "w", encoding="utf-8") as f:
                json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения закладок: {e}")
    
    def load_bookmarks(self):
        """Загрузка закладок"""
        try:
            with open("bookmarks.json", "r", encoding="utf-8") as f:
                self.bookmarks = json.load(f)
        except FileNotFoundError:
            self.bookmarks = []
        except Exception as e:
            print(f"Ошибка загрузки закладок: {e}")
    
    def is_bookmarked(self, url: str) -> bool:
        """Проверка, добавлена ли закладка"""
        for bookmark in self.bookmarks:
            if bookmark["url"] == url:
                return True
        return False
    
    def create_session(self, name: str = None) -> str:
        """Создание сессии"""
        session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        
        session = {
            "id": session_id,
            "name": name or f"Сессия {len(self.sessions) + 1}",
            "tabs": [],
            "created": datetime.now().isoformat()
        }
        
        # Сохраняем текущие вкладки
        # Здесь нужно получить все вкладки из TabManager
        session["tabs"] = self.get_current_tabs()
        
        self.sessions[session_id] = session
        self.current_session = session_id
        self.save_sessions()
        
        return session_id
    
    def get_current_tabs(self) -> List[Dict]:
        """Получение текущих вкладок"""
        # В реальном приложении здесь получаем данные из TabManager
        tabs = []
        if self.current_page:
            tabs.append({
                "url": self.current_page.url().toString(),
                "title": self.current_page.title(),
                "history": []
            })
        return tabs
    
    def load_session(self, session_id: str) -> bool:
        """Загрузка сессии"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        self.current_session = session_id
        
        # Загружаем вкладки
        for tab_data in session["tabs"]:
            # Открываем вкладку
            self.new_window_requested.emit(QUrl(tab_data["url"]))
        
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Удаление сессии"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
            return True
        return False
    
    def get_sessions(self) -> List[Dict]:
        """Получение списка сессий"""
        return list(self.sessions.values())
    
    def save_sessions(self):
        """Сохранение сессий"""
        try:
            with open("sessions.json", "w", encoding="utf-8") as f:
                json.dump(self.sessions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения сессий: {e}")
    
    def load_sessions(self):
        """Загрузка сессий"""
        try:
            with open("sessions.json", "r", encoding="utf-8") as f:
                self.sessions = json.load(f)
        except FileNotFoundError:
            self.sessions = {}
        except Exception as e:
            print(f"Ошибка загрузки сессий: {e}")
    
    def on_cookie_added(self, cookie):
        """Cookie добавлен"""
        pass
    
    def on_cookie_removed(self, cookie):
        """Cookie удален"""
        pass
    
    def on_cookie_changed(self, cookie):
        """Cookie изменен"""
        pass
    
    def on_download_requested(self, download: QWebEngineDownloadItem):
        """Запрос на скачивание"""
        self.download_requested.emit(download)
        download.accept()
    
    def on_load_timeout(self):
        """Таймаут загрузки"""
        if self.current_page:
            self.current_page.stop()
            print("Таймаут загрузки страницы")
    
    def set_zoom_factor(self, factor: float):
        """Установка масштаба"""
        if self.current_view:
            self.current_view.setZoomFactor(factor)
    
    def get_zoom_factor(self) -> float:
        """Получение масштаба"""
        if self.current_view:
            return self.current_view.zoomFactor()
        return 1.0
    
    def zoom_in(self):
        """Увеличить масштаб"""
        factor = self.get_zoom_factor() + 0.1
        self.set_zoom_factor(min(factor, 5.0))
    
    def zoom_out(self):
        """Уменьшить масштаб"""
        factor = self.get_zoom_factor() - 0.1
        self.set_zoom_factor(max(factor, 0.25))
    
    def zoom_reset(self):
        """Сброс масштаба"""
        self.set_zoom_factor(1.0)
    
    def find_text(self, text: str, flags: int = 0) -> bool:
        """Поиск текста"""
        if self.current_page:
            return self.current_page.find_text(text, flags)
        return False
    
    def find_next(self):
        """Поиск следующего совпадения"""
        if self.current_page:
            self.current_page.findText("", QWebEnginePage.FindNext)
    
    def find_previous(self):
        """Поиск предыдущего совпадения"""
        if self.current_page:
            self.current_page.findText("", QWebEnginePage.FindBackward)
    
    def stop_find(self):
        """Остановка поиска"""
        if self.current_page:
            self.current_page.stop_find()
    
    def print_page(self):
        """Печать страницы"""
        if self.current_page:
            self.current_page.print_page()
    
    def print_to_pdf(self, filepath: str):
        """Печать в PDF"""
        if self.current_page:
            self.current_page.printToPdf(filepath)
    
    def take_screenshot(self, format: str = "png") -> Optional[bytes]:
        """Скриншот страницы"""
        if self.current_page:
            data = self.current_page.take_screenshot(format)
            if data:
                return bytes(data)
        return None
    
    def take_screenshot_full(self, format: str = "png") -> Optional[bytes]:
        """Скриншот всей страницы"""
        if not self.current_page:
            return None
        
        # Получаем размер страницы
        script = """
        (function() {
            return {
                width: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight
            };
        })();
        """
        
        def on_size_result(result):
            if result:
                width = result.get("width", 0)
                height = result.get("height", 0)
                # Здесь нужно сделать скриншот всей страницы
                # Это сложнее, требует прокрутки и склейки
                pass
        
        self.current_page.runJavaScript(script, on_size_result)
        return None
    
    def get_page_source(self, callback):
        """Получение исходного кода страницы"""
        if self.current_page:
            self.current_page.get_page_source(callback)
    
    def get_page_text(self, callback):
        """Получение текста страницы"""
        if self.current_page:
            self.current_page.get_page_text(callback)
    
    def execute_javascript(self, code: str):
        """Выполнение JavaScript"""
        if self.current_page:
            self.current_page.inject_javascript(code)
    
    def execute_javascript_with_result(self, code: str, callback):
        """Выполнение JavaScript с результатом"""
        if self.current_page:
            self.current_page.execute_javascript_with_result(code, callback)
    
    def inject_css(self, css: str):
        """Инъекция CSS"""
        if self.current_page:
            self.current_page.inject_css(css)
    
    def get_cookies(self) -> List[Dict]:
        """Получение всех cookies"""
        cookies = []
        
        def on_cookies_loaded(cookie_list):
            for cookie in cookie_list:
                cookies.append({
                    "name": cookie.name(),
                    "value": cookie.value(),
                    "domain": cookie.domain(),
                    "path": cookie.path(),
                    "secure": cookie.isSecure(),
                    "http_only": cookie.isHttpOnly(),
                    "expires": cookie.expiryDate().toSecsSinceEpoch() if cookie.expiryDate() else None
                })
        
        self.cookie_store.getAllCookies(on_cookies_loaded)
        return cookies
    
    def delete_cookie(self, name: str, domain: str):
        """Удаление cookie"""
        self.cookie_store.deleteCookie(name, domain)
    
    def delete_all_cookies(self):
        """Удаление всех cookies"""
        self.cookie_store.deleteAllCookies()
    
    def clear_cache(self):
        """Очистка кэша"""
        self.profile.clearHttpCache()
        self.cache.clear()
    
    def clear_all_data(self):
        """Очистка всех данных"""
        self.clear_cache()
        self.delete_all_cookies()
        self.clear_history()
        self.profile.clearAllVisitedLinks()
    
    def get_profile(self) -> QWebEngineProfile:
        """Получение профиля"""
        return self.profile
    
    def get_current_page(self) -> Optional[QWebEnginePage]:
        """Получение текущей страницы"""
        return self.current_page
    
    def get_current_view(self) -> Optional[QWebEngineView]:
        """Получение текущего WebView"""
        return self.current_view
    
    def set_user_agent(self, user_agent: str):
        """Установка User-Agent"""
        self.profile.setHttpUserAgent(user_agent)
    
    def set_proxy(self, proxy_host: str, proxy_port: int):
        """Установка прокси"""
        # Здесь код для установки прокси
        pass
    
    def get_version(self) -> Dict:
        """Получение версии"""
        return {
            "engine": "Chromium",
            "version": "120.0.0.0",
            "profile": "SuperProfile"
        }
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        return {
            "history_count": len(self.history),
            "bookmarks_count": len(self.bookmarks),
            "sessions_count": len(self.sessions),
            "cache_size": self.get_cache_size()
        }
    
    def get_cache_size(self) -> int:
        """Получение размера кэша"""
        cache_path = self.profile.cachePath()
        if os.path.exists(cache_path):
            total = 0
            for root, dirs, files in os.walk(cache_path):
                for file in files:
                    filepath = os.path.join(root, file)
                    total += os.path.getsize(filepath)
            return total
        return 0
    
    def cleanup(self):
        """Очистка ресурсов"""
        self.stop()
        self.clear_cache()
        self.save_history()
        self.save_bookmarks()
        self.save_sessions()
        
        if self.current_page:
            self.current_page.deleteLater()
        if self.current_view:
            self.current_view.deleteLater()
        if self.profile:
            self.profile.deleteLater()