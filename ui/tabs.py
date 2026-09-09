"""
Модуль управления вкладками с превью, анимациями и группировкой
"""

from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (
    QTabWidget, QTabBar, QWidget, QVBoxLayout,
    QPushButton, QLabel, QMenu, QAction, QHBoxLayout,
    QScrollArea, QGridLayout, QFrame, QApplication
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class TabBar(QTabBar):
    """Кастомная панель вкладок с кнопками и превью"""
    
    close_requested = pyqtSignal(int)
    duplicate_requested = pyqtSignal(int)
    pin_requested = pyqtSignal(int)
    mute_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_requested.emit)
        self.setStyleSheet("""
            QTabBar::tab {
                background: #1a1a2e;
                color: #808090;
                padding: 8px 15px;
                margin: 2px 2px 0 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: none;
                min-width: 80px;
                max-width: 200px;
            }
            QTabBar::tab:selected {
                background: #2a2a3e;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background: #2a2a3e;
                color: #ffffff;
            }
            QTabBar::close-button {
                image: none;
                background: transparent;
                color: #808090;
                padding: 2px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::close-button:hover {
                background: #ff4444;
                color: white;
            }
        """)
    
    def contextMenuEvent(self, event):
        """Контекстное меню для вкладок"""
        index = self.tabAt(event.pos())
        if index < 0:
            return
        
        menu = QMenu(self)
        menu.addAction("🔄 Обновить", lambda: self.tab_clicked.emit(index))
        menu.addAction("📋 Дублировать", lambda: self.duplicate_requested.emit(index))
        menu.addAction("📌 Закрепить", lambda: self.pin_requested.emit(index))
        menu.addAction("🔇 Отключить звук", lambda: self.mute_requested.emit(index))
        menu.addSeparator()
        menu.addAction("📂 Закрыть справа", lambda: self.close_right_tabs(index))
        menu.addAction("📂 Закрыть другие", lambda: self.close_other_tabs(index))
        menu.exec_(event.globalPos())
    
    def close_right_tabs(self, index):
        """Закрыть вкладки справа"""
        for i in range(self.count() - 1, index, -1):
            self.close_requested.emit(i)
    
    def close_other_tabs(self, index):
        """Закрыть другие вкладки"""
        for i in range(self.count() - 1, -1, -1):
            if i != index:
                self.close_requested.emit(i)

