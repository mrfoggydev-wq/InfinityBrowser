# 🌌 InfinityBrowser v4.0

**Полноценный веб-браузер с 50+ функциями на Python + PyQt5**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)]()

---

## 📖 О ПРОЕКТЕ

**InfinityBrowser** — это полноценный веб-браузер, написанный на Python
с использованием QtWebEngine (Chromium). Включает 50+ функций,
которые делают его мощным инструментом для серфинга в интернете.

> ⚠️ **Внимание:** Это демонстрационная версия. Не гарантирует
> полную безопасность и анонимность.

---

## ✨ ФУНКЦИИ

### 🌐 Навигация
- Многозадачные вкладки
- Восстановление закрытых вкладок
- **🆕 Открытие ссылок в новой вкладке** (Ctrl+Click, средняя кнопка)
- Перехват `target="_blank"` и `window.open()`

### 🛡️ Безопасность
- AdBlock (блокировка рекламы)
- SSL-индикатор (🔒/🔓)
- Менеджер разрешений сайтов
- Режим инкогнито

### 🧩 Расширения
- Установка из **ZIP**, **папки** или **JS**
- Попап-окна для расширений
- Просмотр кода расширения
- Встроенные: AdBlock, Dark Reader, Переводчик, Скриншоты

### 🛠️ Инструменты разработчика
- **F12 DevTools** как в Chrome
- Просмотр HTML
- JavaScript-консоль
- Информация о странице

### 📥 Загрузки и файлы
- Менеджер загрузок с прогрессом
- Менеджер файлов с категориями
- Скачивание в `~/Downloads/InfinityBrowser/`

### 🎨 Интерфейс
- **15+ языков** (русский, английский, украинский, немецкий, ...)
- **5 тем оформления** (Infinity, Dark, Light, Neon, Ocean)
- Тёмный режим

---

## 🚀 УСТАНОВКА

### Способ 1: Скачать .exe (для Windows)

Скачай готовый `.exe` из [Releases](https://github.com/mrfoggydev-wq/InfinityBrowser/releases)
и запусти — **никаких установок не нужно**.

### Способ 2: Запустить из исходников

```bash
# Клонировать
git clone https://github.com/mrfoggydev-wq/InfinityBrowser.git
cd InfinityBrowser

# Виртуальное окружение
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Зависимости
pip install -r requirements.txt

# Запуск
python main.py
