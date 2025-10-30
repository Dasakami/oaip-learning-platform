"""
Скрипт для заполнения базы данных тестовыми данными
Запуск: python seed_data.py
"""
from app.database import SessionLocal, engine, Base
from app.models.module import Module
from app.models.task import Task

Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    if db.query(Module).first():
        print("Database already seeded!")
        return
    
    module1 = Module(
        title="Переменные и типы данных",
        description="Изучение основных типов данных в Python: числа, строки, логические значения",
        order=1,
        content="""
        <h3>Переменные</h3>
        <p>Переменная - это именованная область памяти для хранения данных.</p>
        <pre>x = 10
name = "Python"
is_valid = True</pre>
        
        <h3>Типы данных</h3>
        <ul>
        <li><strong>int</strong> - целые числа (1, 42, -10)</li>
        <li><strong>float</strong> - дробные числа (3.14, -0.5)</li>
        <li><strong>str</strong> - строки ("Hello", 'World')</li>
        <li><strong>bool</strong> - логические значения (True, False)</li>
        </ul>
        """
    )
    db.add(module1)
    db.commit()
    
    task1_1 = Task(
        module_id=module1.id,
        title="Сложение двух чисел",
        description="Напишите программу, которая складывает два целых числа и выводит результат.",
        difficulty="easy",
        starter_code="# Введите два числа и выведите их сумму\na = int(input())\nb = int(input())\n# Ваш код здесь",
        test_cases=[
            {"input": "5\n3", "expected_output": "8"},
            {"input": "10\n20", "expected_output": "30"},
            {"input": "-5\n5", "expected_output": "0"}
        ],
        order=1
    )
    
    task1_2 = Task(
        module_id=module1.id,
        title="Приветствие",
        description="Напишите программу, которая спрашивает имя пользователя и выводит приветствие.",
        difficulty="easy",
        starter_code="# Спросите имя и выведите приветствие\nname = input()\n# Ваш код здесь",
        test_cases=[
            {"input": "Иван", "expected_output": "Привет, Иван!"},
            {"input": "Мария", "expected_output": "Привет, Мария!"}
        ],
        order=2
    )
    
    db.add_all([task1_1, task1_2])
    db.commit()
    
    module2 = Module(
        title="Условные операторы",
        description="Изучение условных операторов if, elif, else для принятия решений в программе",
        order=2,
        content="""
        <h3>Оператор if</h3>
        <p>Позволяет выполнять код только при выполнении условия.</p>
        <pre>if x > 0:
    print("Положительное число")</pre>
    
        <h3>Оператор if-else</h3>
        <pre>if x > 0:
    print("Положительное")
else:
    print("Отрицательное или ноль")</pre>
    
        <h3>Оператор if-elif-else</h3>
        <pre>if x > 0:
    print("Положительное")
elif x < 0:
    print("Отрицательное")
else:
    print("Ноль")</pre>
        """
    )
    db.add(module2)
    db.commit()
    
    task2_1 = Task(
        module_id=module2.id,
        title="Проверка на четность",
        description="Напишите программу, которая проверяет, является ли число четным или нечетным.",
        difficulty="easy",
        starter_code="n = int(input())\n# Выведите 'Четное' или 'Нечетное'",
        test_cases=[
            {"input": "4", "expected_output": "Четное"},
            {"input": "7", "expected_output": "Нечетное"},
            {"input": "0", "expected_output": "Четное"}
        ],
        order=1
    )
    
    task2_2 = Task(
        module_id=module2.id,
        title="Максимум из трех чисел",
        description="Найдите и выведите максимальное из трех введенных чисел.",
        difficulty="medium",
        starter_code="a = int(input())\nb = int(input())\nc = int(input())\n# Выведите максимальное число",
        test_cases=[
            {"input": "1\n2\n3", "expected_output": "3"},
            {"input": "5\n3\n4", "expected_output": "5"},
            {"input": "10\n10\n5", "expected_output": "10"}
        ],
        order=2
    )
    
    db.add_all([task2_1, task2_2])
    db.commit()
    
    module3 = Module(
        title="Циклы",
        description="Изучение циклов for и while для повторения действий",
        order=3,
        content="""
        <h3>Цикл while</h3>
        <p>Выполняется, пока условие истинно.</p>
        <pre>i = 0
while i < 5:
    print(i)
    i += 1</pre>
    
        <h3>Цикл for</h3>
        <p>Итерация по последовательности.</p>
        <pre>for i in range(5):
    print(i)</pre>
    
        <h3>Функция range()</h3>
        <ul>
        <li>range(n) - от 0 до n-1</li>
        <li>range(start, stop) - от start до stop-1</li>
        <li>range(start, stop, step) - с шагом step</li>
        </ul>
        """
    )
    db.add(module3)
    db.commit()
    
    task3_1 = Task(
        module_id=module3.id,
        title="Сумма чисел от 1 до N",
        description="Вычислите сумму всех чисел от 1 до N включительно.",
        difficulty="easy",
        starter_code="n = int(input())\n# Вычислите и выведите сумму",
        test_cases=[
            {"input": "5", "expected_output": "15"},
            {"input": "10", "expected_output": "55"},
            {"input": "1", "expected_output": "1"}
        ],
        order=1
    )
    
    task3_2 = Task(
        module_id=module3.id,
        title="Факториал",
        description="Вычислите факториал числа N (N! = 1 * 2 * 3 * ... * N).",
        difficulty="medium",
        starter_code="n = int(input())\n# Вычислите и выведите факториал",
        test_cases=[
            {"input": "5", "expected_output": "120"},
            {"input": "3", "expected_output": "6"},
            {"input": "1", "expected_output": "1"}
        ],
        order=2
    )
    
    db.add_all([task3_1, task3_2])
    db.commit()
    
    print("Database seeded successfully!")
    print(f"Created {db.query(Module).count()} modules")
    print(f"Created {db.query(Task).count()} tasks")
    
    db.close()

if __name__ == "__main__":
    seed_database()