class TabPreview(QWidget):
    """Виджет предпросмотра вкладки"""
    
    def __init__(self, url, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Миниатюра страницы
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(160, 100)
        self.preview_label.setStyleSheet("""
            border: 1px solid #2a2a3e;
            border-radius: 4px;
            background: #1a1a2e;
        """)
        layout.addWidget(self.preview_label)
        
        # Заголовок
        self.title_label = QLabel(title[:30])
        self.title_label.setStyleSheet("color: #c0c0d0; font-size: 11px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.setStyleSheet("""
            QWidget {
                background: #1a1a2e;
                border-radius: 8px;
                padding: 5px;
            }
            QWidget:hover {
                background: #2a2a3e;
            }
        """)

class TabManager(QTabWidget):
    """Менеджер вкладок с расширенными функциями"""
    
    # Сигналы
    tab_changed = pyqtSignal(int)
    new_tab_requested = pyqtSignal(str)
    close_tab_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.closed_tabs = []
        self.max_closed_tabs = 25
        self.pinned_tabs = []
        self.muted_tabs = []
        
    def setup_ui(self):
        """Настройка интерфейса"""
        # Создаем кастомный TabBar
        self.tab_bar = TabBar(self)
        self.setTabBar(self.tab_bar)
        
        # Подключаем сигналы
        self.tab_bar.close_requested.connect(self.close_tab)
        self.tab_bar.duplicate_requested.connect(self.duplicate_tab)
        self.tab_bar.pin_requested.connect(self.pin_tab)
        self.tab_bar.mute_requested.connect(self.mute_tab)
        
        # Настройка внешнего вида
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #0a0a1a;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
        """)
        
        self.currentChanged.connect(self.tab_changed.emit)
        
        # Кнопка новой вкладки
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(30, 25)
        self.new_tab_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #808090;
                font-size: 20px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #2a2a3e;
                color: white;
            }
        """)
        self.new_tab_button.clicked.connect(lambda: self.new_tab_requested.emit("about:blank"))
        self.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)
    
    def add_tab(self, url="about:blank", title="Новая вкладка"):
        """Добавление новой вкладки"""
        # Создаем контейнер для вкладки
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем веб-вью
        web_view = QWebEngineView()
        web_view.setUrl(url)
        layout.addWidget(web_view)
        
        # Добавляем вкладку
        index = self.addTab(container, title)
        self.setCurrentIndex(index)
        self.setTabToolTip(index, url)
        
        return container
    
    def close_tab(self, index):
        """Закрытие вкладки с сохранением в истории"""
        if index < 0 or index >= self.count():
            return
        
        # Сохраняем вкладку в закрытые
        widget = self.widget(index)
        if widget:
            # Получаем URL и заголовок
            web_view = widget.findChild(QWebEngineView)
            if web_view:
                url = web_view.url().toString()
                title = self.tabText(index)
                self.closed_tabs.append({
                    'url': url,
                    'title': title,
                    'widget': widget
                })
                if len(self.closed_tabs) > self.max_closed_tabs:
                    self.closed_tabs.pop(0)
        
        self.removeTab(index)
        self.close_tab_requested.emit(index)
        
        # Если вкладок не осталось, создаем новую
        if self.count() == 0:
            self.new_tab_requested.emit("about:blank")
    
    def restore_tab(self):
        """Восстановление закрытой вкладки"""
        if not self.closed_tabs:
            return
        
        tab_data = self.closed_tabs.pop()
        container = self.add_tab(tab_data['url'], tab_data['title'])
        self.setCurrentWidget(container)
    
    def duplicate_tab(self, index):
        """Дублирование вкладки"""
        if index < 0 or index >= self.count():
            return
        
        widget = self.widget(index)
        web_view = widget.findChild(QWebEngineView)
        if web_view:
            url = web_view.url().toString()
            title = self.tabText(index)
            self.add_tab(url, f"{title} (копия)")
    
    def pin_tab(self, index):
        """Закрепление вкладки"""
        if index in self.pinned_tabs:
            self.pinned_tabs.remove(index)
        else:
            self.pinned_tabs.append(index)
        
        # Обновляем внешний вид
        if index in self.pinned_tabs:
            self.setTabText(index, "📌 " + self.tabText(index))
        else:
            text = self.tabText(index).replace("📌 ", "")
            self.setTabText(index, text)
    
    def mute_tab(self, index):
        """Отключение звука в вкладке"""
        if index in self.muted_tabs:
            self.muted_tabs.remove(index)
            self.setTabText(index, self.tabText(index).replace("🔇 ", ""))
        else:
            self.muted_tabs.append(index)
            self.setTabText(index, "🔇 " + self.tabText(index))
        
        # Отключаем звук на странице
        widget = self.widget(index)
        web_view = widget.findChild(QWebEngineView)
        if web_view:
            web_view.page().setAudioMuted(index in self.muted_tabs)
    
    def show_all_tabs(self):
        """Показать все вкладки в виде сетки"""
        # Создаем диалог с превью
        from PyQt5.QtWidgets import QDialog, QScrollArea
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📊 Все вкладки")
        dialog.setGeometry(200, 200, 800, 500)
        dialog.setStyleSheet("""
            QDialog {
                background: #0a0a1a;
            }
        """)
        
        scroll = QScrollArea(dialog)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(10)
        
        # Добавляем все вкладки
        for i in range(self.count()):
            title = self.tabText(i)
            url = self.tabToolTip(i)
            
            preview = TabPreview(url, title)
            preview.mousePressEvent = lambda e, idx=i: self.setCurrentIndex(idx)
            
            row = i // 4
            col = i % 4
            grid_layout.addWidget(preview, row, col)
        
        scroll.setWidget(container)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll)
        dialog.exec_()
    
    def save_tabs(self):
        """Сохранение состояния вкладок"""
        tabs_data = []
        for i in range(self.count()):
            widget = self.widget(i)
            web_view = widget.findChild(QWebEngineView)
            if web_view:
                tabs_data.append({
                    'url': web_view.url().toString(),
                    'title': self.tabText(i),
                    'pinned': i in self.pinned_tabs
                })
        
        import json
        try:
            with open("tabs_state.json", "w", encoding="utf-8") as f:
                json.dump(tabs_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_tabs(self):
        """Загрузка состояния вкладок"""
        import json
        try:
            with open("tabs_state.json", "r", encoding="utf-8") as f:
                tabs_data = json.load(f)
                for tab_data in tabs_data:
                    self.add_tab(tab_data['url'], tab_data['title'])
        except:
            pass
    
    def next_tab(self):
        """Переключение на следующую вкладку"""
        index = self.currentIndex() + 1
        if index >= self.count():
            index = 0
        self.setCurrentIndex(index)
    
    def prev_tab(self):
        """Переключение на предыдущую вкладку"""
        index = self.currentIndex() - 1
        if index < 0:
            index = self.count() - 1
        self.setCurrentIndex(index)
    
    def get_tab_info(self, index):
        """Получение информации о вкладке"""
        if index < 0 or index >= self.count():
            return None
        
        widget = self.widget(index)
        web_view = widget.findChild(QWebEngineView)
        
        return {
            'url': web_view.url().toString() if web_view else "",
            'title': self.tabText(index),
            'pinned': index in self.pinned_tabs,
            'muted': index in self.muted_tabs
        }