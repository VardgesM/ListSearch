# 🔍 List.am Scraper (ListSearch)

A powerful web-based scraper for the Armenian classifieds website **list.am**. It features Cloudflare protection bypass, automatic keyword translation for a broader search, real-time UI updates, and optional Telegram notifications.

[🇷🇺 Читать на русском](#-русская-версия)

## ✨ Features

* **User-Friendly Web Interface**: Clean and responsive UI built with HTML/CSS/JS, served by FastAPI.
* **Cloudflare Bypass**: Uses `curl_cffi` to mimic a real Chrome browser, effectively bypassing anti-bot protections.
* **Smart Multi-Language Search**: Automatically translates your search keyword into Russian, English, and Armenian (using `deep_translator`) to maximize search results.
* **Real-Time Updates**: Watch scraped items appear live on the web interface using Server-Sent Events (SSE).
* **Advanced Filtering**: Filter results by a maximum price and select your preferred currency (AMD or USD).
* **Telegram Notifications**: Get instant alerts with links and prices sent directly to your Telegram bot.
* **CSV Export**: All found items are automatically saved to a `list_results.csv` file for easy access.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Scraping:** `curl_cffi` (HTTP requests), BeautifulSoup4 (HTML parsing)
* **Translation:** `deep_translator`
* **Frontend:** HTML, CSS, Vanilla JavaScript (SSE for live updates)

## 🚀 Installation & Setup

1. Clone this repository to your local machine.
2. Install the required Python dependencies:
   ```bash
   pip install fastapi uvicorn curl_cffi beautifulsoup4 deep_translator
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Open your web browser and navigate to: `http://localhost:8000`

## ⚙️ How to Use

1. Enter a **Keyword** (e.g., "macbook" or "монитор").
2. Select the **Currency** (AMD or USD) and specify the **Maximum Price**.
3. Set the **Number of Pages** to scrape per translated keyword.
4. *(Optional)* Enter your Telegram **Bot Token** and **Chat ID** to receive live alerts.
5. Click **Start Scraper** and view the results grouped by keywords in real-time!

   ---

## ⚠️ Legal Notice and Disclaimer

This project (**ListSearch**) and all of its source code are provided strictly for **educational and research purposes**.

1. **User Responsibility:** The user assumes full responsibility for the use of this software. By running this script, you automatically agree that the author of this project bears absolutely no responsibility for:
   * Any direct or indirect damages resulting from the use of this code.
   * Bans or blocks of your IP addresses, accounts, or devices by target web resources.
   * Any legal claims, disputes, or consequences caused by the improper or illegal use of this tool.

2. **Terms of Service (ToS) Compliance:** Web scraping may violate the Terms of Service of certain websites. The user is obligated to independently review the terms and conditions of *list.am* (or any other target website) and ensure that their actions do not contradict these rules, as well as local and international laws.

3. **No Warranties ("AS IS"):** The software is provided on an "AS IS" basis, without warranties of any kind, express or implied. The author does not guarantee the uninterrupted operation of the script, its continuous maintenance, or its fitness for any commercial or specific purposes.

By using this tool, you confirm that you are acting at your own risk and commit to not using it for DDoS attacks, spamming, theft of confidential data, or any other malicious or illegal activities.

---

## 🇷🇺 Русская версия

Мощный веб-парсер для армянской доски объявлений **list.am**. Приложение включает обход защиты Cloudflare, автоматический перевод ключевых слов для расширенного поиска, отображение результатов в реальном времени и интеграцию с Telegram для уведомлений.

## ✨ Ключевые особенности

* **Удобный веб-интерфейс**: Интуитивно понятный UI, работающий на базе FastAPI.
* **Обход Cloudflare**: Использование библиотеки `curl_cffi` для имитации реального браузера (Chrome) и успешного обхода защиты от ботов.
* **Мультиязычный поиск**: Автоматический перевод вашего поискового запроса на русский, английский и армянский языки (с помощью `deep_translator`) для максимального охвата объявлений.
* **Live-режим**: Результаты поиска и логи появляются на экране в режиме реального времени благодаря технологии Server-Sent Events (SSE).
* **Гибкие фильтры**: Возможность задать максимальную цену и выбрать подходящую валюту (AMD или USD).
* **Уведомления в Telegram**: Мгновенные оповещения о найденных товарах с прямыми ссылками прямо в ваш Telegram.
* **Экспорт в CSV**: Все найденные подходящие объявления автоматически сохраняются в файл `list_results.csv`.

## 🛠️ Технологии

* **Бэкенд:** Python, FastAPI, Uvicorn
* **Парсинг:** `curl_cffi` (HTTP-запросы), BeautifulSoup4 (парсинг HTML)
* **Перевод:** `deep_translator`
* **Фронтенд:** HTML, CSS, Vanilla JavaScript

## 🚀 Установка и запуск

1. Склонируйте репозиторий на свой компьютер.
2. Установите необходимые зависимости:
   ```bash
   pip install fastapi uvicorn curl_cffi beautifulsoup4 deep_translator
   ```
3. Запустите приложение:
   ```bash
   python main.py
   ```
4. Откройте браузер и перейдите по адресу: `http://localhost:8000`

## ⚙️ Использование

1. Введите **Ключевое слово** (например, "macbook" или "монитор").
2. Выберите **Валюту** (AMD или USD) и укажите **Максимальную цену**.
3. Задайте **Количество страниц** для обхода (для каждого языка перевода).
4. *(Опционально)* Укажите **Bot Token** и **Chat ID** для получения уведомлений в Telegram.
5. Нажмите **Запустить парсер** и следите за результатами в реальном времени!

---

## ⚠️ Правовое уведомление и Отказ от ответственности (Disclaimer)

Данный проект (**ListSearch**) и весь исходный код предоставляются исключительно в **образовательных и исследовательских целях**.

1. **Ответственность пользователя:** Пользователь берет на себя полную ответственность за использование данного программного обеспечения. Запуская этот скрипт, вы автоматически соглашаетесь с тем, что автор проекта не несет абсолютно никакой ответственности за:
   * Любые прямые или косвенные убытки, возникшие в результате использования кода.
   * Блокировки ваших IP-адресов, аккаунтов или устройств со стороны целевых веб-ресурсов.
   * Любые юридические претензии или последствия, вызванные неправомерным использованием инструмента.

2. **Соблюдение правил (ToS):** Веб-скрапинг (парсинг) может нарушать Условия использования (Terms of Service) некоторых веб-сайтов. Пользователь обязан самостоятельно ознакомиться с правилами сайта *list.am* (или любого другого целевого ресурса) и убедиться, что его действия не противоречат этим правилам, а также местному и международному законодательству.

3. **Отсутствие гарантий («КАК ЕСТЬ»):** Программное обеспечение предоставляется по принципу «КАК ЕСТЬ» (AS IS), без каких-либо явных или подразумеваемых гарантий. Автор не гарантирует бесперебойную работу скрипта, его актуальность или пригодность для каких-либо коммерческих или иных специфических целей.

Используя этот инструмент, вы подтверждаете, что действуете на свой страх и риск и обязуетесь не использовать его для DDoS-атак, спама, кражи конфиденциальных данных или любых других незаконных действий.
