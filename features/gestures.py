"""
Жесты мышью:
- 8 жестов для навигации
- Настройка жестов
- Визуальная обратная связь
"""

from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPaintEvent
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class GestureManager:
    """Менеджер жестов мышью"""
    
    # Сигналы
    gesture_performed = pyqtSignal(str)
    
    def __init__(self):
        self.enabled = True
        self.mouse_tracking = False
        self.start_point = None
        self.current_point = None
        self.gesture_path = []
        self.visual_feedback = True
        
        # Настройки жестов
        self.gesture_threshold = 50  # пикселей
        self.gesture_timeout = 500  # миллисекунд
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        
        # Сопоставление жестов с действиями
        self.gesture_actions = {
            "LR": "forward",  # Вправо-влево
            "RL": "back",     # Влево-вправо
            "UD": "up",       # Вверх-вниз
            "DU": "down",     # Вниз-вверх
            "UR": "new_tab",  # Вверх-вправо
            "UL": "close_tab",# Вверх-влево
            "DR": "reload",   # Вниз-вправо
            "DL": "home"      # Вниз-влево
        }
        
        # Инвертированные жесты
        self.gesture_actions_reverse = {v: k for k, v in self.gesture_actions.items()}
    
    def start_gesture(self, pos: QPoint):
        """Начало жеста"""
        if not self.enabled:
            return
        
        self.mouse_tracking = True
        self.start_point = pos
        self.current_point = pos
        self.gesture_path = [pos]
        self.timer.start(self.gesture_timeout)
    
    def update_gesture(self, pos: QPoint):
        """Обновление жеста"""
        if not self.mouse_tracking:
            return
        
        self.current_point = pos
        self.gesture_path.append(pos)
        
        # Проверка на завершение жеста
        if self.is_gesture_complete():
            self.finish_gesture()
    
    def finish_gesture(self):
        """Завершение жеста"""
        self.mouse_tracking = False
        self.timer.stop()
        
        if len(self.gesture_path) < 2:
            return
        
        # Определяем направление жеста
        gesture = self.detect_gesture()
        
        if gesture:
            # Выполняем действие
            action = self.gesture_actions.get(gesture)
            if action:
                self.gesture_performed.emit(action)
                self.show_visual_feedback(gesture)
    
    def detect_gesture(self) -> Optional[str]:
        """Определение жеста по траектории"""
        if len(self.gesture_path) < 2:
            return None
        
        start = self.gesture_path[0]
        end = self.gesture_path[-1]
        
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        
        # Определяем основное направление
        if abs(dx) > abs(dy):
            direction = "R" if dx > 0 else "L"
        else:
            direction = "D" if dy > 0 else "U"
        
        # Проверяем на составной жест
        if len(self.gesture_path) > 3:
            # Ищем смену направления
            mid_point = self.gesture_path[len(self.gesture_path) // 2]
            mid_dx = mid_point.x() - start.x()
            mid_dy = mid_point.y() - start.y()
            
            if abs(mid_dx) > self.gesture_threshold or abs(mid_dy) > self.gesture_threshold:
                if abs(mid_dx) > abs(mid_dy):
                    mid_dir = "R" if mid_dx > 0 else "L"
                else:
                    mid_dir = "D" if mid_dy > 0 else "U"
                
                if mid_dir != direction:
                    # Составной жест
                    return f"{mid_dir}{direction}"
        
        # Простой жест
        return direction
    
    def is_gesture_complete(self) -> bool:
        """Проверка, завершен ли жест"""
        if not self.start_point or not self.current_point:
            return False
        
        dx = self.current_point.x() - self.start_point.x()
        dy = self.current_point.y() - self.start_point.y()
        
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance > self.gesture_threshold
    
    def show_visual_feedback(self, gesture: str):
        """Показ визуальной обратной связи"""
        if not self.visual_feedback:
            return
        
        # Создаем временный виджет для отображения жеста
        feedback = QLabel()
        feedback.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        feedback.setAttribute(Qt.WA_TranslucentBackground)
        feedback.setStyleSheet("""
            QLabel {
                background: rgba(0, 212, 255, 0.2);
                border: 2px solid #00d4ff;
                border-radius: 10px;
                color: #00d4ff;
                padding: 15px 25px;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        # Отображаем название жеста
        action = self.gesture_actions.get(gesture, gesture)
        feedback.setText(f"✋ {gesture} → {action}")
        feedback.adjustSize()
        
        # Позиционируем в центре экрана
        screen = QApplication.primaryScreen()
        if screen:
            rect = screen.geometry()
            x = (rect.width() - feedback.width()) // 2
            y = (rect.height() - feedback.height()) // 2
            feedback.move(x, y)
        
        feedback.show()
        
        # Автоматически скрываем через 1 секунду
        QTimer.singleShot(1000, feedback.close)
    
    def set_gesture_action(self, gesture: str, action: str):
        """Установка действия для жеста"""
        self.gesture_actions[gesture] = action
        self.save_gestures()
    
    def get_gesture_for_action(self, action: str) -> Optional[str]:
        """Получение жеста для действия"""
        for gesture, action_name in self.gesture_actions.items():
            if action_name == action:
                return gesture
        return None
    
    def save_gestures(self):
        """Сохранение настроек жестов"""
        try:
            with open("gestures.json", "w", encoding="utf-8") as f:
                json.dump(self.gesture_actions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения жестов: {e}")
    
    def load_gestures(self):
        """Загрузка настроек жестов"""
        try:
            with open("gestures.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
                self.gesture_actions.update(loaded)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки жестов: {e}")
    
    def enable(self):
        """Включение жестов"""
        self.enabled = True
    
    def disable(self):
        """Отключение жестов"""
        self.enabled = False
        self.mouse_tracking = False
        self.timer.stop()
    
    def toggle(self):
        """Переключение жестов"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.mouse_tracking = False
            self.timer.stop()