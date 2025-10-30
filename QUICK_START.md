# Быстрый старт OAIP Learning Platform

## За 3 минуты до запуска

### 1. Установка (один раз)

```bash
# Убедитесь что установлены Docker и Docker Compose
docker --version
docker-compose --version

# Клонируйте проект
git clone <your-repo-url>
cd oaip-learning-platform
```

### 2. Запуск

```bash
# Один скрипт делает всё
chmod +x setup.sh
./setup.sh
```

**Или вручную:**

```bash
cp backend/.env.example backend/.env
docker-compose up -d --build
sleep 10
docker exec oaip-backend python seed_data.py
```

### 3. Готово!

Откройте: **http://localhost:5173**

## Первые шаги

1. **Зарегистрируйтесь** - создайте аккаунт
2. **Войдите** - используйте свои данные
3. **Выберите модуль** - начните с "Переменные и типы данных"
4. **Решайте задания** - пишите код и проверяйте

## Частые команды

```bash
# Остановить проект
docker-compose down

# Запустить снова
docker-compose up -d

# Посмотреть логи
docker logs oaip-backend
docker logs oaip-frontend

# Перезапустить с пересборкой
docker-compose down
docker-compose up -d --build

# Очистить всё и начать заново
docker-compose down -v
rm backend/oaip_learning.db
docker-compose up -d --build
docker exec oaip-backend python seed_data.py
```

## Что уже работает

✅ Регистрация и вход  
✅ 3 модуля с заданиями  
✅ Редактор кода Monaco  
✅ Автоматическая проверка  
✅ Отслеживание прогресса  
✅ Статистика достижений  

## Структура файлов (упрощенно)

```
oaip-learning-platform/
├── backend/           # Python FastAPI
│   ├── app/          # Код приложения
│   └── seed_data.py  # Заполнение БД
├── frontend/         # React приложение
│   └── src/          # Компоненты и страницы
├── docker-compose.yml
└── setup.sh
```

## Порты

- **5173** - Frontend (React)
- **8000** - Backend (FastAPI)

## API документация

**Swagger UI:** http://localhost:8000/docs  
Здесь можно тестировать все API эндпоинты

## Добавление модулей

Редактируйте: `backend/seed_data.py`

```python
# Пример добавления модуля
module_new = Module(
    title="Ваш модуль",
    description="Описание",
    order=4,
    content="<h3>HTML контент</h3>"
)
```

Затем:
```bash
docker exec oaip-backend python seed_data.py
```

## Решение проблем

### Backend не запускается
```bash
docker logs oaip-backend
docker-compose restart backend
```

### Frontend не отображается
```bash
docker logs oaip-frontend
docker-compose restart frontend
```

### База данных повреждена
```bash
docker-compose down
rm backend/oaip_learning.db
docker-compose up -d
docker exec oaip-backend python seed_data.py
```

### Порты заняты
Измените порты в `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Вместо 8000
  - "5174:5173"  # Вместо 5173
```

## Тестовые данные

После `seed_data.py` у вас есть:

**Модуль 1:** Переменные (2 задания)  
**Модуль 2:** Условия (2 задания)  
**Модуль 3:** Циклы (2 задания)

Всего: **3 модуля, 6 заданий**

## Следующие шаги

1. 📖 Прочитайте README.md - полное описание
2. 📁 Изучите PROJECT_STRUCTURE.md - архитектура
3. ➕ Читайте ADDING_MODULES.md - добавление контента
4. 🚀 Начните разработку своих модулей

## Полезные ссылки

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Разработка

### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## Технологии

**Backend:** FastAPI + SQLAlchemy + SQLite  
**Frontend:** React + Vite + Monaco Editor  
**Deploy:** Docker + Docker Compose

---

**Возникли вопросы?** Проверьте документацию или создайте issue.

**Всё работает?** Начинайте добавлять свои модули! 🎓