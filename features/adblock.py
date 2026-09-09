"""
Модуль блокировки рекламы
Поддерживает: EasyList, EasyPrivacy, RuAdList, пользовательские фильтры
"""

import re
import json
import requests
from typing import List, Dict, Optional, Pattern
from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta

class AdBlockRule:
    """Класс правила блокировки"""
    
    def __init__(self, rule_string: str):
        self.raw = rule_string
        self.type = self.detect_type(rule_string)
        self.pattern = self.compile_pattern(rule_string)
        self.options = self.parse_options(rule_string)
        self.priority = self.calculate_priority()
    
    def detect_type(self, rule: str) -> str:
        """Определение типа правила"""
        if rule.startswith("||"):
            return "domain"
        elif rule.startswith("|"):
            return "start"
        elif rule.endswith("|"):
            return "end"
        elif "$" in rule:
            return "complex"
        else:
            return "contains"
    
    def compile_pattern(self, rule: str) -> Pattern:
        """Компиляция правила в регулярное выражение"""
        # Убираем опции
        if "$" in rule:
            rule = rule.split("$")[0]
        
        # Экранируем специальные символы
        pattern = re.escape(rule)
        
        # Заменяем wildcards
        pattern = pattern.replace("\\*", ".*")
        pattern = pattern.replace("\\^", "[^\\w\\-]")
        pattern = pattern.replace("\\|\\|", "(?:^|://|\\.)")
        
        # Начало и конец строки
        if self.type == "start":
            pattern = f"^{pattern}"
        elif self.type == "end":
            pattern = f"{pattern}$"
        elif self.type == "domain":
            pattern = f"(?:^|://|\\.){pattern}$"
        
        return re.compile(pattern, re.IGNORECASE)
    
    def parse_options(self, rule: str) -> Dict:
        """Парсинг опций правила"""
        options = {}
        if "$" in rule:
            opts = rule.split("$")[1]
            for opt in opts.split(","):
                if "=" in opt:
                    key, value = opt.split("=", 1)
                    options[key] = value
                else:
                    options[opt] = True
        return options
    
    def calculate_priority(self) -> int:
        """Расчет приоритета правила"""
        priority = 0
        
        # Доменные правила имеют более высокий приоритет
        if self.type == "domain":
            priority += 10
        
        # Правила с опциями
        if self.options:
            priority += 5
        
        # Длина правила (чем длиннее, тем точнее)
        priority += min(len(self.raw) // 10, 5)
        
        return priority
    
    def matches(self, url: str) -> bool:
        """Проверка соответствия правила URL"""
        # Проверка опций
        if self.options:
            # Проверка домена
            if "domain" in self.options:
                domains = self.options["domain"].split("|")
                parsed = urlparse(url)
                host = parsed.netloc
                if not any(host.endswith(d) for d in domains):
                    return False
            
            # Проверка типа ресурса
            if "script" in self.options:
                # Пропускаем только скрипты
                pass
            if "image" in self.options:
                # Пропускаем только изображения
                pass
            if "stylesheet" in self.options:
                # Пропускаем только CSS
                pass
        
        # Проверка основного паттерна
        return bool(self.pattern.search(url))

class AdBlockManager:
    """Менеджер блокировки рекламы"""
    
    # Списки фильтров
    FILTER_LISTS = {
        "easylist": "https://easylist.to/easylist/easylist.txt",
        "easyprivacy": "https://easylist.to/easylist/easyprivacy.txt",
        "ruadlist": "https://easylist.to/easylist/ruadlist.txt",
        "adguard": "https://filters.adtidy.org/extension/chromium/filters/2.txt"
    }
    
    def __init__(self):
        self.rules: List[AdBlockRule] = []
        self.enabled = True
        self.whitelist: List[str] = []
        self.custom_rules: List[str] = []
        self.stats = {
            "blocked_count": 0,
            "processed_count": 0,
            "last_update": None
        }
        self.updating = False
        self.update_interval = timedelta(hours=24)
        
        # Загрузка правил
        self.load_rules()
        self.load_custom_rules()
        self.load_whitelist()
        self.load_stats()
        
        # Автообновление
        self.check_update()
    
    def load_rules(self):
        """Загрузка правил из файла"""
        try:
            with open("adblock_rules.json", "r", encoding="utf-8") as f:
                rules_data = json.load(f)
                self.rules = [AdBlockRule(r) for r in rules_data]
                print(f"Загружено {len(self.rules)} правил")
        except FileNotFoundError:
            self.rules = []
        except Exception as e:
            print(f"Ошибка загрузки правил: {e}")
    
    def save_rules(self):
        """Сохранение правил"""
        try:
            rules_data = [r.raw for r in self.rules]
            with open("adblock_rules.json", "w", encoding="utf-8") as f:
                json.dump(rules_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения правил: {e}")
    
    def load_custom_rules(self):
        """Загрузка пользовательских правил"""
        try:
            with open("custom_adblock.txt", "r", encoding="utf-8") as f:
                self.custom_rules = [line.strip() for line in f if line.strip()]
            self.update_rules()
        except FileNotFoundError:
            self.custom_rules = []
        except Exception as e:
            print(f"Ошибка загрузки пользовательских правил: {e}")
    
    def load_whitelist(self):
        """Загрузка белого списка"""
        try:
            with open("adblock_whitelist.txt", "r", encoding="utf-8") as f:
                self.whitelist = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.whitelist = []
        except Exception as e:
            print(f"Ошибка загрузки белого списка: {e}")
    
    def load_stats(self):
        """Загрузка статистики"""
        try:
            with open("adblock_stats.json", "r", encoding="utf-8") as f:
                self.stats = json.load(f)
        except FileNotFoundError:
            self.stats = {
                "blocked_count": 0,
                "processed_count": 0,
                "last_update": None
            }
        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")
    
    def save_stats(self):
        """Сохранение статистики"""
        try:
            with open("adblock_stats.json", "w", encoding="utf-8") as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения статистики: {e}")
    
    def update_rules(self):
        """Обновление правил из файлов"""
        all_rules = []
        
        # Загрузка из файла
        try:
            with open("adblock_rules.json", "r", encoding="utf-8") as f:
                rules_data = json.load(f)
                all_rules.extend(rules_data)
        except:
            pass
        
        # Добавление пользовательских правил
        all_rules.extend(self.custom_rules)
        
        # Компиляция правил
        self.rules = [AdBlockRule(r) for r in set(all_rules)]
        self.rules.sort(key=lambda x: x.priority, reverse=True)
        
        print(f"Обновлено {len(self.rules)} правил")
        self.save_rules()
    
    def add_custom_rule(self, rule: str):
        """Добавление пользовательского правила"""
        if rule not in self.custom_rules:
            self.custom_rules.append(rule)
            self.save_custom_rules()
            self.update_rules()
            return True
        return False
    
    def remove_custom_rule(self, rule: str):
        """Удаление пользовательского правила"""
        if rule in self.custom_rules:
            self.custom_rules.remove(rule)
            self.save_custom_rules()
            self.update_rules()
            return True
        return False
    
    def save_custom_rules(self):
        """Сохранение пользовательских правил"""
        try:
            with open("custom_adblock.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(self.custom_rules))
        except Exception as e:
            print(f"Ошибка сохранения пользовательских правил: {e}")
    
    def add_to_whitelist(self, url: str):
        """Добавление URL в белый список"""
        if url not in self.whitelist:
            self.whitelist.append(url)
            self.save_whitelist()
            return True
        return False
    
    def remove_from_whitelist(self, url: str):
        """Удаление из белого списка"""
        if url in self.whitelist:
            self.whitelist.remove(url)
            self.save_whitelist()
            return True
        return False
    
    def save_whitelist(self):
        """Сохранение белого списка"""
        try:
            with open("adblock_whitelist.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(self.whitelist))
        except Exception as e:
            print(f"Ошибка сохранения белого списка: {e}")
    
    def should_block(self, url: str) -> bool:
        """Проверка, должен ли быть заблокирован URL"""
        if not self.enabled:
            return False
        
        # Проверка белого списка
        for pattern in self.whitelist:
            if pattern in url:
                return False
        
        # Проверка правил
        self.stats["processed_count"] += 1
        for rule in self.rules:
            if rule.matches(url):
                self.stats["blocked_count"] += 1
                self.save_stats()
                return True
        
        return False
    
    def update_filters(self, force=False):
        """Обновление фильтров из интернета"""
        if self.updating:
            return
        
        # Проверка необходимости обновления
        if not force:
            if self.stats.get("last_update"):
                last_update = datetime.fromisoformat(self.stats["last_update"])
                if datetime.now() - last_update < self.update_interval:
                    return
        
        self.updating = True
        print("Начинаем обновление фильтров...")
        
        all_rules = []
        
        for name, url in self.FILTER_LISTS.items():
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    lines = response.text.splitlines()
                    for line in lines:
                        line = line.strip()
                        # Пропускаем комментарии и пустые строки
                        if line and not line.startswith(("!", "[", "#")):
                            all_rules.append(line)
                    print(f"Загружено {len(lines)} правил из {name}")
                else:
                    print(f"Ошибка загрузки {name}: статус {response.status_code}")
            except Exception as e:
                print(f"Ошибка загрузки {name}: {e}")
        
        if all_rules:
            # Сохраняем правила
            try:
                with open("adblock_rules.json", "w", encoding="utf-8") as f:
                    json.dump(list(set(all_rules)), f, ensure_ascii=False, indent=2)
                
                # Обновляем правила в памяти
                self.update_rules()
                
                # Обновляем статистику
                self.stats["last_update"] = datetime.now().isoformat()
                self.save_stats()
                print(f"Фильтры обновлены! Всего правил: {len(self.rules)}")
            except Exception as e:
                print(f"Ошибка сохранения фильтров: {e}")
        
        self.updating = False
    
    def check_update(self):
        """Проверка необходимости обновления"""
        self.update_filters(force=False)
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        return {
            "rules_count": len(self.rules),
            "custom_rules": len(self.custom_rules),
            "whitelist_count": len(self.whitelist),
            "blocked_count": self.stats["blocked_count"],
            "processed_count": self.stats["processed_count"],
            "block_rate": (
                (self.stats["blocked_count"] / self.stats["processed_count"] * 100)
                if self.stats["processed_count"] > 0 else 0
            ),
            "last_update": self.stats.get("last_update"),
            "enabled": self.enabled
        }
    
    def enable(self):
        """Включение блокировщика"""
        self.enabled = True
        print("AdBlock включен")
    
    def disable(self):
        """Отключение блокировщика"""
        self.enabled = False
        print("AdBlock отключен")
    
    def toggle(self):
        """Переключение состояния"""
        self.enabled = not self.enabled
        print(f"AdBlock {'включен' if self.enabled else 'отключен'}")