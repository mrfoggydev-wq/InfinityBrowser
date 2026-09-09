"""
Ночной режим для всех сайтов:
- Инверсия цветов
- Режим чтения
- Автоматическое включение по времени
- Настройка яркости
"""

import json
import os
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView

class DarkReader(QObject):
    """Менеджер ночного режима"""
    
    # Сигналы
    dark_mode_changed = pyqtSignal(bool)
    brightness_changed = pyqtSignal(int)
    contrast_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.enabled = False
        self.auto_enabled = False
        self.brightness = 100  # 0-200
        self.contrast = 100    # 0-200
        self.grayscale = False
        self.sepia = False
        
        self.auto_start_hour = 20  # 20:00
        self.auto_end_hour = 6     # 06:00
        
        # Загрузка настроек
        self.load_settings()
        
        # Таймер для автоматического включения
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.check_auto_mode)
        self.auto_timer.start(60000)  # Проверка каждую минуту
    
    def enable(self, apply_to_all: bool = True):
        """Включение ночного режима"""
        self.enabled = True
        self.dark_mode_changed.emit(True)
        
        if apply_to_all:
            self.apply_to_all_pages()
        
        self.save_settings()
    
    def disable(self, apply_to_all: bool = True):
        """Отключение ночного режима"""
        self.enabled = False
        self.dark_mode_changed.emit(False)
        
        if apply_to_all:
            self.apply_to_all_pages()
        
        self.save_settings()
    
    def toggle(self, apply_to_all: bool = True):
        """Переключение ночного режима"""
        if self.enabled:
            self.disable(apply_to_all)
        else:
            self.enable(apply_to_all)
    
    def apply_to_page(self, web_view: QWebEngineView):
        """Применение ночного режима к странице"""
        if not web_view:
            return
        
        if self.enabled:
            # Добавляем CSS для инверсии цветов
            css = self.generate_dark_css()
            self.inject_css(web_view, css)
        else:
            # Убираем CSS
            self.inject_css(web_view, "")
    
    def apply_to_all_pages(self):
        """Применение ночного режима ко всем страницам"""
        # Здесь код для применения ко всем вкладкам
        # В реальном приложении нужно получить все WebView
        pass
    
    def generate_dark_css(self) -> str:
        """Генерация CSS для ночного режима"""
        brightness_filter = f"brightness({self.brightness / 100})"
        contrast_filter = f"contrast({self.contrast / 100})"
        
        if self.grayscale:
            grayscale_filter = "grayscale(100%)"
        else:
            grayscale_filter = ""
        
        if self.sepia:
            sepia_filter = "sepia(100%)"
        else:
            sepia_filter = ""
        
        filters = " ".join([brightness_filter, contrast_filter, grayscale_filter, sepia_filter])
        
        css = f"""
        /* SuperBrowser Dark Mode */
        html {{
            filter: {filters};
        }}
        
        /* Инверсия цветов */
        body {{
            background-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }}
        
        /* Инверсия для изображений (частичная) */
        img, video, iframe {{
            filter: invert(1) hue-rotate(180deg) brightness(0.85);
        }}
        
        /* Ссылки */
        a {{
            color: #88ccff !important;
        }}
        
        a:hover {{
            color: #00ddff !important;
        }}
        
        /* Формы */
        input, textarea, select {{
            background-color: #2a2a3a !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a5a !important;
        }}
        
        /* Кнопки */
        button {{
            background-color: #2a2a3a !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a5a !important;
        }}
        
        button:hover {{
            background-color: #3a3a4a !important;
        }}
        
        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {{
            color: #f0f0f0 !important;
        }}
        
        /* Блоки кода */
        pre, code {{
            background-color: #0a0a1a !important;
            color: #f0f0f0 !important;
        }}
        
        /* Таблицы */
        table {{
            border-color: #3a3a4a !important;
        }}
        
        th, td {{
            border-color: #3a3a4a !important;
        }}
        
        /* Списки */
        ul, ol {{
            color: #e0e0e0 !important;
        }}
        
        /* Блоки */
        div, section, article, header, footer, nav, main {{
            background-color: transparent !important;
        }}
        
        /* Параграфы */
        p {{
            color: #e0e0e0 !important;
        }}
        
        /* Границы */
        hr {{
            border-color: #3a3a4a !important;
        }}
        """
        
        return css
    
    def inject_css(self, web_view: QWebEngineView, css: str):
        """Инъекция CSS в страницу"""
        if not web_view:
            return
        
        # Код для инъекции CSS
        script = f"""
        (function() {{
            var style = document.getElementById('superbrowser-dark-mode');
            if (!style) {{
                style = document.createElement('style');
                style.id = 'superbrowser-dark-mode';
                document.head.appendChild(style);
            }}
            style.textContent = `{css}`;
        }})();
        """
        
        web_view.page().runJavaScript(script)
    
    def set_brightness(self, value: int):
        """Установка яркости"""
        self.brightness = max(0, min(200, value))
        self.brightness_changed.emit(self.brightness)
        self.save_settings()
        
        if self.enabled:
            self.apply_to_all_pages()
    
    def set_contrast(self, value: int):
        """Установка контрастности"""
        self.contrast = max(0, min(200, value))
        self.contrast_changed.emit(self.contrast)
        self.save_settings()
        
        if self.enabled:
            self.apply_to_all_pages()
    
    def set_grayscale(self, enabled: bool):
        """Установка черно-белого режима"""
        self.grayscale = enabled
        self.save_settings()
        
        if self.enabled:
            self.apply_to_all_pages()
    
    def set_sepia(self, enabled: bool):
        """Установка сепии"""
        self.sepia = enabled
        self.save_settings()
        
        if self.enabled:
            self.apply_to_all_pages()
    
    def check_auto_mode(self):
        """Проверка автоматического режима"""
        if not self.auto_enabled:
            return
        
        current_hour = datetime.now().hour
        
        if self.auto_start_hour > self.auto_end_hour:
            # Переход через полночь
            should_be_enabled = (current_hour >= self.auto_start_hour or 
                               current_hour < self.auto_end_hour)
        else:
            should_be_enabled = (self.auto_start_hour <= current_hour < self.auto_end_hour)
        
        if should_be_enabled and not self.enabled:
            self.enable()
        elif not should_be_enabled and self.enabled:
            self.disable()
    
    def set_auto_time(self, start_hour: int, end_hour: int):
        """Установка времени автоматического режима"""
        self.auto_start_hour = max(0, min(23, start_hour))
        self.auto_end_hour = max(0, min(23, end_hour))
        self.save_settings()
    
    def enable_auto(self):
        """Включение автоматического режима"""
        self.auto_enabled = True
        self.save_settings()
        self.check_auto_mode()
    
    def disable_auto(self):
        """Отключение автоматического режима"""
        self.auto_enabled = False
        self.save_settings()
    
    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open("dark_reader_settings.json", "w", encoding="utf-8") as f:
                json.dump({
                    "enabled": self.enabled,
                    "auto_enabled": self.auto_enabled,
                    "brightness": self.brightness,
                    "contrast": self.contrast,
                    "grayscale": self.grayscale,
                    "sepia": self.sepia,
                    "auto_start_hour": self.auto_start_hour,
                    "auto_end_hour": self.auto_end_hour
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек DarkReader: {e}")
    
    def load_settings(self):
        """Загрузка настроек"""
        try:
            with open("dark_reader_settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.enabled = data.get("enabled", False)
                self.auto_enabled = data.get("auto_enabled", False)
                self.brightness = data.get("brightness", 100)
                self.contrast = data.get("contrast", 100)
                self.grayscale = data.get("grayscale", False)
                self.sepia = data.get("sepia", False)
                self.auto_start_hour = data.get("auto_start_hour", 20)
                self.auto_end_hour = data.get("auto_end_hour", 6)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки настроек DarkReader: {e}")