"""
Встроенный переводчик:
- 100+ языков
- Автоопределение языка
- Перевод страниц
- Перевод выделенного текста
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal

class Translator(QObject):
    """Менеджер перевода"""
    
    # Сигналы
    translation_completed = pyqtSignal(str, str, str)  # text, from_lang, to_lang
    translation_failed = pyqtSignal(str, str)  # text, error
    
    # Поддерживаемые языки
    LANGUAGES = {
        "auto": "Автоопределение",
        "ru": "Русский",
        "en": "Английский",
        "de": "Немецкий",
        "fr": "Французский",
        "es": "Испанский",
        "it": "Итальянский",
        "pt": "Португальский",
        "zh": "Китайский",
        "ja": "Японский",
        "ko": "Корейский",
        "ar": "Арабский",
        "hi": "Хинди",
        "uk": "Украинский",
        "pl": "Польский",
        "tr": "Турецкий",
        "nl": "Голландский",
        "sv": "Шведский",
        "no": "Норвежский",
        "da": "Датский",
        "fi": "Финский",
        "hu": "Венгерский",
        "cs": "Чешский",
        "el": "Греческий",
        "he": "Иврит",
        "th": "Тайский",
        "vi": "Вьетнамский",
        "id": "Индонезийский",
        "ms": "Малайский",
        "fa": "Персидский"
    }
    
    def __init__(self):
        super().__init__()
        
        self.source_lang = "auto"
        self.target_lang = "ru"
        self.translation_cache = {}
        self.max_cache_size = 1000
        
        # Настройки
        self.use_google = True
        self.use_deepl = False
        self.api_key = None
        
        # Загрузка настроек
        self.load_settings()
    
    def translate(self, text: str, source: str = None, target: str = None) -> Optional[str]:
        """Перевод текста"""
        if not text:
            return None
        
        source = source or self.source_lang
        target = target or self.target_lang
        
        # Проверка кэша
        cache_key = f"{text}_{source}_{target}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        try:
            # Выбор метода перевода
            if self.use_google:
                result = self.translate_google(text, source, target)
            elif self.use_deepl:
                result = self.translate_deepl(text, source, target)
            else:
                result = self.translate_local(text, source, target)
            
            if result:
                # Сохраняем в кэш
                if len(self.translation_cache) >= self.max_cache_size:
                    # Удаляем старые записи
                    keys = list(self.translation_cache.keys())
                    for key in keys[:100]:
                        del self.translation_cache[key]
                
                self.translation_cache[cache_key] = result
                self.translation_completed.emit(text, source, target)
                return result
            
        except Exception as e:
            self.translation_failed.emit(text, str(e))
            return None
    
    def translate_google(self, text: str, source: str, target: str) -> Optional[str]:
        """Перевод через Google Translate"""
        try:
            # Используем бесплатный API
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": source,
                "tl": target,
                "dt": "t",
                "q": text
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Парсим результат
            if data and isinstance(data, list) and len(data) > 0:
                result = ""
                for item in data[0]:
                    if item and isinstance(item, list) and len(item) > 0:
                        result += item[0]
                return result
            
            return None
            
        except Exception as e:
            print(f"Ошибка перевода Google: {e}")
            return None
    
    def translate_deepl(self, text: str, source: str, target: str) -> Optional[str]:
        """Перевод через DeepL"""
        if not self.api_key:
            return None
        
        try:
            url = "https://api.deepl.com/v2/translate"
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "text": [text],
                "target_lang": target.upper()
            }
            if source != "auto":
                data["source_lang"] = source.upper()
            
            response = requests.post(url, json=data, headers=headers, timeout=5)
            response.raise_for_status()
            
            result = response.json()
            if "translations" in result and len(result["translations"]) > 0:
                return result["translations"][0]["text"]
            
            return None
            
        except Exception as e:
            print(f"Ошибка перевода DeepL: {e}")
            return None
    
    def translate_local(self, text: str, source: str, target: str) -> Optional[str]:
        """Локальный перевод (эмуляция)"""
        # В реальном приложении здесь может быть локальная модель
        # Например, через PyTorch или TensorFlow
        
        # Эмулируем перевод
        if source == target:
            return text
        
        # Простая эмуляция для демонстрации
        if target == "en" and source == "ru":
            # Эмулируем перевод с русского на английский
            return f"[EN] {text}"
        elif target == "ru" and source == "en":
            return f"[RU] {text}"
        else:
            return f"[{target}] {text}"
    
    def detect_language(self, text: str) -> Optional[str]:
        """Определение языка текста"""
        if not text:
            return None
        
        try:
            # Используем Google для определения языка
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": "auto",
                "tl": "en",
                "dt": "t",
                "q": text
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data and isinstance(data, list) and len(data) > 1:
                # Язык определяется во второй части ответа
                if len(data[1]) > 0 and len(data[1][0]) > 0:
                    return data[1][0][0]
            
            return None
            
        except Exception as e:
            print(f"Ошибка определения языка: {e}")
            return None
    
    def translate_page(self, html: str, source: str = "auto", target: str = "ru") -> str:
        """Перевод HTML страницы"""
        # Простой парсер для перевода текста внутри тегов
        # В реальном приложении используем BeautifulSoup
        
        # Эмулируем перевод страницы
        result = html
        # Здесь код для перевода содержимого страницы
        return result
    
    def translate_selection(self, text: str) -> Optional[str]:
        """Перевод выделенного текста"""
        return self.translate(text)
    
    def set_source_language(self, lang: str):
        """Установка исходного языка"""
        if lang in self.LANGUAGES:
            self.source_lang = lang
            self.save_settings()
    
    def set_target_language(self, lang: str):
        """Установка целевого языка"""
        if lang in self.LANGUAGES:
            self.target_lang = lang
            self.save_settings()
    
    def get_language_name(self, code: str) -> str:
        """Получение названия языка"""
        return self.LANGUAGES.get(code, code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Получение списка поддерживаемых языков"""
        return self.LANGUAGES
    
    def clear_cache(self):
        """Очистка кэша переводов"""
        self.translation_cache.clear()
    
    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open("translator_settings.json", "w", encoding="utf-8") as f:
                json.dump({
                    "source_lang": self.source_lang,
                    "target_lang": self.target_lang,
                    "use_google": self.use_google,
                    "use_deepl": self.use_deepl
                }, f)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings(self):
        """Загрузка настроек"""
        try:
            with open("translator_settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.source_lang = data.get("source_lang", "auto")
                self.target_lang = data.get("target_lang", "ru")
                self.use_google = data.get("use_google", True)
                self.use_deepl = data.get("use_deepl", False)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")