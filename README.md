# Биматричная игра с графическим интерфейсом

## Описание проекта
Этот проект представляет собой приложение с графическим интерфейсом (GUI) на PyQt6 для работы с биматричными играми. Включает авторизацию, работу с базой данных SQLite, обработку игровых матриц и вычисление стратегий.

## Установка и запуск
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите приложение:
   ```bash
   python app.py
   ```

## Структура проекта

### 1. `app.py`
Главный файл приложения, запускает окно авторизации.

### 2. `Functions.py`
Модуль с основными функциями работы с биматричными играми:
- `remove_dominated_strategies(matrix, weak=True)`: Удаляет доминируемые стратегии.
- `save_csv_to_db(username, csv_data)`: Сохраняет CSV-файл в базу данных.
- `parse_bimatrix(matrix)`: Разбирает строковые значения в числовые массивы.
- `minimax_bimatrix(matrix)`: Рассчитывает минимаксные стратегии.
- `nash_equilibria(matrix)`: Находит равновесия Нэша.

### 3. `database.py`
Модуль работы с базой данных SQLite:
- `get_db_connection()`: Создает подключение и таблицу `users` при необходимости.

### 4. `auth.py`
Функции для авторизации:
- `register_user(username, password)`: Регистрация пользователя.
- `validate_user(username, password)`: Проверка логина и пароля.

### 5. `login_window.py`
GUI-окно авторизации с вводом логина и пароля. Позволяет зарегистрироваться или войти.

### 6. `main_window.py`
Основное окно приложения для работы с биматричными играми. Возможности:
- Выбор размера матрицы.
- Генерация случайных значений.
- Поиск минимакса и равновесий Нэша.
- Удаление доминируемых стратегий.
- Сохранение и загрузка данных из БД.

### 7. `utils.py`
Вспомогательные функции:
- `hash_password(password)`: Хеширование паролей.

## Логирование
Для логирования событий можно использовать модуль `logging`. Пример добавления логирования в `auth.py`:
```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Пользователь зарегистрирован: %s", username)
```

## TODO
- Улучшить UI/UX.
- Добавить графическое представление стратегий.
- Подключить возможность онлайн-игры.

## Авторы
Разработчик: Я

