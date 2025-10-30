# Полная структура проекта OAIP Learning Platform

## Корневая директория
```
oaip-learning-platform/
├── backend/
├── frontend/
├── docker-compose.yml
├── .gitignore
├── setup.sh
├── README.md
└── PROJECT_STRUCTURE.md
```

## Backend структура

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Главный файл FastAPI
│   ├── config.py                  # Конфигурация (Settings)
│   ├── database.py                # Подключение к БД
│   │
│   ├── models/                    # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py               # Модель пользователя
│   │   ├── module.py             # Модель модуля обучения
│   │   ├── task.py               # Модель задания
│   │   └── progress.py           # Модель прогресса
│   │
│   ├── schemas/                   # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py               # Схемы для User
│   │   ├── module.py             # Схемы для Module
│   │   ├── task.py               # Схемы для Task
│   │   └── progress.py           # Схемы для Progress
│   │
│   ├── api/                       # API эндпоинты
│   │   ├── __init__.py
│   │   ├── auth.py               # Аутентификация
│   │   ├── modules.py            # CRUD модулей
│   │   ├── tasks.py              # CRUD заданий
│   │   └── progress.py           # Отслеживание прогресса
│   │
│   ├── services/                  # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth.py               # Сервис аутентификации
│   │   ├── code_checker.py       # Проверка кода
│   │   └── progress_tracker.py   # Отслеживание прогресса
│   │
│   └── utils/                     # Утилиты
│       ├── __init__.py
│       └── security.py           # JWT, хэширование
│
├── tests/                         # Тесты (для будущей разработки)
├── seed_data.py                  # Скрипт заполнения БД
├── requirements.txt              # Python зависимости
├── Dockerfile                    # Docker образ
├── .env.example                  # Пример .env файла
└── oaip_learning.db             # SQLite база данных (создается автоматически)
```

## Frontend структура

```
frontend/
├── src/
│   ├── pages/                    # Страницы приложения
│   │   ├── Login.jsx            # Страница входа
│   │   ├── Register.jsx         # Страница регистрации
│   │   ├── Dashboard.jsx        # Главная панель
│   │   ├── ModuleView.jsx       # Просмотр модуля
│   │   └── TaskView.jsx         # Решение задания
│   │
│   ├── services/                 # API сервисы
│   │   └── api.js               # Axios клиент и API методы
│   │
│   ├── styles/                   # CSS стили
│   │   ├── Auth.css             # Стили авторизации
│   │   ├── Dashboard.css        # Стили дашборда
│   │   ├── ModuleView.css       # Стили модуля
│   │   └── TaskView.css         # Стили задания
│   │
│   ├── App.jsx                   # Главный компонент
│   ├── main.jsx                  # Точка входа
│   └── index.css                 # Глобальные стили
│
├── public/                       # Статические файлы
├── index.html                    # HTML шаблон
├── package.json                  # Node зависимости
├── vite.config.js               # Конфигурация Vite
└── Dockerfile                    # Docker образ
```

## Ключевые файлы по назначению

### Конфигурация и развертывание
- `docker-compose.yml` - оркестрация контейнеров
- `setup.sh` - скрипт быстрого запуска
- `.gitignore` - исключения для git
- `.env.example` - шаблон переменных окружения

### Backend ключевые файлы
- `app/main.py` - инициализация FastAPI, подключение роутеров
- `app/database.py` - настройка SQLAlchemy
- `app/services/code_checker.py` - ядро проверки кода
- `seed_data.py` - инициализация БД с тестовыми данными

### Frontend ключевые файлы
- `App.jsx` - роутинг и управление аутентификацией
- `services/api.js` - централизованный API клиент
- `pages/TaskView.jsx` - редактор кода с Monaco

## База данных (SQLite)

### Таблицы
1. **users** - пользователи системы
   - id, username, email, hashed_password, full_name, created_at

2. **modules** - учебные модули
   - id, title, description, order, content

3. **tasks** - практические задания
   - id, module_id, title, description, difficulty, starter_code, test_cases, order

4. **progress** - прогресс пользователей
   - id, user_id, task_id, completed, code_submitted, completed_at, attempts

## API Endpoints

### Authentication (`/api/auth`)
- POST `/register` - регистрация
- POST `/login` - вход
- GET `/me` - текущий пользователь

### Modules (`/api/modules`)
- GET `/` - список модулей с прогрессом
- GET `/{id}` - конкретный модуль

### Tasks (`/api/tasks`)
- GET `/module/{module_id}` - задания модуля
- GET `/{id}` - конкретное задание
- POST `/submit` - отправка решения

### Progress (`/api/progress`)
- GET `/stats` - статистика прогресса

## Технологический стек

### Backend
- **FastAPI** 0.104.1 - веб-фреймворк
- **SQLAlchemy** 2.0.23 - ORM
- **Pydantic** 2.5.0 - валидация данных
- **python-jose** 3.3.0 - JWT токены
- **passlib** 1.7.4 - хэширование паролей

### Frontend
- **React** 18.2.0 - UI библиотека
- **Vite** 5.0.8 - сборщик
- **React Router** 6.20.0 - маршрутизация
- **Monaco Editor** 4.6.0 - редактор кода
- **Axios** 1.6.2 - HTTP клиент
- **Lucide React** 0.263.1 - иконки

### Инфраструктура
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **SQLite** - база данных

## Процесс работы

1. **Пользователь регистрируется** → сохраняется в таблицу users
2. **Входит в систему** → получает JWT токен
3. **Просматривает модули** → загружаются из БД с прогрессом
4. **Выбирает модуль** → видит теорию и задания
5. **Решает задание** → пишет код в Monaco Editor
6. **Отправляет решение** → код проверяется на сервере
7. **Получает результат** → видит какие тесты прошли
8. **Прогресс сохраняется** → обновляется таблица progress

## Безопасность

- JWT токены для аутентификации
- Bcrypt для хэширования паролей
- CORS настроен для фронтенда
- Изолированное выполнение кода пользователя
- Валидация данных через Pydantic

## Возможности расширения

1. Добавить больше модулей и заданий
2. Реализовать рейтинг пользователей
3. Добавить комментарии к заданиям
4. Реализовать систему подсказок
5. Добавить экспорт прогресса
6. Интегрировать с GitHub
7. Добавить видеоуроки
8. Реализовать форум обсуждений