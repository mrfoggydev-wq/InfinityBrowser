"""
Система логирования:
- Запись логов в файл
- Разные уровни логирования
- Ротация логов
- Фильтрация
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """Система логирования"""
    
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    def __init__(self, name: str = "SuperBrowser", log_dir: str = "./logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        
        # Создаем директорию для логов
        os.makedirs(log_dir, exist_ok=True)
        
        # Настройка логгера
        self.setup_logger()
    
    def setup_logger(self):
        """Настройка логгера"""
        self.logger.setLevel(logging.DEBUG)
        
        # Формат логов
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler для файла
        log_file = os.path.join(self.log_dir, f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Логирование отладочной информации"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Логирование информационного сообщения"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Логирование предупреждения"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Логирование ошибки"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Логирование критической ошибки"""
        self.logger.critical(message)
    
    def log_exception(self, e: Exception, context: str = ""):
        """Логирование исключения"""
        self.logger.error(f"Exception in {context}: {str(e)}")
        self.logger.exception(e)
    
    def log_performance(self, operation: str, duration: float):
        """Логирование производительности"""
        self.logger.info(f"Performance - {operation}: {duration:.2f}s")
    
    def log_user_action(self, action: str, details: str = ""):
        """Логирование действия пользователя"""
        self.logger.info(f"User action - {action}: {details}")
    
    def set_level(self, level: str):
        """Установка уровня логирования"""
        if level in self.LOG_LEVELS:
            self.logger.setLevel(self.LOG_LEVELS[level])
    
    def get_log_files(self) -> list:
        """Получение списка файлов логов"""
        return sorted([
            f for f in os.listdir(self.log_dir)
            if f.startswith(self.name) and f.endswith('.log')
        ])
    
    def get_log_content(self, filename: str, lines: int = 100) -> str:
        """Получение содержимого лога"""
        log_file = os.path.join(self.log_dir, filename)
        if not os.path.exists(log_file):
            return "Файл лога не найден"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        except Exception as e:
            return f"Ошибка чтения лога: {e}"
    
    def clear_logs(self, days: int = 7):
        """Очистка старых логов"""
        now = datetime.now()
        for filename in self.get_log_files():
            # Парсим дату из имени файла
            try:
                date_str = filename.split('_')[1].split('.')[0]
                file_date = datetime.strptime(date_str, '%Y%m%d')
                if (now - file_date).days > days:
                    os.remove(os.path.join(self.log_dir, filename))
            except:
                pass

class PerformanceLogger:
    """Логгер производительности"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.start_time = {}
    
    def start_timer(self, operation: str):
        """Начало таймера"""
        self.start_time[operation] = datetime.now()
    
    def stop_timer(self, operation: str):
        """Остановка таймера"""
        if operation in self.start_time:
            duration = (datetime.now() - self.start_time[operation]).total_seconds()
            self.logger.log_performance(operation, duration)
            del self.start_time[operation]
            return duration
        return None
    
    def measure(self, operation: str):
        """Декоратор для измерения времени"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.start_timer(operation)
                result = func(*args, **kwargs)
                self.stop_timer(operation)
                return result
            return wrapper
        return decorator