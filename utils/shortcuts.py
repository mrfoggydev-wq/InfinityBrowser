"""
Система горячих клавиш:
- Настраиваемые комбинации
- Конфликты клавиш
- Импорт/экспорт настроек
"""

import json
from PyQt5.QtCore import Qt, QKeySequence, pyqtSignal
from PyQt5.QtWidgets import QAction, QShortcut, QKeySequenceEdit, QDialog

class ShortcutManager:
    """Менеджер горячих клавиш"""
    
    # Сигналы
    shortcut_triggered = pyqtSignal(str)  # action_name
    
    # Стандартные комбинации
    DEFAULT_SHORTCUTS = {
        "new_tab": "Ctrl+T",
        "close_tab": "Ctrl+W",
        "restore_tab": "Ctrl+Shift+T",
        "next_tab": "Ctrl+Tab",
        "prev_tab": "Ctrl+Shift+Tab",
        "reload": "F5",
        "reload_force": "Ctrl+F5",
        "fullscreen": "F11",
        "dev_tools": "Ctrl+Shift+I",
        "zoom_in": "Ctrl++",
        "zoom_out": "Ctrl+-",
        "zoom_reset": "Ctrl+0",
        "find": "Ctrl+F",
        "find_next": "F3",
        "save_page": "Ctrl+S",
        "print": "Ctrl+P",
        "history": "Ctrl+H",
        "bookmarks": "Ctrl+D",
        "downloads": "Ctrl+J",
        "settings": "Ctrl+,",
        "new_window": "Ctrl+N",
        "incognito": "Ctrl+Shift+N",
        "back": "Alt+Left",
        "forward": "Alt+Right",
        "home": "Alt+Home",
        "close_window": "Ctrl+Q",
        "mute": "Ctrl+M",
        "screenshot": "Ctrl+Shift+S"
    }
    
    def __init__(self):
        self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
        self.actions = {}
        self.shortcuts_objects = []
        self.conflicts = {}
        
        # Загрузка сохраненных комбинаций
        self.load_shortcuts()
    
    def register_action(self, action_name: str, callback, parent=None):
        """Регистрация действия"""
        shortcut = self.shortcuts.get(action_name)
        if not shortcut:
            return None
        
        # Создаем QAction или QShortcut
        if parent:
            action = QAction(parent)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(callback)
            parent.addAction(action)
            
            self.actions[action_name] = action
            self.shortcuts_objects.append(action)
            
            return action
        
        return None
    
    def set_shortcut(self, action_name: str, shortcut: str):
        """Установка новой комбинации"""
        # Проверяем конфликты
        conflict = self.check_conflict(action_name, shortcut)
        if conflict:
            self.conflicts[action_name] = conflict
        
        # Обновляем комбинацию
        self.shortcuts[action_name] = shortcut
        
        # Обновляем QAction если есть
        if action_name in self.actions:
            self.actions[action_name].setShortcut(QKeySequence(shortcut))
        
        # Сохраняем настройки
        self.save_shortcuts()
    
    def check_conflict(self, action_name: str, shortcut: str) -> Optional[str]:
        """Проверка конфликтов с другими комбинациями"""
        for name, key in self.shortcuts.items():
            if name != action_name and key == shortcut:
                return name
        return None
    
    def get_shortcut(self, action_name: str) -> str:
        """Получение комбинации для действия"""
        return self.shortcuts.get(action_name, "")
    
    def get_all_shortcuts(self) -> dict:
        """Получение всех комбинаций"""
        return self.shortcuts
    
    def reset_to_defaults(self):
        """Сброс к стандартным комбинациям"""
        self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
        
        # Обновляем все QAction
        for name, action in self.actions.items():
            if name in self.shortcuts:
                action.setShortcut(QKeySequence(self.shortcuts[name]))
        
        self.save_shortcuts()
    
    def import_shortcuts(self, filename: str):
        """Импорт комбинаций из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for name, shortcut in data.items():
                    if name in self.shortcuts:
                        self.set_shortcut(name, shortcut)
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False
    
    def export_shortcuts(self, filename: str):
        """Экспорт комбинаций в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
    
    def save_shortcuts(self):
        """Сохранение комбинаций"""
        try:
            with open("shortcuts.json", "w", encoding='utf-8') as f:
                json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_shortcuts(self):
        """Загрузка комбинаций"""
        try:
            with open("shortcuts.json", "r", encoding='utf-8') as f:
                loaded = json.load(f)
                self.shortcuts.update(loaded)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    
    def show_shortcuts_dialog(self, parent=None):
        """Показать диалог настройки комбинаций"""
        dialog = QDialog(parent)
        dialog.setWindowTitle("⌨️ Горячие клавиши")
        dialog.setGeometry(300, 300, 500, 400)
        
        from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
        
        layout = QVBoxLayout(dialog)
        
        # Список комбинаций
        list_widget = QListWidget()
        for name, shortcut in sorted(self.shortcuts.items()):
            item_text = f"{name}: {shortcut}"
            list_widget.addItem(item_text)
        
        layout.addWidget(list_widget)
        
        # Кнопки
        btn_row = QHBoxLayout()
        
        btn_reset = QPushButton("↺ Сбросить")
        btn_reset.clicked.connect(lambda: self.reset_to_defaults())
        btn_row.addWidget(btn_reset)
        
        btn_export = QPushButton("📤 Экспорт")
        btn_export.clicked.connect(lambda: self.export_shortcuts("shortcuts_export.json"))
        btn_row.addWidget(btn_export)
        
        btn_import = QPushButton("📥 Импорт")
        btn_import.clicked.connect(lambda: self.import_shortcuts("shortcuts_export.json"))
        btn_row.addWidget(btn_import)
        
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(dialog.close)
        btn_row.addWidget(btn_close)
        
        layout.addLayout(btn_row)
        
        dialog.exec_()