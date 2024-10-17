## Стек технологий
- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Управление зависимостями: Poetry

# Установка и настройка окружения

Для начала работы с проектом, пожалуйста, выполните следующие шаги:

1. Клонирование репозитория: 
   
   git clone https://github.com/KoostaPl/CineNight-Home-Cinema-.git
   cd kinopoisk

2. Создание виртуального окружения:
   
   python -m venv venv

3. Активация виртуального окружения:
   - Для Windows:
     
     venv\Scripts\activate
     
   - Для macOS/Linux:
     
     source venv/bin/activate

4. Установка зависимостей с помощью Poetry:
   Убедитесь, что у вас установлен Poetry. Если Poetry не установлен, вы можете установить его, следуя [документации Poetry](https://python-poetry.org/docs/#installation).

   Затем выполните команду для установки зависимостей:
   
   poetry install

## Запуск проекта

После установки зависимостей вы можете запустить проект с помощью следующих команд:

1. Примените миграции:
   
   python manage.py migrate
   

2. Запустите сервер:
   
   python manage.py runserver
   

3. Перейдите по адресу http://127.0.0.1:8000 в вашем браузере, чтобы увидеть приложение.

4. Для запуска скрипта для json используйте команду python manage.py import_movies.