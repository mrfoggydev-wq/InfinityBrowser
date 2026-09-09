"""
Голосовое управление:
- Распознавание речи
- 30+ голосовых команд
- Синтез речи (TTS)
- Настройка голоса
"""

import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import os
import threading
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class VoiceController(QObject):
    """Контроллер голосового управления"""
    
    # Сигналы
    command_recognized = pyqtSignal(str)
    command_processed = pyqtSignal(str, bool)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Настройки
        self.enabled = False
        self.language = "ru-RU"
        self.energy_threshold = 3000
        self.pause_threshold = 0.8
        
        # Распознаватель
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.listener_thread = None
        
        # Команды
        self.commands = self.init_commands()
        
        # TTS
        self.tts_enabled = True
        self.tts_language = "ru"
        
        # Инициализация pygame для аудио
        pygame.mixer.init()
    
    def init_commands(self) -> Dict:
        """Инициализация голосовых команд"""
        return {
            # Навигация
            "открой": "open",
            "перейди": "navigate",
            "назад": "back",
            "вперед": "forward",
            "обнови": "reload",
            "домой": "home",
            
            # Вкладки
            "новая вкладка": "new_tab",
            "закрыть вкладку": "close_tab",
            "следующая вкладка": "next_tab",
            "предыдущая вкладка": "prev_tab",
            "восстановить вкладку": "restore_tab",
            
            # Поиск
            "найди": "find",
            "поиск": "search",
            "гугл": "google",
            "яндекс": "yandex",
            
            # Функции
            "закладка": "bookmark",
            "история": "history",
            "загрузки": "downloads",
            "настройки": "settings",
            "помощь": "help",
            
            # Режимы
            "полный экран": "fullscreen",
            "ночной режим": "dark_mode",
            "увеличь": "zoom_in",
            "уменьши": "zoom_out",
            "сбросить масштаб": "zoom_reset",
            
            # Инструменты
            "скриншот": "screenshot",
            "заметки": "notes",
            "калькулятор": "calculator",
            "погода": "weather",
            
            # Управление
            "стоп": "stop",
            "выключи": "stop",
            "привет": "hello",
            "спасибо": "thanks"
        }
    
    def start_listening(self):
        """Начать прослушивание"""
        if self.listening:
            return
        
        self.listening = True
        self.listener_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listener_thread.start()
        self.listening_started.emit()
        self.speak("Голосовое управление активировано")
    
    def stop_listening(self):
        """Остановить прослушивание"""
        self.listening = False
        if self.listener_thread:
            self.listener_thread.join(timeout=1)
            self.listener_thread = None
        self.listening_stopped.emit()
        self.speak("Голосовое управление деактивировано")
    
    def listen_loop(self):
        """Цикл прослушивания"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.listening:
                try:
                    # Слушаем речь
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    # Распознаем
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    text = text.lower().strip()
                    
                    if text:
                        self.command_recognized.emit(text)
                        self.process_command(text)
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    self.error_occurred.emit(f"Ошибка распознавания: {e}")
                except Exception as e:
                    print(f"Ошибка: {e}")
    
    def process_command(self, text: str):
        """Обработка голосовой команды"""
        # Ищем команду в словаре
        command = None
        params = []
        
        for cmd, action in self.commands.items():
            if text.startswith(cmd):
                command = action
                params = text[len(cmd):].strip().split()
                break
        
        if command:
            # Обрабатываем команду
            self.handle_command(command, params)
            self.command_processed.emit(text, True)
        else:
            # Если команда не распознана, пробуем как поисковый запрос
            self.handle_command("search", [text])
            self.command_processed.emit(text, False)
    
    def handle_command(self, command: str, params: List[str]):
        """Выполнение команды"""
        from ui.main_window import SuperMainWindow
        
        if command == "open" and params:
            url = params[0] if params else ""
            if not url.startswith("http"):
                url = f"https://{url}"
            # Открываем URL
            self.emit_signal("open_url", url)
            
        elif command == "navigate" and params:
            # Навигация
            self.emit_signal("navigate", " ".join(params))
            
        elif command == "back":
            self.emit_signal("go_back")
            
        elif command == "forward":
            self.emit_signal("go_forward")
            
        elif command == "reload":
            self.emit_signal("reload")
            
        elif command == "home":
            self.emit_signal("go_home")
            
        elif command == "new_tab":
            self.emit_signal("new_tab")
            
        elif command == "close_tab":
            self.emit_signal("close_tab")
            
        elif command == "next_tab":
            self.emit_signal("next_tab")
            
        elif command == "prev_tab":
            self.emit_signal("prev_tab")
            
        elif command == "restore_tab":
            self.emit_signal("restore_tab")
            
        elif command == "find" and params:
            self.emit_signal("find", " ".join(params))
            
        elif command == "search":
            search_query = " ".join(params)
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            self.emit_signal("open_url", search_url)
            
        elif command == "google":
            self.emit_signal("open_url", "https://www.google.com")
            
        elif command == "yandex":
            self.emit_signal("open_url", "https://ya.ru")
            
        elif command == "bookmark":
            self.emit_signal("toggle_bookmark")
            
        elif command == "history":
            self.emit_signal("show_history")
            
        elif command == "downloads":
            self.emit_signal("show_downloads")
            
        elif command == "settings":
            self.emit_signal("show_settings")
            
        elif command == "help":
            self.emit_signal("show_help")
            
        elif command == "fullscreen":
            self.emit_signal("toggle_fullscreen")
            
        elif command == "dark_mode":
            self.emit_signal("toggle_dark_mode")
            
        elif command == "zoom_in":
            self.emit_signal("zoom", 0.1)
            
        elif command == "zoom_out":
            self.emit_signal("zoom", -0.1)
            
        elif command == "zoom_reset":
            self.emit_signal("reset_zoom")
            
        elif command == "screenshot":
            self.emit_signal("take_screenshot")
            
        elif command == "notes":
            self.emit_signal("show_notes")
            
        elif command == "calculator":
            self.emit_signal("toggle_calculator")
            
        elif command == "weather":
            self.emit_signal("show_weather")
            
        elif command == "stop":
            self.stop_listening()
            
        elif command == "hello":
            self.speak("Привет! Я ваш голосовой помощник!")
            
        elif command == "thanks":
            self.speak("Пожалуйста! Обращайтесь еще!")
    
    def emit_signal(self, signal_name: str, *args):
        """Эмуляция отправки сигнала"""
        # Здесь должен быть код для отправки сигналов в главное окно
        # В реальном приложении используем pyqtSignal
        print(f"Сигнал: {signal_name} {args}")
    
    def speak(self, text: str):
        """Синтез речи (TTS)"""
        if not self.tts_enabled:
            return
        
        try:
            # Создаем аудио
            tts = gTTS(text=text, lang=self.tts_language, slow=False)
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                audio_file = f.name
            
            # Воспроизводим
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Ждем окончания воспроизведения
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Удаляем временный файл
            os.unlink(audio_file)
            
        except Exception as e:
            print(f"Ошибка TTS: {e}")
    
    def set_language(self, language: str):
        """Установка языка"""
        self.language = language
        if language.startswith("ru"):
            self.tts_language = "ru"
        elif language.startswith("en"):
            self.tts_language = "en"
        else:
            self.tts_language = "auto"
    
    def toggle(self):
        """Включение/выключение"""
        if self.enabled:
            self.stop_listening()
            self.enabled = False
        else:
            self.start_listening()
            self.enabled = True
    
    def get_commands_list(self) -> Dict[str, str]:
        """Получение списка команд"""
        return self.commands