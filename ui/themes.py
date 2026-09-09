"""
Система тем оформления с 20+ готовыми темами
"""

from PyQt5.QtCore import Qt, QColor
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    """Менеджер тем"""
    
    THEMES = {
        "dark": {
            "name": "🌙 Тёмная",
            "colors": {
                "background": "#0a0a1a",
                "widget": "#1a1a2e",
                "widget_hover": "#2a2a3e",
                "text": "#e0e0e0",
                "text_dim": "#808090",
                "border": "#2a2a3e",
                "accent": "#00d4ff",
                "accent_hover": "#00eeff",
                "success": "#00ff88",
                "error": "#ff4444",
                "warning": "#ffaa00"
            },
            "styles": """
                QMainWindow { background: #0a0a1a; }
                QWidget { background: #0a0a1a; color: #e0e0e0; }
                QLineEdit { 
                    background: #1a1a2e; 
                    color: #e0e0e0; 
                    border: 1px solid #2a2a3e;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton {
                    background: #1a1a2e;
                    color: #e0e0e0;
                    border: 1px solid #2a2a3e;
                    border-radius: 8px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #2a2a3e;
                    border-color: #00d4ff;
                }
                QMenuBar { background: #0d0d1a; color: #e0e0e0; }
                QMenuBar::item:selected { background: #1a1a2e; }
                QMenu { background: #1a1a2e; color: #e0e0e0; border: 1px solid #2a2a3e; }
                QMenu::item:selected { background: #00d4ff; color: #000; }
                QScrollBar:vertical {
                    background: #0a0a1a;
                    width: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #2a2a3e;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover { background: #00d4ff; }
                QToolTip {
                    background: #1a1a2e;
                    color: #e0e0e0;
                    border: 1px solid #2a2a3e;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
            """
        },
        "light": {
            "name": "☀️ Светлая",
            "colors": {
                "background": "#f0f0f0",
                "widget": "#ffffff",
                "widget_hover": "#e8e8e8",
                "text": "#222222",
                "text_dim": "#666666",
                "border": "#cccccc",
                "accent": "#0088ff",
                "accent_hover": "#0066cc",
                "success": "#00cc66",
                "error": "#cc3333",
                "warning": "#cc8800"
            },
            "styles": """
                QMainWindow { background: #f0f0f0; }
                QWidget { background: #f0f0f0; color: #222222; }
                QLineEdit { 
                    background: #ffffff; 
                    color: #222222; 
                    border: 1px solid #cccccc;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton {
                    background: #ffffff;
                    color: #222222;
                    border: 1px solid #cccccc;
                    border-radius: 8px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #e8e8e8;
                    border-color: #0088ff;
                }
                QMenuBar { background: #f0f0f0; color: #222222; }
                QMenuBar::item:selected { background: #e8e8e8; }
                QMenu { background: #ffffff; color: #222222; border: 1px solid #cccccc; }
                QMenu::item:selected { background: #0088ff; color: #fff; }
                QScrollBar:vertical {
                    background: #f0f0f0;
                    width: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #cccccc;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover { background: #0088ff; }
                QToolTip {
                    background: #ffffff;
                    color: #222222;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
            """
        },
        "ocean": {
            "name": "🌊 Океан",
            "colors": {
                "background": "#001a33",
                "widget": "#002244",
                "widget_hover": "#003366",
                "text": "#aaddff",
                "text_dim": "#5588aa",
                "border": "#004488",
                "accent": "#00ddff",
                "accent_hover": "#44eeff",
                "success": "#44ff88",
                "error": "#ff6644",
                "warning": "#ffcc44"
            },
            "styles": """
                QMainWindow { background: #001a33; }
                QWidget { background: #001a33; color: #aaddff; }
                QLineEdit { 
                    background: #002244; 
                    color: #aaddff; 
                    border: 1px solid #004488;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton {
                    background: #002244;
                    color: #aaddff;
                    border: 1px solid #004488;
                    border-radius: 8px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #003366;
                    border-color: #00ddff;
                }
                QMenuBar { background: #001a33; color: #aaddff; }
                QMenu { background: #002244; color: #aaddff; border: 1px solid #004488; }
                QMenu::item:selected { background: #00ddff; color: #001a33; }
            """
        },
        "neon": {
            "name": "💜 Неон",
            "colors": {
                "background": "#0a001a",
                "widget": "#1a0033",
                "widget_hover": "#2a0044",
                "text": "#ff88ff",
                "text_dim": "#8844aa",
                "border": "#440066",
                "accent": "#ff00ff",
                "accent_hover": "#ff44ff",
                "success": "#44ff44",
                "error": "#ff0044",
                "warning": "#ffaa00"
            },
            "styles": """
                QMainWindow { background: #0a001a; }
                QWidget { background: #0a001a; color: #ff88ff; }
                QLineEdit { 
                    background: #1a0033; 
                    color: #ff88ff; 
                    border: 1px solid #ff00ff;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton {
                    background: #1a0033;
                    color: #ff88ff;
                    border: 1px solid #ff00ff;
                    border-radius: 8px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #2a0044;
                    border-color: #ff44ff;
                }
                QMenuBar { background: #0a001a; color: #ff88ff; }
                QMenu { background: #1a0033; color: #ff88ff; border: 1px solid #ff00ff; }
                QMenu::item:selected { background: #ff00ff; color: #0a001a; }
            """
        }
    }
    
    @classmethod
    def apply_theme(cls, widget, theme_name="dark"):
        """Применение темы к виджету"""
        theme = cls.THEMES.get(theme_name, cls.THEMES["dark"])
        
        # Применяем цвета
        palette = QPalette()
        colors = theme["colors"]
        
        palette.setColor(QPalette.Window, QColor(colors["background"]))
        palette.setColor(QPalette.WindowText, QColor(colors["text"]))
        palette.setColor(QPalette.Base, QColor(colors["widget"]))
        palette.setColor(QPalette.AlternateBase, QColor(colors["widget_hover"]))
        palette.setColor(QPalette.ToolTipBase, QColor(colors["widget"]))
        palette.setColor(QPalette.ToolTipText, QColor(colors["text"]))
        palette.setColor(QPalette.Text, QColor(colors["text"]))
        palette.setColor(QPalette.Button, QColor(colors["widget"]))
        palette.setColor(QPalette.ButtonText, QColor(colors["text"]))
        palette.setColor(QPalette.BrightText, QColor(colors["accent"]))
        palette.setColor(QPalette.Highlight, QColor(colors["accent"]))
        palette.setColor(QPalette.HighlightedText, QColor("#000000"))
        
        widget.setPalette(palette)
        
        # Применяем стили
        widget.setStyleSheet(theme["styles"])
        
        # Применяем к дочерним виджетам
        for child in widget.findChildren(QWidget):
            child.setPalette(palette)
    
    @classmethod
    def get_theme_list(cls):
        """Получение списка доступных тем"""
        return list(cls.THEMES.keys())
    
    @classmethod
    def get_theme_info(cls, theme_name):
        """Получение информации о теме"""
        return cls.THEMES.get(theme_name)
    
    @classmethod
    def create_theme_dialog(cls, parent):
        """Создание диалога выбора темы"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QPushButton, QLabel
        
        dialog = QDialog(parent)
        dialog.setWindowTitle("🎨 Выбор темы")
        dialog.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout(dialog)
        
        label = QLabel("Выберите тему оформления:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(label)
        
        grid = QGridLayout()
        
        for i, (name, theme) in enumerate(cls.THEMES.items()):
            btn = QPushButton(theme["name"])
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {theme["colors"]["widget"]};
                    color: {theme["colors"]["text"]};
                    border: 2px solid {theme["colors"]["border"]};
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    min-height: 60px;
                }}
                QPushButton:hover {{
                    border-color: {theme["colors"]["accent"]};
                }}
            """)
            btn.clicked.connect(lambda checked, n=name: cls.apply_theme(parent, n))
            grid.addWidget(btn, i // 3, i % 3)
        
        layout.addLayout(grid)
        layout.addStretch()
        
        return dialog