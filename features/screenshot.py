"""
Инструменты для создания скриншотов:
- Скриншот всей страницы
- Скриншот области
- Скриншот видимой области
- Аннотации
"""

from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
import os
from datetime import datetime

class ScreenshotManager:
    """Менеджер скриншотов"""
    
    # Сигналы
    screenshot_taken = pyqtSignal(str)  # filepath
    screenshot_failed = pyqtSignal(str)  # error
    
    def __init__(self):
        self.screenshot_dir = "./screenshots"
        self.format = "png"
        self.quality = 95
        self.auto_save = True
        self.include_cursor = False
        
        # Создаем директорию
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def capture_full_page(self, web_view) -> Optional[str]:
        """Скриншот всей страницы"""
        try:
            # Получаем размер страницы
            page = web_view.page()
            size = page.contentsSize()
            
            # Создаем изображение
            pixmap = QPixmap(size.width(), size.height())
            pixmap.fill(Qt.transparent)
            
            # Рендерим страницу
            painter = QPainter(pixmap)
            page.render(painter)
            painter.end()
            
            # Сохраняем
            return self.save_screenshot(pixmap)
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def capture_visible_area(self, web_view) -> Optional[str]:
        """Скриншот видимой области"""
        try:
            # Получаем видимую область
            pixmap = web_view.grab()
            return self.save_screenshot(pixmap)
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def capture_selection(self, web_view, selection: QRect) -> Optional[str]:
        """Скриншот выделенной области"""
        try:
            # Получаем полный скриншот
            full_pixmap = web_view.grab()
            
            # Вырезаем выделенную область
            if selection.isValid():
                pixmap = full_pixmap.copy(selection)
                return self.save_screenshot(pixmap)
            
            return None
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def capture_window(self, widget: QWidget) -> Optional[str]:
        """Скриншот окна"""
        try:
            pixmap = widget.grab()
            return self.save_screenshot(pixmap)
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def capture_fullscreen(self) -> Optional[str]:
        """Скриншот всего экрана"""
        try:
            screen = QApplication.primaryScreen()
            if screen:
                pixmap = screen.grabWindow(0)
                return self.save_screenshot(pixmap)
            return None
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def save_screenshot(self, pixmap: QPixmap) -> Optional[str]:
        """Сохранение скриншота"""
        try:
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.{self.format}"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Сохраняем
            if pixmap.save(filepath, self.format.upper(), self.quality):
                self.screenshot_taken.emit(filepath)
                return filepath
            
            return None
            
        except Exception as e:
            self.screenshot_failed.emit(str(e))
            return None
    
    def add_annotation(self, pixmap: QPixmap, annotations: list) -> QPixmap:
        """Добавление аннотаций к скриншоту"""
        painter = QPainter(pixmap)
        
        for annotation in annotations:
            if annotation["type"] == "rectangle":
                painter.setPen(QPen(QColor(annotation.get("color", "#ff0000")), 2))
                painter.drawRect(annotation["rect"])
            
            elif annotation["type"] == "text":
                painter.setPen(QPen(QColor(annotation.get("color", "#ffffff"))))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(annotation["pos"], annotation["text"])
            
            elif annotation["type"] == "arrow":
                painter.setPen(QPen(QColor(annotation.get("color", "#ff0000")), 2))
                painter.drawLine(annotation["start"], annotation["end"])
        
        painter.end()
        return pixmap
    
    def set_format(self, format: str):
        """Установка формата скриншотов"""
        if format.lower() in ["png", "jpg", "jpeg", "bmp"]:
            self.format = format.lower()
    
    def set_quality(self, quality: int):
        """Установка качества (для JPG)"""
        self.quality = max(1, min(100, quality))
    
    def set_screenshot_dir(self, directory: str):
        """Установка директории для скриншотов"""
        if os.path.exists(directory) or os.makedirs(directory, exist_ok=True):
            self.screenshot_dir = directory