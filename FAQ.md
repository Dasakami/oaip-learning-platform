# FAQ - Часто задаваемые вопросы

## Установка и запуск

### Q: Не могу запустить проект, что делать?

**A:** Проверьте следующее:

1. Установлен ли Docker?
```bash
docker --version  # Должна быть версия 20.0+
docker-compose --version
```

2. Запущен ли Docker?
```bash
# Linux/Mac
sudo systemctl status docker

# Windows - проверьте Docker Desktop
```

3. Свободны ли порты 8000 и 5173?
```bash
# Linux/Mac
lsof -i :8000
lsof -i :5173

# Windows
netstat -ano | findstr :8000
```

### Q: Порты 8000/5173 заняты, как изменить?

**A:** Отредактируйте `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Внешний:Внутренний
  frontend:
    ports:
      - "5174:5173"
```

### Q: Ошибка "Cannot connect to Docker daemon"

**A:** Docker не запущен:
```bash
# Linux
sudo systemctl start docker

# Mac/Windows
# Запустите Docker Desktop
```

## Работа с базой данных

### Q: Как посмотреть содержимое базы данных?

**A:** Используйте sqlite3:
```bash
# Войти в контейнер
docker exec -it oaip-backend bash

# Открыть БД
sqlite3 oaip_learning.db

# Команды SQLite
.tables                    # Показать таблицы
SELECT * FROM users;       # Показать пользователей
SELECT * FROM modules;     # Показать модули
.exit                      # Выйти
```

### Q: Как сбросить базу данных?

**A:** 
```bash
docker-compose down
rm backend/oaip_learning.db
docker-compose up -d --build
docker exec oaip-backend python seed_data.py
```

### Q: База не создается автоматически

**A:** Проверьте:
1. Права доступа на папку `backend/`
2. Переменные окружения в `.env`
3. Логи: `docker logs oaip-backend`

## Аутентификация

### Q: Забыл пароль, как восстановить?

**A:** Сейчас нет функции восстановления. Можно:

1. Зарегистрировать новый аккаунт
2. Или изменить пароль в БД:
```bash
docker exec -it oaip-backend python -c "
from app.utils.security import get_password_hash
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username=='your_username').first()
user.hashed_password = get_password_hash('new_password')
db.commit()
print('Password changed!')
"
```

### Q: Токен истекает слишком быстро

**A:** Измените в `backend/app/config.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 часа
```

### Q: Как работает аутентификация?

**A:** JWT токены:
1. Пользователь входит → получает токен
2. Токен сохраняется в localStorage
3. Каждый запрос отправляет токен в заголовке
4. Backend проверяет токен

## Модули и задания

### Q: Как добавить новый модуль?

**A:** См. [ADDING_MODULES.md](ADDING_MODULES.md). Кратко:

1. Отредактируйте `backend/seed_data.py`
2. Добавьте модуль и задания
3. Запустите: `docker exec oaip-backend python seed_data.py`

### Q: Можно ли добавлять модули через UI?

**A:** Нет, только через API или seed скрипт. Можно добавить админ-панель позже.

### Q: Поддерживаются ли другие языки программирования кроме Python?

**A:** Нет, только Python. Для поддержки других языков нужно:
1. Добавить компиляторы в Docker
2. Модифицировать `code_checker.py`
3. Настроить безопасное выполнение

### Q: Как работает проверка кода?

**A:** 
1. Код отправляется на сервер
2. Проверяется синтаксис
3. Запускаются тест-кейсы
4. Сравнивается вывод с ожидаемым
5. Результат возвращается клиенту

## Редактор кода

### Q: Monaco Editor не загружается

**A:** Проверьте:
```bash
# Логи frontend
docker logs oaip-frontend

# Пересоберите
docker-compose down
docker-compose up -d --build frontend
```

### Q: Как изменить тему редактора?

**A:** В `frontend/src/pages/TaskView.jsx`:
```javascript
<Editor
  theme="vs-dark"  // или "vs-light", "hc-black"
  // ...
/>
```

### Q: Можно ли добавить автосохранение кода?

**A:** Да, добавьте в `TaskView.jsx`:
```javascript
useEffect(() => {
  const timer = setTimeout(() => {
    localStorage.setItem(`task_${taskId}_code`, code);
  }, 1000);
  return () => clearTimeout(timer);
}, [code, taskId]);
```

## Производительность

### Q: Приложение работает медленно

**A:** Возможные причины:

1. **Мало ресурсов Docker**
```bash
# Увеличьте в Docker Desktop:
# Settings → Resources → Memory: 4GB+
```

2. **Много логов**
```bash
docker-compose logs --tail=100  # Ограничить вывод
```

3. **База данных большая**
```bash
# Очистите старые записи прогресса
```

### Q: Как ускорить запуск контейнеров?

**A:**
- Используйте Docker build cache
- Не пересобирайте без необходимости
- Используйте `.dockerignore`

## Безопасность

### Q: Безопасно ли выполнять пользовательский код?

