# API Examples - Примеры использования API

Все примеры используют `curl`. Замените `YOUR_TOKEN` на реальный JWT токен после входа.

## Аутентификация

### Регистрация нового пользователя

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student1@example.com",
    "password": "securepass123",
    "full_name": "Иван Иванов"
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "username": "student1",
  "email": "student1@example.com",
  "full_name": "Иван Иванов",
  "created_at": "2024-01-15T10:30:00"
}
```

### Вход в систему

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "securepass123"
  }'
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Сохраните `access_token` для дальнейших запросов!

### Получить информацию о текущем пользователе

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Модули

### Получить все модули с прогрессом

```bash
curl -X GET "http://localhost:8000/api/modules/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Ответ:**
```json
[
  {
    "id": 1,
    "title": "Переменные и типы данных",
    "description": "Изучение основных типов данных в Python",
    "order": 1,
    "content": "<h3>Переменные</h3>...",
    "completed_tasks": 2,
    "total_tasks": 2,
    "progress_percentage": 100.0
  },
  {
    "id": 2,
    "title": "Условные операторы",
    "description": "Изучение условных операторов if, elif, else",
    "order": 2,
    "content": "<h3>Оператор if</h3>...",
    "completed_tasks": 0,
    "total_tasks": 2,
    "progress_percentage": 0.0
  }
]
```

### Получить конкретный модуль

```bash
curl -X GET "http://localhost:8000/api/modules/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Задания

### Получить задания модуля

```bash
curl -X GET "http://localhost:8000/api/tasks/module/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Ответ:**
```json
[
  {
    "id": 1,
    "module_id": 1,
    "title": "Сложение двух чисел",
    "description": "Напишите программу, которая складывает два числа",
    "difficulty": "easy",
    "starter_code": "a = int(input())\nb = int(input())\n# Ваш код",
    "test_cases": [
      {"input": "5\n3", "expected_output": "8"}
    ],
    "order": 1,
    "completed": false,
    "attempts": 0
  }
]
```

### Получить конкретное задание

```bash
curl -X GET "http://localhost:8000/api/tasks/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Отправить решение задания

```bash
curl -X POST "http://localhost:8000/api/tasks/submit" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1,
    "code": "a = int(input())\nb = int(input())\nprint(a + b)"
  }'
```

**Успешный ответ:**
```json
{
  "success": true,
  "message": "Passed 3/3 tests",
  "test_results": [
    {
      "passed": true,
      "input": "5\n3",
      "expected": "8",
      "actual": "8",
      "error": null
    },
    {
      "passed": true,
      "input": "10\n20",
      "expected": "30",
      "actual": "30",
      "error": null
    },
    {
      "passed": true,
      "input": "-5\n5",
      "expected": "0",
      "actual": "0",
      "error": null
    }
  ]
}
```

**Ответ с ошибкой:**
```json
{
  "success": false,
  "message": "Passed 1/3 tests",
  "test_results": [
    {
      "passed": true,
      "input": "5\n3",
      "expected": "8",
      "actual": "8",
      "error": null
    },
    {
      "passed": false,
      "input": "10\n20",
      "expected": "30",
      "actual": "200",
      "error": null
    },
    {
      "passed": false,
      "input": "-5\n5",
      "expected": "0",
      "actual": "",
      "error": "NameError: name 'result' is not defined"
    }
  ]
}
```

## Прогресс

### Получить статистику прогресса

```bash
curl -X GET "http://localhost:8000/api/progress/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Ответ:**
```json
{
  "total_modules": 3,
  "completed_modules": 1,
  "total_tasks": 6,
  "completed_tasks": 2,
  "overall_progress": 33.33
}
```

## Примеры с Python requests

### Регистрация и получение токена

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Регистрация
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "student1",
        "email": "student1@example.com",
        "password": "pass123",
        "full_name": "Student One"
    }
)
print(response.json())

# Вход
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "username": "student1",
        "password": "pass123"
    }
)
token = response.json()["access_token"]
print(f"Token: {token}")

# Заголовки для авторизованных запросов
headers = {"Authorization": f"Bearer {token}"}
```

### Получить модули и решить задание

```python
# Получить модули
response = requests.get(f"{BASE_URL}/modules/", headers=headers)
modules = response.json()
print(f"Modules: {len(modules)}")

# Получить задания первого модуля
module_id = modules[0]["id"]
response = requests.get(f"{BASE_URL}/tasks/module/{module_id}", headers=headers)
tasks = response.json()
print(f"Tasks: {len(tasks)}")

# Отправить решение
task_id = tasks[0]["id"]
code = """
a = int(input())
b = int(input())
print(a + b)
"""

response = requests.post(
    f"{BASE_URL}/tasks/submit",
    headers=headers,
    json={"task_id": task_id, "code": code}
)
result = response.json()
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

### Отслеживание прогресса

```python
# Получить статистику
response = requests.get(f"{BASE_URL}/progress/stats", headers=headers)
stats = response.json()

print(f"Completed modules: {stats['completed_modules']}/{stats['total_modules']}")
print(f"Completed tasks: {stats['completed_tasks']}/{stats['total_tasks']}")
print(f"Overall progress: {stats['overall_progress']:.1f}%")
```

## JavaScript (Axios) примеры

### Настройка клиента

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Добавить токен ко всем запросам
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Регистрация и вход

```javascript
// Регистрация
async function register() {
  const response = await api.post('/auth/register', {
    username: 'student1',
    email: 'student1@example.com',
    password: 'pass123',
    full_name: 'Student One'
  });
  console.log('Registered:', response.data);
}

// Вход
async function login() {
  const response = await api.post('/auth/login', {
    username: 'student1',
    password: 'pass123'
  });
  localStorage.setItem('token', response.data.access_token);
  console.log('Logged in');
}
```

### Работа с модулями и заданиями

```javascript
// Получить модули
async function getModules() {
  const response = await api.get('/modules/');
  return response.data;
}

// Отправить решение
async function submitCode(taskId, code) {
  const response = await api.post('/tasks/submit', {
    task_id: taskId,
    code: code
  });
  return response.data;
}

// Использование
const modules = await getModules();
const result = await submitCode(1, 'print("Hello")');
console.log('Test passed:', result.success);
```

## Коды ошибок

- **200** - Успех
- **201** - Создано
- **400** - Неверный запрос
- **401** - Не авторизован
- **404** - Не найдено
- **422** - Ошибка валидации
- **500** - Ошибка сервера

## WebSocket (будущая функция)

Для real-time обновлений можно добавить WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## Полезные советы

1. **Всегда используйте токен** для защищенных эндпоинтов
2. **Обрабатывайте ошибки** - проверяйте статус коды
3. **Кэшируйте токен** - сохраняйте в localStorage/sessionStorage
4. **Используйте interceptors** - для автоматического добавления токена
5. **Логируйте запросы** - для отладки

## Тестирование API

### Swagger UI
Откройте http://localhost:8000/docs для интерактивного тестирования

### Postman Collection
Импортируйте эти примеры в Postman для удобного тестирования

### Автоматические тесты
```python
# test_api.py
import requests
import pytest

BASE_URL = "http://localhost:8000/api"

def test_register():
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
```

Запуск: `pytest test_api.py`