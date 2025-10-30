# Руководство по добавлению модулей и заданий

## Способ 1: Через seed_data.py (Рекомендуется)

### Шаг 1: Откройте файл seed_data.py

```bash
nano backend/seed_data.py
# или используйте любой редактор
```

### Шаг 2: Добавьте новый модуль

```python
# Пример: Модуль 4 - Функции
module4 = Module(
    title="Функции",
    description="Изучение функций в Python: определение, параметры, возвращаемые значения",
    order=4,  # Порядковый номер
    content="""
    <h3>Что такое функция?</h3>
    <p>Функция - это блок кода, который можно вызывать многократно.</p>
    
    <h3>Определение функции</h3>
    <pre>def my_function():
    print("Hello from function!")</pre>
    
    <h3>Функция с параметрами</h3>
    <pre>def greet(name):
    return f"Hello, {name}!"</pre>
    
    <h3>Возвращаемое значение</h3>
    <pre>def add(a, b):
    return a + b

result = add(5, 3)  # 8</pre>
    """
)
db.add(module4)
db.commit()
```

### Шаг 3: Добавьте задания к модулю

```python
# Задание 1: Простая функция
task4_1 = Task(
    module_id=module4.id,
    title="Функция приветствия",
    description="Создайте функцию greet(name), которая возвращает строку 'Привет, {name}!'",
    difficulty="easy",
    starter_code="""def greet(name):
    # Ваш код здесь
    pass

# Тестирование
print(greet(input()))""",
    test_cases=[
        {"input": "Иван", "expected_output": "Привет, Иван!"},
        {"input": "Мария", "expected_output": "Привет, Мария!"}
    ],
    order=1
)

# Задание 2: Функция с вычислениями
task4_2 = Task(
    module_id=module4.id,
    title="Площадь прямоугольника",
    description="Создайте функцию area(width, height), которая возвращает площадь прямоугольника",
    difficulty="easy",
    starter_code="""def area(width, height):
    # Ваш код здесь
    pass

# Тестирование
w = int(input())
h = int(input())
print(area(w, h))""",
    test_cases=[
        {"input": "5\n3", "expected_output": "15"},
        {"input": "10\n10", "expected_output": "100"},
        {"input": "7\n4", "expected_output": "28"}
    ],
    order=2
)

db.add_all([task4_1, task4_2])
db.commit()
```

### Шаг 4: Запустите скрипт

```bash
# Если база уже существует, удалите её сначала
docker exec oaip-backend rm -f oaip_learning.db

# Пересоздайте контейнер
docker-compose down
docker-compose up -d --build

# Запустите seed скрипт
docker exec oaip-backend python seed_data.py
```

## Способ 2: Через API (для динамического добавления)

### Создание модуля через API

```bash
# Получите токен (сначала зарегистрируйтесь и войдите)
TOKEN="your_jwt_token"

# Создайте модуль
curl -X POST "http://localhost:8000/api/modules/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Списки и массивы",
    "description": "Работа со списками в Python",
    "order": 5,
    "content": "<h3>Списки</h3><p>Упорядоченные коллекции элементов</p>"
  }'
```

### Создание задания через API

```bash
curl -X POST "http://localhost:8000/api/tasks/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module_id": 5,
    "title": "Сумма элементов списка",
    "description": "Найдите сумму всех элементов списка",
    "difficulty": "easy",
    "starter_code": "numbers = list(map(int, input().split()))\n# Ваш код",
    "test_cases": [
      {"input": "1 2 3 4 5", "expected_output": "15"},
      {"input": "10 20 30", "expected_output": "60"}
    ],
    "order": 1
  }'
```

## Структура test_cases

Тест-кейсы должны быть в формате JSON массива:

```python
test_cases = [
    {
        "input": "5\n3",           # Входные данные (через \n для новой строки)
        "expected_output": "8"      # Ожидаемый вывод
    },
    {
        "input": "10\n20",
        "expected_output": "30"
    }
]
```

## Уровни сложности

- `"easy"` - легкий (зеленый)
- `"medium"` - средний (оранжевый)
- `"hard"` - сложный (красный)

## HTML в content модуля

В поле `content` можно использовать HTML теги:

```html
<h3>Заголовок</h3>
<p>Параграф текста</p>
<pre>код в блоке</pre>
<ul>
  <li>Пункт списка 1</li>
  <li>Пункт списка 2</li>
</ul>
<strong>Жирный текст</strong>
<em>Курсив</em>
```

## Примеры готовых модулей

### Модуль: Списки

```python
Module(
    title="Списки и массивы",
    description="Работа со списками: создание, индексация, методы",
    order=5,
    content="""
    <h3>Создание списка</h3>
    <pre>my_list = [1, 2, 3, 4, 5]
empty_list = []</pre>
    
    <h3>Индексация</h3>
    <pre>first = my_list[0]    # 1
last = my_list[-1]     # 5</pre>
    
    <h3>Методы списков</h3>
    <ul>
    <li>append() - добавить элемент</li>
    <li>remove() - удалить элемент</li>
    <li>len() - длина списка</li>
    <li>sum() - сумма элементов</li>
    </ul>
    """
)
```

### Модуль: Строки

```python
Module(
    title="Работа со строками",
    description="Методы строк, форматирование, срезы",
    order=6,
    content="""
    <h3>Методы строк</h3>
    <pre>text = "Hello World"
upper = text.upper()       # "HELLO WORLD"
lower = text.lower()       # "hello world"
split = text.split()       # ["Hello", "World"]</pre>
    
    <h3>Форматирование</h3>
    <pre>name = "Alice"
age = 25
text = f"My name is {name}, I am {age}"</pre>
    """
)
```

## Проверка корректности

После добавления модуля проверьте:

1. **Модуль отображается** на главной странице
2. **Теория читаема** и правильно отформатирована
3. **Задания доступны** при клике на модуль
4. **Тесты проходят** при правильном решении
5. **Прогресс обновляется** после выполнения

## Отладка

Если модуль не появился:

```bash
# Проверьте логи backend
docker logs oaip-backend

# Проверьте содержимое БД
docker exec -it oaip-backend sqlite3 oaip_learning.db
sqlite> SELECT * FROM modules;
sqlite> .exit
```

## Рекомендации

1. **Порядок модулей** - логическая последовательность от простого к сложному
2. **Описание задания** - четкое и понятное
3. **Тест-кейсы** - покрывают разные сценарии
4. **Стартовый код** - помогает начать решение
5. **Сложность** - соответствует реальной сложности

## Полный пример добавления модуля

```python
# В конце функции seed_database() в seed_data.py

# Модуль: Словари
module_dict = Module(
    title="Словари",
    description="Работа со словарями: ключи, значения, методы",
    order=7,
    content="""<h3>Что такое словарь?</h3>
    <p>Словарь - коллекция пар ключ-значение</p>
    <pre>person = {
    "name": "Alice",
    "age": 25,
    "city": "Moscow"
}</pre>"""
)
db.add(module_dict)
db.commit()

# Задание 1
task_dict_1 = Task(
    module_id=module_dict.id,
    title="Создание словаря",
    description="Создайте словарь student с ключами name, age, grade",
    difficulty="easy",
    starter_code="""# Создайте словарь student
student = {}

# Вывод для проверки (не изменяйте)
print(student.get('name', ''))
print(student.get('age', ''))
print(student.get('grade', ''))""",
    test_cases=[
        {
            "input": "",
            "expected_output": "Alice\n20\nA"
        }
    ],
    order=1
)
db.add(task_dict_1)
db.commit()

print(f"Added module: {module_dict.title}")
```

Затем перезапустите seed скрипт!