**A:** Частично:
- Код выполняется в Docker контейнере (изоляция)
- Есть ограничение по времени выполнения
- НО: нет песочницы для Python

**Для production рекомендуется:**
- Использовать Docker в Docker
- Ограничить ресурсы (CPU, память)
- Добавить timeout на выполнение
- Использовать изолированные контейнеры

### Q: Можно ли использовать в production?

**A:** Текущая версия для разработки/обучения. Для production нужно:

1. ✅ Изменить SECRET_KEY
2. ✅ Использовать PostgreSQL вместо SQLite
3. ✅ Добавить HTTPS
4. ✅ Настроить backup БД
5. ✅ Улучшить изоляцию выполнения кода
6. ✅ Добавить rate limiting
7. ✅ Настроить мониторинг

### Q: Пароли хранятся в открытом виде?

**A:** Нет, используется bcrypt хэширование. Пароли нельзя восстановить, только сбросить.

## Разработка

### Q: Как разрабатывать без Docker?

**A:**

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Q: Hot reload не работает

**A:** Убедитесь что volumes настроены в `docker-compose.yml`:
```yaml
volumes:
  - ./backend:/app
  - ./frontend:/app
  - /app/node_modules  # Важно для frontend
```

### Q: Как добавить новый API endpoint?

**A:**

1. Создайте роутер в `backend/app/api/`:
```python
# my_router.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-endpoint")
def my_endpoint():
    return {"message": "Hello"}
```

2. Подключите в `main.py`:
```python
from app.api import my_router
app.include_router(my_router.router, prefix="/api/my", tags=["My"])
```

### Q: Как добавить новую страницу в React?

**A:**

1. Создайте компонент в `frontend/src/pages/`:
```javascript
// MyPage.jsx
function MyPage() {
  return <div>My Page</div>;
}
export default MyPage;
```

2. Добавьте роут в `App.jsx`:
```javascript
<Route path="/my-page" element={<MyPage />} />
```

## Тестирование

### Q: Как запустить тесты?

**A:**

**Backend:**
```bash
docker exec oaip-backend pytest
```

**Frontend:**
```bash
docker exec oaip-frontend npm test
```

### Q: Есть ли готовые тесты?

**A:** Нет, нужно написать. Примеры:

```python
# backend/tests/test_auth.py
def test_register():
    response = client.post("/api/auth/register", json={
        "username": "test",
        "email": "test@test.com",
        "password": "test123"
    })
    assert response.status_code == 200
```

## Деплой

### Q: Как задеплоить на сервер?

**A:**

1. **На VPS с Docker:**
```bash
# На сервере
git clone <repo>
cd oaip-learning-platform
docker-compose up -d --build
```

2. **С Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5173;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

3. **Environment variables:**
Создайте `.env` с production настройками

### Q: Как настроить домен?

**A:**
1. Купите домен
2. Настройте DNS A-record на IP сервера
3. Настройте Nginx/Caddy
4. Добавьте SSL (Let's Encrypt)

## Резервное копирование

### Q: Как сделать backup?

**A:**

**База данных:**
```bash
docker cp oaip-backend:/app/oaip_learning.db ./backup_$(date +%Y%m%d).db
```

**Весь проект:**
```bash
tar -czf backup.tar.gz oaip-learning-platform/
```

**Автоматический backup (cron):**
```bash
# Добавить в crontab
0 2 * * * docker cp oaip-backend:/app/oaip_learning.db /backups/db_$(date +\%Y\%m\%d).db
```

### Q: Как восстановить backup?

**A:**
```bash
docker-compose down
cp backup_20240115.db backend/oaip_learning.db
docker-compose up -d
```

## Производительность и масштабирование

### Q: Сколько пользователей может поддерживать?

**A:** С текущей архитектурой (SQLite):
- **Одновременно:** ~50-100 пользователей
- **Всего:** неограниченно

Для большего нужно:
- PostgreSQL
- Redis для кеша
- Load balancer
- Несколько инстансов backend

### Q: Как добавить кеширование?

**A:** Используйте Redis:

```python
# backend
import redis
r = redis.Redis(host='redis', port=6379)

@router.get("/modules/")
def get_modules():
    cached = r.get('modules')
    if cached:
        return json.loads(cached)
    # ... fetch from DB
    r.setex('modules', 3600, json.dumps(result))
```

## Известные проблемы

### Q: Monaco Editor иногда не загружается

**A:** Временное решение - перезагрузите страницу

### Q: Тесты не всегда проходят с правильным кодом

**A:** Проблема с `\n` и пробелами. Используйте `.strip()` при сравнении

### Q: После обновления Docker образа настройки сбрасываются

**A:** Используйте volumes для персистентности:
```yaml
volumes:
  - db_data:/app/data
```

---

## Не нашли ответ?

1. Проверьте [README.md](README.md)
2. Посмотрите [API_EXAMPLES.md](API_EXAMPLES.md)
3. Прочитайте [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
4. Создайте issue на GitHub
5. Проверьте логи: `docker-compose logs`