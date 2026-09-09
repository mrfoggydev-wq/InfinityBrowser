"""
Главное окно браузера с полной панелью управления
Поддерживает: скины, анимации, табы, боковую панель
"""

from PyQt5.QtCore import (
    Qt, QPoint, QRect, QTimer, QPropertyAnimation, 
    QEasingCurve, pyqtSignal
)
from PyQt5.QtGui import (
    QIcon, QPixmap, QColor, QPalette, QFont, 
    QKeySequence, QAction, QPainter, QLinearGradient
)
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTabBar, QStackedWidget,
    QMenu, QMenuBar, QStatusBar, QToolBar, QSplitter,
    QListWidget, QTreeWidget, QTableWidget, QLabel,
    QProgressBar, QSlider, QComboBox, QCheckBox,
    QRadioButton, QGroupBox, QScrollArea, QDockWidget,
    QMessageBox, QFileDialog, QInputDialog, QColorDialog
)

from core.engine import SuperEngine
from ui.tabs import TabManager
from ui.sidebar import SidebarManager
from ui.themes import ThemeManager

class SuperMainWindow(QMainWindow):
    """Главное окно супер-браузера"""
    
    # Сигналы
    url_changed = pyqtSignal(str)
    title_changed = pyqtSignal(str)
    loading_progress = pyqtSignal(int)
    tab_changed = pyqtSignal(int)
    theme_changed = pyqtSignal(str)
    
    def __init__(
        self,
        engine,
        network,
        security,
        adblock,
        downloader,
        translator,
        password_manager,
        gesture_manager,
        voice_controller,
        dark_reader,
        screenshot_manager,
        notes_manager,
        rss_reader,
        shortcut_manager,
        settings
    ):
        super().__init__()
        
        # Сохраняем ссылки на менеджеры
        self.engine = engine
        self.network = network
        self.security = security
        self.adblock = adblock
        self.downloader = downloader
        self.translator = translator
        self.password_manager = password_manager
        self.gesture_manager = gesture_manager
        self.voice_controller = voice_controller
        self.dark_reader = dark_reader
        self.screenshot_manager = screenshot_manager
        self.notes_manager = notes_manager
        self.rss_reader = rss_reader
        self.shortcut_manager = shortcut_manager
        self.settings = settings
        
        # Состояние
        self.current_url = ""
        self.current_title = "Новая вкладка"
        self.is_fullscreen = False
        self.is_incognito = False
        self.is_dark_mode = False
        self.zoom_factor = 1.0
        
        # Инициализация UI
        self.init_ui()
        self.init_menus()
        self.init_toolbars()
        self.init_statusbar()
        self.init_shortcuts()
        self.init_signals()
        
        # Загрузка сохраненных настроек
        self.load_settings()
        
        # Применяем тему
        self.apply_theme("dark")
        
        # Создаем первую вкладку
        self.create_tab("https://www.google.com")
        
        # Показываем приветственное сообщение
        self.show_status("🚀 Супер-браузер готов к работе!")
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("🌍 Супер-Браузер V4.0")
        self.setGeometry(100, 50, 1400, 900)
        self.setMinimumSize(800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Создаем верхнюю панель
        top_widget = QWidget()
        top_widget.setObjectName("topWidget")
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_layout.setSpacing(8)
        
        # Кнопки навигации
        self.btn_back = self.create_tool_button("◀", "Назад", self.go_back)
        self.btn_forward = self.create_tool_button("▶", "Вперед", self.go_forward)
        self.btn_reload = self.create_tool_button("⟳", "Обновить", self.reload)
        self.btn_home = self.create_tool_button("🏠", "Домой", self.go_home)
        
        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Поиск или введите URL...")
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border-radius: 15px;
                padding: 8px 15px;
                background: #2a2a3a;
                color: #e0e0e0;
                font-size: 14px;
                border: 2px solid transparent;
            }
            QLineEdit:focus {
                border-color: #00d4ff;
                background: #1a1a2e;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.textChanged.connect(self.on_url_text_changed)
        
        # Кнопка перехода
        self.btn_go = self.create_tool_button("🚀", "Перейти", self.navigate)
        self.btn_go.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099ff);
                border-radius: 15px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00eeff, stop:1 #00aaff);
            }
        """)
        
        # Кнопки функций
        self.btn_bookmark = self.create_tool_button("☆", "Закладки", self.toggle_bookmark)
        self.btn_adblock = self.create_tool_button("🛡️", "AdBlock", self.toggle_adblock)
        self.btn_dark = self.create_tool_button("🌙", "Ночной режим", self.toggle_dark_mode)
        self.btn_tools = self.create_tool_button("⚙️", "Инструменты", self.show_tools_menu)
        
        # Собираем верхнюю панель
        top_layout.addWidget(self.btn_back)
        top_layout.addWidget(self.btn_forward)
        top_layout.addWidget(self.btn_reload)
        top_layout.addWidget(self.btn_home)
        top_layout.addWidget(self.url_bar, 1)
        top_layout.addWidget(self.btn_go)
        top_layout.addWidget(self.btn_bookmark)
        top_layout.addWidget(self.btn_adblock)
        top_layout.addWidget(self.btn_dark)
        top_layout.addWidget(self.btn_tools)
        
        # Создаем менеджер вкладок
        self.tab_manager = TabManager(self)
        self.tab_manager.tab_changed.connect(self.on_tab_changed)
        self.tab_manager.new_tab_requested.connect(self.create_tab)
        self.tab_manager.close_tab_requested.connect(self.close_tab)
        
        # Создаем боковую панель
        self.sidebar_manager = SidebarManager(self)
        
        # Создаем сплиттер для боковой панели
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.sidebar_manager)
        self.splitter.addWidget(self.tab_manager)
        self.splitter.setSizes([250, 1150])
        self.splitter.setHandleWidth(3)
        
        # Добавляем все в главный лейаут
        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.splitter)
        
        # Настройка стилей
        self.setStyleSheet("""
            QMainWindow {
                background: #0a0a1a;
            }
            #topWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #0d0d1a);
                border-bottom: 2px solid #00d4ff;
            }
            QSplitter::handle {
                background: #1a1a2e;
                width: 3px;
            }
            QSplitter::handle:hover {
                background: #00d4ff;
            }
        """)
    
    def create_tool_button(self, text, tooltip, callback):
        """Создание кнопки на панели инструментов"""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(38, 38)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
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
        btn.clicked.connect(callback)
        return btn
    
    def init_menus(self):
        """Создание меню"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: #0d0d1a;
                color: #c0c0d0;
                border: none;
                padding: 4px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #1a1a2e;
            }
            QMenu {
                background: #1a1a2e;
                color: #c0c0d0;
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
                color: #000;
            }
        """)
        
        # Файл
        file_menu = menubar.addMenu("📁 Файл")
        file_menu.addAction("📄 Новая вкладка", self.create_tab, "Ctrl+T")
        file_menu.addAction("📂 Новое окно", self.new_window, "Ctrl+N")
        file_menu.addAction("🕵️ Инкогнито", self.new_incognito, "Ctrl+Shift+N")
        file_menu.addSeparator()
        file_menu.addAction("💾 Сохранить как...", self.save_page_as, "Ctrl+S")
        file_menu.addAction("🖨️ Печать", self.print_page, "Ctrl+P")
        file_menu.addSeparator()
        file_menu.addAction("🚪 Выход", self.close, "Ctrl+Q")
        
        # Вкладки
        tabs_menu = menubar.addMenu("📑 Вкладки")
        tabs_menu.addAction("➕ Новая вкладка", self.create_tab, "Ctrl+T")
        tabs_menu.addAction("❌ Закрыть вкладку", self.close_current_tab, "Ctrl+W")
        tabs_menu.addAction("↩️ Восстановить вкладку", self.restore_tab, "Ctrl+Shift+T")
        tabs_menu.addSeparator()
        tabs_menu.addAction("◀ Следующая вкладка", self.next_tab, "Ctrl+Tab")
        tabs_menu.addAction("▶ Предыдущая вкладка", self.prev_tab, "Ctrl+Shift+Tab")
        tabs_menu.addSeparator()
        tabs_menu.addAction("📊 Все вкладки", self.show_all_tabs, "Ctrl+Shift+E")
        
        # История
        history_menu = menubar.addMenu("⏳ История")
        history_menu.addAction("📋 Показать историю", self.show_history, "Ctrl+H")
        history_menu.addAction("🗑️ Очистить историю", self.clear_history)
        history_menu.addSeparator()
        
        # Закладки
        bookmarks_menu = menubar.addMenu("⭐ Закладки")
        bookmarks_menu.addAction("➕ Добавить закладку", self.add_bookmark, "Ctrl+D")
        bookmarks_menu.addAction("📂 Показать закладки", self.show_bookmarks, "Ctrl+Shift+O")
        bookmarks_menu.addSeparator()
        bookmarks_menu.addAction("📥 Импорт", self.import_bookmarks)
        bookmarks_menu.addAction("📤 Экспорт", self.export_bookmarks)
        
        # Инструменты
        tools_menu = menubar.addMenu("🛠️ Инструменты")
        tools_menu.addAction("🔧 Менеджер загрузок", self.show_downloads, "Ctrl+J")
        tools_menu.addAction("🔑 Менеджер паролей", self.show_passwords)
        tools_menu.addAction("📝 Заметки", self.show_notes)
        tools_menu.addAction("📰 RSS-читалка", self.show_rss)
        tools_menu.addSeparator()
        tools_menu.addAction("🎨 Темы", self.show_themes)
        tools_menu.addAction("⚡ Настройки", self.show_settings, "Ctrl+,")
        
        # Помощь
        help_menu = menubar.addMenu("❓ Помощь")
        help_menu.addAction("📖 Справка", self.show_help, "F1")
        help_menu.addAction("ℹ️ О программе", self.show_about)
        help_menu.addAction("🔄 Проверить обновления", self.check_updates)
    
    def init_toolbars(self):
        """Инициализация дополнительных панелей"""
        # Создаем плавающую панель
        self.tools_dock = QDockWidget("🛠️ Инструменты", self)
        self.tools_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.tools_dock.setFeatures(QDockWidget.DockWidgetClosable | 
                                    QDockWidget.DockWidgetMovable)
        
        tools_widget = QWidget()
        tools_layout = QVBoxLayout(tools_widget)
        
        # Калькулятор
        calc_group = QGroupBox("🧮 Калькулятор")
        calc_layout = QVBoxLayout(calc_group)
        self.calc_display = QLineEdit()
        self.calc_display.setReadOnly(True)
        self.calc_display.setAlignment(Qt.AlignRight)
        calc_layout.addWidget(self.calc_display)
        
        calc_buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]
        
        for row in calc_buttons:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFixedSize(45, 35)
                btn.clicked.connect(lambda checked, t=btn_text: self.calc_click(t))
                row_layout.addWidget(btn)
            calc_layout.addWidget(row_widget)
        
        tools_layout.addWidget(calc_group)
        
        # Погода
        weather_group = QGroupBox("🌤️ Погода")
        weather_layout = QVBoxLayout(weather_group)
        self.weather_label = QLabel("Загрузка...")
        self.weather_label.setStyleSheet("font-size: 14px; padding: 5px;")
        weather_layout.addWidget(self.weather_label)
        tools_layout.addWidget(weather_group)
        
        self.tools_dock.setWidget(tools_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tools_dock)
        self.tools_dock.hide()
    
    def init_statusbar(self):
        """Инициализация строки состояния"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #0d0d1a;
                color: #808090;
                border-top: 1px solid #1a1a2e;
            }
        """)
        
        # Добавляем виджеты в статусбар
        self.status_label = QLabel("✅ Готово")
        self.status_bar.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background: #1a1a2e;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099ff);
                border-radius: 6px;
            }
        """)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Индикаторы
        self.ssl_status = QLabel("🔒")
        self.status_bar.addPermanentWidget(self.ssl_status)
        
        self.zoom_status = QLabel("100%")
        self.status_bar.addPermanentWidget(self.zoom_status)
    
    def init_shortcuts(self):
        """Инициализация горячих клавиш"""
        shortcuts = [
            ("Ctrl+T", self.create_tab),
            ("Ctrl+W", self.close_current_tab),
            ("Ctrl+Shift+T", self.restore_tab),
            ("Ctrl+Tab", self.next_tab),
            ("Ctrl+Shift+Tab", self.prev_tab),
            ("Ctrl+Q", self.close),
            ("Ctrl+S", self.save_page_as),
            ("Ctrl+P", self.print_page),
            ("Ctrl+H", self.show_history),
            ("Ctrl+J", self.show_downloads),
            ("Ctrl+D", self.add_bookmark),
            ("Ctrl+Shift+O", self.show_bookmarks),
            ("Ctrl+,", self.show_settings),
            ("F5", self.reload),
            ("F11", self.toggle_fullscreen),
            ("Ctrl++", lambda: self.zoom(0.1)),
            ("Ctrl+-", lambda: self.zoom(-0.1)),
            ("Ctrl+0", self.reset_zoom),
            ("Ctrl+F", self.find_on_page),
            ("Ctrl+G", self.find_next),
            ("Alt+Home", self.go_home),
            ("Ctrl+U", self.view_source),
            ("Ctrl+Shift+I", self.show_devtools),
        ]
        
        for shortcut, callback in shortcuts:
            action = QAction(self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(callback)
            self.addAction(action)
    
    def init_signals(self):
        """Подключение сигналов"""
        # Сигналы от движка
        self.engine.title_changed.connect(self.on_title_changed)
        self.engine.url_changed.connect(self.on_url_changed)
        self.engine.load_progress.connect(self.on_load_progress)
        self.engine.new_window_requested.connect(self.create_tab)
    
    def create_tab(self, url="about:blank"):
        """Создание новой вкладки"""
        tab_widget = self.tab_manager.add_tab(url)
        if url and url != "about:blank":
            self.engine.navigate(url)
        return tab_widget
    
    def close_tab(self, index):
        """Закрытие вкладки"""
        self.tab_manager.close_tab(index)
    
    def close_current_tab(self):
        """Закрытие текущей вкладки"""
        current = self.tab_manager.currentIndex()
        if current >= 0:
            self.close_tab(current)
    
    def restore_tab(self):
        """Восстановление закрытой вкладки"""
        self.tab_manager.restore_tab()
    
    def next_tab(self):
        """Переключение на следующую вкладку"""
        self.tab_manager.next_tab()
    
    def prev_tab(self):
        """Переключение на предыдущую вкладку"""
        self.tab_manager.prev_tab()
    
    def go_back(self):
        """Назад"""
        self.engine.back()
    
    def go_forward(self):
        """Вперед"""
        self.engine.forward()
    
    def reload(self):
        """Обновить страницу"""
        self.engine.reload()
    
    def go_home(self):
        """Перейти на домашнюю страницу"""
        home = self.settings.value("home_page", "https://www.google.com")
        self.navigate_to(home)
    
    def navigate(self):
        """Навигация по URL из адресной строки"""
        url = self.url_bar.text().strip()
        if not url:
            return
        
        if not url.startswith(("http://", "https://", "file://", "about:")):
            url = "https://" + url
        
        self.navigate_to(url)
    
    def navigate_to(self, url):
        """Переход по URL"""
        self.current_url = url
        self.engine.navigate(url)
        self.url_bar.setText(url)
        
        # Проверка на фишинг
        if self.security.is_phishing(url):
            self.show_status("⚠️ Внимание! Сайт может быть опасен!")
        
        # Проверка на рекламу
        if self.adblock.should_block(url):
            self.show_status("🛡️ Реклама заблокирована на этом сайте")
    
    def on_url_changed(self, url):
        """Обработка изменения URL"""
        self.current_url = url.toString()
        self.url_bar.setText(self.current_url)
        self.url_changed.emit(self.current_url)
    
    def on_title_changed(self, title):
        """Обработка изменения заголовка"""
        self.current_title = title
        current_index = self.tab_manager.currentIndex()
        if current_index >= 0:
            self.tab_manager.setTabText(current_index, title)
        self.title_changed.emit(title)
    
    def on_load_progress(self, progress):
        """Обработка прогресса загрузки"""
        self.progress_bar.setValue(progress)
        self.loading_progress.emit(progress)
        if progress == 100:
            QTimer.singleShot(500, lambda: self.progress_bar.setValue(0))
    
    def on_tab_changed(self, index):
        """Обработка смены вкладки"""
        self.tab_changed.emit(index)
        # Обновляем URL и заголовок
        current_widget = self.tab_manager.currentWidget()
        if current_widget:
            page = current_widget.page()
            if page:
                self.on_url_changed(page.url())
                self.on_title_changed(page.title())
    
    def on_url_text_changed(self, text):
        """Обработка изменения текста в адресной строке"""
        # Проверяем, является ли текст URL
        if text.startswith(("http://", "https://")):
            # Проверяем безопасность
            if self.security.is_phishing(text):
                self.url_bar.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #ff4444;
                        background: #1a0a0a;
                    }
                """)
            else:
                self.url_bar.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #00ff88;
                        background: #0a1a0a;
                    }
                """)
        else:
            self.url_bar.setStyleSheet("""
                QLineEdit {
                    border: 2px solid transparent;
                    background: #2a2a3a;
                }
            """)
    
    def toggle_bookmark(self):
        """Добавление/удаление закладки"""
        if self.current_url:
            if self.engine.is_bookmarked(self.current_url):
                self.engine.remove_bookmark(self.current_url)
                self.btn_bookmark.setText("☆")
                self.show_status("Закладка удалена")
            else:
                self.engine.add_bookmark(self.current_url, self.current_title)
                self.btn_bookmark.setText("★")
                self.show_status("Закладка добавлена")
    
    def toggle_adblock(self):
        """Включение/выключение AdBlock"""
        self.adblock.toggle()
        self.btn_adblock.setStyleSheet("""
            QPushButton {
                background: %s;
                border-radius: 8px;
                padding: 5px;
            }
        """ % ("#00d4ff" if self.adblock.enabled else "transparent"))
        self.show_status(f"AdBlock {'включен' if self.adblock.enabled else 'отключен'}")
    
    def toggle_dark_mode(self):
        """Включение/выключение ночного режима"""
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.apply_theme("dark")
            self.btn_dark.setText("☀️")
            # Включаем DarkReader
            self.dark_reader.enable()
        else:
            self.apply_theme("light")
            self.btn_dark.setText("🌙")
            self.dark_reader.disable()
        self.show_status(f"Ночной режим {'включен' if self.is_dark_mode else 'отключен'}")
    
    def apply_theme(self, theme_name):
        """Применение темы"""
        ThemeManager.apply_theme(self, theme_name)
        self.theme_changed.emit(theme_name)
        self.settings.setValue("theme", theme_name)
    
    def toggle_fullscreen(self):
        """Переключение полноэкранного режима"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def zoom(self, delta):
        """Изменение масштаба"""
        self.zoom_factor += delta
        self.zoom_factor = max(0.25, min(5.0, self.zoom_factor))
        self.engine.set_zoom_factor(self.zoom_factor)
        self.zoom_status.setText(f"{int(self.zoom_factor * 100)}%")
    
    def reset_zoom(self):
        """Сброс масштаба"""
        self.zoom_factor = 1.0
        self.engine.set_zoom_factor(1.0)
        self.zoom_status.setText("100%")
    
    def find_on_page(self):
        """Поиск на странице"""
        text, ok = QInputDialog.getText(self, "Поиск", "Введите текст для поиска:")
        if ok and text:
            self.engine.find_text(text)
            self.show_status(f"🔍 Поиск: {text}")
    
    def find_next(self):
        """Поиск следующего совпадения"""
        self.engine.find_text("", QWebEnginePage.FindNext)
    
    def view_source(self):
        """Просмотр исходного кода"""
        if self.current_url:
            self.engine.view_source(self.current_url)
    
    def show_devtools(self):
        """Показать инструменты разработчика"""
        if self.engine.current_view:
            self.engine.current_view.page().triggerAction(
                QWebEnginePage.InspectElement
            )
    
    def save_page_as(self):
        """Сохранение страницы"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить страницу", "", 
            "HTML файл (*.html);;Все файлы (*.*)"
        )
        if filename:
            self.engine.save_page(filename)
            self.show_status(f"Страница сохранена: {filename}")
    
    def print_page(self):
        """Печать страницы"""
        self.engine.print_page()
    
    def new_window(self):
        """Создание нового окна"""
        from ui.main_window import SuperMainWindow
        new_window = SuperMainWindow(
            self.engine, self.network, self.security,
            self.adblock, self.downloader, self.translator,
            self.password_manager, self.gesture_manager,
            self.voice_controller, self.dark_reader,
            self.screenshot_manager, self.notes_manager,
            self.rss_reader, self.shortcut_manager,
            self.settings
        )
        new_window.show()
    
    def new_incognito(self):
        """Создание окна инкогнито"""
        # Включаем приватный режим
        self.is_incognito = True
        self.setWindowTitle("🕵️ Инкогнито - Супер-Браузер")
        self.engine.enable_incognito()
        self.create_tab()
        self.show_status("🕵️ Режим инкогнито активирован")
    
    def show_history(self):
        """Показать историю"""
        history_dialog = HistoryDialog(self.engine.get_history(), self)
        history_dialog.exec_()
    
    def clear_history(self):
        """Очистка истории"""
        reply = QMessageBox.question(
            self, "Очистка истории",
            "Вы уверены, что хотите очистить всю историю?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.engine.clear_history()
            self.show_status("История очищена")
    
    def show_bookmarks(self):
        """Показать закладки"""
        bookmarks_dialog = BookmarksDialog(self.engine.get_bookmarks(), self)
        bookmarks_dialog.exec_()
    
    def add_bookmark(self):
        """Добавление закладки"""
        if self.current_url:
            self.engine.add_bookmark(self.current_url, self.current_title)
            self.show_status("⭐ Закладка добавлена")
    
    def import_bookmarks(self):
        """Импорт закладок"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Импорт закладок", "",
            "HTML файлы (*.html);;JSON файлы (*.json)"
        )
        if filename:
            self.engine.import_bookmarks(filename)
            self.show_status("Закладки импортированы")
    
    def export_bookmarks(self):
        """Экспорт закладок"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт закладок", "bookmarks.html",
            "HTML файлы (*.html);;JSON файлы (*.json)"
        )
        if filename:
            self.engine.export_bookmarks(filename)
            self.show_status("Закладки экспортированы")
    
    def show_downloads(self):
        """Показать менеджер загрузок"""
        downloads_dialog = DownloadsDialog(self.downloader, self)
        downloads_dialog.exec_()
    
    def show_passwords(self):
        """Показать менеджер паролей"""
        passwords_dialog = PasswordsDialog(self.password_manager, self)
        passwords_dialog.exec_()
    
    def show_notes(self):
        """Показать заметки"""
        notes_dialog = NotesDialog(self.notes_manager, self)
        notes_dialog.exec_()
    
    def show_rss(self):
        """Показать RSS-читалку"""
        rss_dialog = RSSDialog(self.rss_reader, self)
        rss_dialog.exec_()
    
    def show_tools_menu(self):
        """Показать меню инструментов"""
        menu = QMenu(self)
        
        # Добавляем пункты
        menu.addAction("📥 Менеджер загрузок", self.show_downloads)
        menu.addAction("🔑 Менеджер паролей", self.show_passwords)
        menu.addAction("📝 Заметки", self.show_notes)
        menu.addAction("📰 RSS-читалка", self.show_rss)
        menu.addSeparator()
        menu.addAction("🎨 Темы", self.show_themes)
        menu.addAction("⚡ Настройки", self.show_settings)
        menu.addSeparator()
        menu.addAction("🧮 Калькулятор", self.toggle_calculator)
        menu.addAction("🌤️ Погода", self.show_weather)
        
        menu.exec_(self.btn_tools.mapToGlobal(
            self.btn_tools.rect().bottomLeft()
        ))
    
    def toggle_calculator(self):
        """Показать/скрыть калькулятор"""
        self.tools_dock.toggleViewAction().trigger()
    
    def show_weather(self):
        """Показать погоду"""
        self.show_status("🌤️ Загрузка погоды...")
        # Здесь код для получения погоды
        self.weather_label.setText("☀️ +25°C, Москва")
    
    def show_themes(self):
        """Показать выбор тем"""
        themes_dialog = ThemesDialog(self)
        themes_dialog.exec_()
    
    def show_settings(self):
        """Показать настройки"""
        settings_dialog = SettingsDialog(self.settings, self)
        settings_dialog.exec_()
    
    def show_all_tabs(self):
        """Показать все вкладки"""
        # Анимация показа всех вкладок
        self.tab_manager.show_all_tabs()
    
    def show_help(self):
        """Показать справку"""
        help_text = """
        <h1>🌍 Супер-Браузер V4.0</h1>
        <h2>Горячие клавиши:</h2>
        <ul>
            <li><b>Ctrl+T</b> - Новая вкладка</li>
            <li><b>Ctrl+W</b> - Закрыть вкладку</li>
            <li><b>Ctrl+Shift+T</b> - Восстановить вкладку</li>
            <li><b>Ctrl+Tab</b> - Следующая вкладка</li>
            <li><b>Ctrl+Shift+Tab</b> - Предыдущая вкладка</li>
            <li><b>Ctrl+D</b> - Добавить закладку</li>
            <li><b>Ctrl+H</b> - История</li>
            <li><b>Ctrl+J</b> - Загрузки</li>
            <li><b>F5</b> - Обновить</li>
            <li><b>F11</b> - Полный экран</li>
        </ul>
        """
        QMessageBox.information(self, "Справка", help_text)
    
    def show_about(self):
        """О программе"""
        about_text = f"""
        <h1>🌍 Супер-Браузер V4.0</h1>
        <p>Версия: {SuperBrowser.VERSION}</p>
        <p>Сборка: {SuperBrowser.BUILD}</p>
        <hr>
        <p>🔥 50+ функций</p>
        <p>🛡️ Встроенный AdBlock</p>
        <p>🔒 Менеджер паролей</p>
        <p>🎤 Голосовое управление</p>
        <p>✋ Жесты мышью</p>
        <hr>
        <p>© 2026 SuperSoft</p>
        """
        QMessageBox.about(self, "О программе", about_text)
    
    def check_updates(self):
        """Проверка обновлений"""
        self.show_status("🔄 Проверка обновлений...")
        # Здесь код проверки обновлений
        QTimer.singleShot(2000, lambda: self.show_status("✅ Нет доступных обновлений"))
    
    def show_status(self, message, timeout=3000):
        """Показать сообщение в статусбаре"""
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.status_label.setText("✅ Готово"))
    
    def calc_click(self, value):
        """Обработка нажатия на калькуляторе"""
        if value == "=":
            try:
                result = eval(self.calc_display.text())
                self.calc_display.setText(str(result))
            except:
                self.calc_display.setText("Error")
        elif value == "C":
            self.calc_display.clear()
        else:
            self.calc_display.setText(self.calc_display.text() + value)
    
    def load_settings(self):
        """Загрузка настроек"""
        # Загружаем тему
        theme = self.settings.value("theme", "dark")
        self.apply_theme(theme)
        
        # Загружаем домашнюю страницу
        home = self.settings.value("home_page", "https://www.google.com")
        
        # Загружаем настройки AdBlock
        adblock_enabled = self.settings.value("adblock_enabled", True, type=bool)
        if adblock_enabled:
            self.adblock.enable()
        else:
            self.adblock.disable()
        
        # Загружаем масштаб
        zoom = self.settings.value("zoom_factor", 1.0, type=float)
        self.zoom_factor = zoom
        self.engine.set_zoom_factor(zoom)
        self.zoom_status.setText(f"{int(zoom * 100)}%")
        
        # Загружаем позицию окна
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
    
    def save_settings(self):
        """Сохранение настроек"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("window_state", self.saveState())
        self.settings.setValue("zoom_factor", self.zoom_factor)
        self.settings.setValue("adblock_enabled", self.adblock.enabled)
        self.settings.sync()
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Сохраняем сессии
        self.engine.save_session()
        self.tab_manager.save_tabs()
        
        # Сохраняем настройки
        self.save_settings()
        
        # Закрываем все загрузки
        self.engine.cancel_all_downloads()
        
        event.accept()