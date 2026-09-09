"""
Боковая панель с виджетами:
- Закладки
- История
- Заметки
- RSS-лента
- Погода
- Калькулятор
"""

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QListWidget, QListWidgetItem,
    QLabel, QScrollArea, QFrame, QTreeWidget,
    QTreeWidgetItem, QLineEdit, QTextEdit, QComboBox,
    QSplitter, QToolButton, QMenu
)

class SidebarManager(QWidget):
    """Менеджер боковой панели"""
    
    # Сигналы
    tab_selected = pyqtSignal(int)
    url_selected = pyqtSignal(str)
    note_selected = pyqtSignal(dict)
    rss_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_tab = 0
        self.is_collapsed = False
        self.width_normal = 250
        self.width_collapsed = 40
        
        self.init_ui()
        self.load_widgets()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setFixedWidth(self.width_normal)
        self.setStyleSheet("""
            QWidget {
                background: #0d0d1a;
            }
            QPushButton {
                background: transparent;
                border: none;
                color: #808090;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #1a1a2e;
                color: #ffffff;
            }
            QPushButton:checked {
                background: #00d4ff;
                color: #000000;
            }
            QListWidget {
                background: transparent;
                border: none;
                color: #c0c0d0;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background: #1a1a2e;
            }
            QListWidget::item:selected {
                background: #00d4ff;
                color: #000000;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QLineEdit {
                background: #1a1a2e;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border-color: #00d4ff;
            }
            QLabel {
                color: #808090;
                padding: 5px;
            }
        """)
        
        # Главный лейаут
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Верхняя панель с кнопками
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(5, 5, 5, 5)
        
        # Кнопки переключения вкладок
        self.btn_bookmarks = self.create_tab_button("⭐", "Закладки", 0)
        self.btn_history = self.create_tab_button("⏳", "История", 1)
        self.btn_notes = self.create_tab_button("📝", "Заметки", 2)
        self.btn_rss = self.create_tab_button("📰", "RSS", 3)
        self.btn_tools = self.create_tab_button("🛠️", "Инструменты", 4)
        
        top_layout.addWidget(self.btn_bookmarks)
        top_layout.addWidget(self.btn_history)
        top_layout.addWidget(self.btn_notes)
        top_layout.addWidget(self.btn_rss)
        top_layout.addWidget(self.btn_tools)
        
        # Кнопка сворачивания
        self.btn_collapse = QPushButton("◀")
        self.btn_collapse.setFixedSize(30, 30)
        self.btn_collapse.clicked.connect(self.toggle_collapse)
        top_layout.addWidget(self.btn_collapse)
        
        layout.addWidget(top_widget)
        
        # Стек вкладок
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
    
    def create_tab_button(self, icon: str, tooltip: str, index: int) -> QPushButton:
        """Создание кнопки вкладки"""
        btn = QPushButton(icon)
        btn.setToolTip(tooltip)
        btn.setFixedSize(35, 35)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.switch_tab(index))
        
        if index == 0:
            btn.setChecked(True)
        
        return btn
    
    def load_widgets(self):
        """Загрузка виджетов для каждой вкладки"""
        # Закладки
        self.bookmarks_widget = self.create_bookmarks_widget()
        self.stack.addWidget(self.bookmarks_widget)
        
        # История
        self.history_widget = self.create_history_widget()
        self.stack.addWidget(self.history_widget)
        
        # Заметки
        self.notes_widget = self.create_notes_widget()
        self.stack.addWidget(self.notes_widget)
        
        # RSS
        self.rss_widget = self.create_rss_widget()
        self.stack.addWidget(self.rss_widget)
        
        # Инструменты
        self.tools_widget = self.create_tools_widget()
        self.stack.addWidget(self.tools_widget)
    
    def create_bookmarks_widget(self) -> QWidget:
        """Создание виджета закладок"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Поиск
        search = QLineEdit()
        search.setPlaceholderText("🔍 Поиск закладок...")
        search.textChanged.connect(self.search_bookmarks)
        layout.addWidget(search)
        
        # Список закладок
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.on_bookmark_clicked)
        layout.addWidget(self.bookmarks_list)
        
        # Кнопка добавления
        btn_add = QPushButton("➕ Добавить закладку")
        btn_add.clicked.connect(self.add_bookmark)
        layout.addWidget(btn_add)
        
        return widget
    
    def create_history_widget(self) -> QWidget:
        """Создание виджета истории"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Поиск
        search = QLineEdit()
        search.setPlaceholderText("🔍 Поиск в истории...")
        search.textChanged.connect(self.search_history)
        layout.addWidget(search)
        
        # Список истории
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_history_clicked)
        layout.addWidget(self.history_list)
        
        # Кнопки
        btn_row = QHBoxLayout()
        btn_clear = QPushButton("🗑️ Очистить")
        btn_clear.clicked.connect(self.clear_history)
        btn_row.addWidget(btn_clear)
        
        btn_export = QPushButton("📤 Экспорт")
        btn_export.clicked.connect(self.export_history)
        btn_row.addWidget(btn_export)
        
        layout.addLayout(btn_row)
        
        return widget
    
    def create_notes_widget(self) -> QWidget:
        """Создание виджета заметок"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Поиск
        search = QLineEdit()
        search.setPlaceholderText("🔍 Поиск заметок...")
        search.textChanged.connect(self.search_notes)
        layout.addWidget(search)
        
        # Список заметок
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.on_note_clicked)
        layout.addWidget(self.notes_list)
        
        # Кнопка добавления
        btn_add = QPushButton("➕ Новая заметка")
        btn_add.clicked.connect(self.add_note)
        layout.addWidget(btn_add)
        
        return widget
    
    def create_rss_widget(self) -> QWidget:
        """Создание виджета RSS"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Добавление RSS
        add_widget = QWidget()
        add_layout = QHBoxLayout(add_widget)
        
        self.rss_input = QLineEdit()
        self.rss_input.setPlaceholderText("Введите URL RSS...")
        add_layout.addWidget(self.rss_input)
        
        btn_add = QPushButton("➕")
        btn_add.setFixedWidth(30)
        btn_add.clicked.connect(self.add_rss_feed)
        add_layout.addWidget(btn_add)
        
        layout.addWidget(add_widget)
        
        # Список RSS
        self.rss_list = QListWidget()
        self.rss_list.itemClicked.connect(self.on_rss_clicked)
        layout.addWidget(self.rss_list)
        
        # Новости
        self.news_view = QTextEdit()
        self.news_view.setReadOnly(True)
        self.news_view.setStyleSheet("""
            QTextEdit {
                background: #1a1a2e;
                border: 1px solid #2a2a3e;
                border-radius: 8px;
                color: #c0c0d0;
            }
        """)
        layout.addWidget(self.news_view)
        
        return widget
    
    def create_tools_widget(self) -> QWidget:
        """Создание виджета инструментов"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Калькулятор
        calc_label = QLabel("🧮 Калькулятор")
        calc_label.setStyleSheet("font-weight: bold; color: #00d4ff;")
        layout.addWidget(calc_label)
        
        self.calc_display = QLineEdit()
        self.calc_display.setReadOnly(True)
        self.calc_display.setAlignment(Qt.AlignRight)
        layout.addWidget(self.calc_display)
        
        # Кнопки калькулятора
        calc_buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "←"]
        ]
        
        for row in calc_buttons:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFixedSize(45, 35)
                btn.clicked.connect(lambda checked, t=btn_text: self.calc_click(t))
                row_layout.addWidget(btn)
            layout.addWidget(row_widget)
        
        # Погода
        weather_label = QLabel("🌤️ Погода")
        weather_label.setStyleSheet("font-weight: bold; color: #00d4ff; margin-top: 10px;")
        layout.addWidget(weather_label)
        
        self.weather_display = QLabel("Загрузка...")
        self.weather_display.setStyleSheet("padding: 5px;")
        layout.addWidget(self.weather_display)
        
        # Кнопка обновления
        btn_refresh = QPushButton("🔄 Обновить погоду")
        btn_refresh.clicked.connect(self.update_weather)
        layout.addWidget(btn_refresh)
        
        layout.addStretch()
        
        return widget
    
    def switch_tab(self, index: int):
        """Переключение вкладки"""
        self.current_tab = index
        
        # Обновляем состояние кнопок
        buttons = [self.btn_bookmarks, self.btn_history, self.btn_notes, self.btn_rss, self.btn_tools]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)
        
        self.stack.setCurrentIndex(index)
        self.tab_selected.emit(index)
    
    def toggle_collapse(self):
        """Сворачивание/разворачивание панели"""
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            self.setFixedWidth(self.width_collapsed)
            self.btn_collapse.setText("▶")
            # Скрываем содержимое
            self.stack.setVisible(False)
        else:
            self.setFixedWidth(self.width_normal)
            self.btn_collapse.setText("◀")
            self.stack.setVisible(True)
    
    def on_bookmark_clicked(self, item: QListWidgetItem):
        """Обработка клика по закладке"""
        url = item.data(Qt.UserRole)
        if url:
            self.url_selected.emit(url)
    
    def on_history_clicked(self, item: QListWidgetItem):
        """Обработка клика по истории"""
        url = item.data(Qt.UserRole)
        if url:
            self.url_selected.emit(url)
    
    def on_note_clicked(self, item: QListWidgetItem):
        """Обработка клика по заметке"""
        note_data = item.data(Qt.UserRole)
        if note_data:
            self.note_selected.emit(note_data)
    
    def on_rss_clicked(self, item: QListWidgetItem):
        """Обработка клика по RSS"""
        url = item.data(Qt.UserRole)
        if url:
            self.rss_selected.emit(url)
    
    def search_bookmarks(self, text: str):
        """Поиск в закладках"""
        # Здесь код для поиска
        pass
    
    def search_history(self, text: str):
        """Поиск в истории"""
        pass
    
    def search_notes(self, text: str):
        """Поиск в заметках"""
        pass
    
    def add_bookmark(self):
        """Добавление закладки"""
        # Здесь код для добавления
        pass
    
    def add_note(self):
        """Добавление заметки"""
        # Здесь код для добавления
        pass
    
    def add_rss_feed(self):
        """Добавление RSS-ленты"""
        url = self.rss_input.text().strip()
        if url:
            # Добавляем RSS
            self.rss_input.clear()
    
    def clear_history(self):
        """Очистка истории"""
        pass
    
    def export_history(self):
        """Экспорт истории"""
        pass
    
    def update_weather(self):
        """Обновление погоды"""
        # Здесь код для получения погоды
        self.weather_display.setText("☀️ +25°C, Москва")
    
    def calc_click(self, value: str):
        """Обработка нажатия на калькуляторе"""
        if value == "=":
            try:
                result = eval(self.calc_display.text())
                self.calc_display.setText(str(result))
            except:
                self.calc_display.setText("Error")
        elif value == "C":
            self.calc_display.clear()
        elif value == "←":
            text = self.calc_display.text()
            self.calc_display.setText(text[:-1])
        else:
            self.calc_display.setText(self.calc_display.text() + value)