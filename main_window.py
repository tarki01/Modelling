from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, \
    QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import csv
import random
from io import StringIO
import database as db
from Functions import remove_dominated_strategies, save_csv_to_db, minimax_bimatrix, nash_equilibria

# Класс главного окна приложения
class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Работа с биматричной игрой")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon('gm.png'))

        layout = QVBoxLayout()

        self.label_matrix = QLabel("Выберите размер матрицы для игры:")
        layout.addWidget(self.label_matrix)

        # Контейнер для кнопок размерности матрицы
        size_layout = QHBoxLayout()

        # Кнопки для выбора размера матрицы
        sizes = ["1x1", "2x2", "3x3", "4x4", "5x5", "6x6"]
        self.size_buttons = []
        for size in sizes:
            button = QPushButton(size)
            button.clicked.connect(self.create_size_button_handler(size))
            self.size_buttons.append(button)
            size_layout.addWidget(button)

        layout.addLayout(size_layout)

        # Контейнер для таблицы с выравниванием по центру
        table_layout = QVBoxLayout()  # Используем VBoxLayout для выравнивания по вертикали
        table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравниваем по центру

        # Таблица для биматричных данных
        self.matrix_table = QTableWidget(3, 3)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.matrix_table)
        scroll_area.setWidgetResizable(True)
        table_layout.addWidget(scroll_area)

        layout.addLayout(table_layout)  # Добавляем таблицу в основной макет

        self.minimax_button = QPushButton("Рассчитать минимакс")
        self.minimax_button.clicked.connect(self.calculate_minimax)
        layout.addWidget(self.minimax_button)
        
        self.nash_button = QPushButton("Найти равновесие Нэша")
        self.nash_button.clicked.connect(self.calculate_nash)
        layout.addWidget(self.nash_button)
        
        # Кнопка для удаления слабо доминируемых стратегий
        self.remove_weak_button = QPushButton("Удалить слабо доминируемые стратегии")
        self.remove_weak_button.clicked.connect(self.remove_weak_dominated_strategies)
        layout.addWidget(self.remove_weak_button)

        # Кнопка для удаления строго доминируемых стратегий
        self.remove_strict_button = QPushButton("Удалить строго доминируемые стратегии")
        self.remove_strict_button.clicked.connect(self.remove_strict_dominated_strategies)
        layout.addWidget(self.remove_strict_button)
        
        self.generate_button = QPushButton("Генерировать значения")
        self.generate_button.clicked.connect(self.generate_matrix_values)
        layout.addWidget(self.generate_button)

        self.save_button = QPushButton("Сохранить в CSV")
        self.save_button.clicked.connect(self.save_to_db)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Загрузить последнюю сохраненную матрицу")
        self.load_button.clicked.connect(self.load_from_db)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def create_size_button_handler(self, size_str):
        def handler():
            size = int(size_str[0])  # Получаем размер из строки, например "3x3" -> 3
            self.matrix_table.setRowCount(size)
            self.matrix_table.setColumnCount(size)
        return handler

    def generate_matrix_values(self):
        """Генерирует случайные значения для матрицы в формате (выигрыш_игрока_1;выигрыш_игрока_2)"""
        for i in range(self.matrix_table.rowCount()):
            for j in range(self.matrix_table.columnCount()):
                value_player1 = random.randint(1, 10)
                value_player2 = random.randint(1, 10)
                self.matrix_table.setItem(i, j, QTableWidgetItem(f"({value_player1};{value_player2})"))

    def remove_weak_dominated_strategies(self):
        # Получаем текущую матрицу из таблицы
        matrix = [[self.matrix_table.item(i, j).text() if self.matrix_table.item(i, j) else '(0;0)'
                for j in range(self.matrix_table.columnCount())]
                for i in range(self.matrix_table.rowCount())]

        # Вызываем функцию для удаления слабо доминируемых стратегий
        reduced_matrix1, reduced_matrix2 = remove_dominated_strategies(matrix, weak=True)

        # Определим новый размер таблицы, который соответствует уменьшенной матрице
        new_rows, new_cols = reduced_matrix1.shape

        # Обновим размеры таблицы
        self.matrix_table.setRowCount(new_rows)
        self.matrix_table.setColumnCount(new_cols)

        # Заполним таблицу обновленными значениями
        for i in range(new_rows):
            for j in range(new_cols):
                self.matrix_table.setItem(i, j, QTableWidgetItem(f"({int(reduced_matrix1[i, j])};{int(reduced_matrix2[i, j])})"))

        QMessageBox.information(self, "Удаление слабо доминируемых стратегий", "Слабо доминируемые стратегии удалены.")

    def remove_strict_dominated_strategies(self):
        # Получаем текущую матрицу из таблицы
        matrix = [[self.matrix_table.item(i, j).text() if self.matrix_table.item(i, j) else '(0;0)'
                for j in range(self.matrix_table.columnCount())]
                for i in range(self.matrix_table.rowCount())]

        # Вызываем функцию для удаления строго доминируемых стратегий
        reduced_matrix1, reduced_matrix2 = remove_dominated_strategies(matrix, weak=False)

        # Определим новый размер таблицы, который соответствует уменьшенной матрице
        new_rows, new_cols = reduced_matrix1.shape

        # Обновим размеры таблицы
        self.matrix_table.setRowCount(new_rows)
        self.matrix_table.setColumnCount(new_cols)

        # Заполним таблицу обновленными значениями
        for i in range(new_rows):
            for j in range(new_cols):
                self.matrix_table.setItem(i, j, QTableWidgetItem(f"({int(reduced_matrix1[i, j])};{int(reduced_matrix2[i, j])})"))

        QMessageBox.information(self, "Удаление строго доминируемых стратегий", "Строго доминируемые стратегии удалены.")
    
    def calculate_minimax(self):
        matrix = [[self.matrix_table.item(i, j).text() if self.matrix_table.item(i, j) else '(0;0)'
                   for j in range(self.matrix_table.columnCount())]
                  for i in range(self.matrix_table.rowCount())]

        maximin_p1, maximin_p2 = minimax_bimatrix(matrix)
        QMessageBox.information(self, "Минимакс", f"Минимакс первого игрока: {maximin_p1}\nМинимакс второго игрока: {maximin_p2}")
    
    def calculate_nash(self):
        matrix = [[self.matrix_table.item(i, j).text() if self.matrix_table.item(i, j) else '(0;0)'
                   for j in range(self.matrix_table.columnCount())]
                  for i in range(self.matrix_table.rowCount())]
        
        equilibria = nash_equilibria(matrix)
        if equilibria:
            eq_str = "\n".join([f"Стратегия A={eq[0] + 1}, B={eq[1] + 1}" for eq in equilibria])
        else:
            eq_str = "Равновесий Нэша не найдено."
        
        QMessageBox.information(self, "Равновесие Нэша", eq_str)
    
    def save_to_db(self):
        """Сохраняет биматричную матрицу в базу данных в формате CSV"""
        # Получаем данные из таблицы
        matrix = [[self.matrix_table.item(i, j).text() if self.matrix_table.item(i, j) else '0'
                   for j in range(self.matrix_table.columnCount())]
                  for i in range(self.matrix_table.rowCount())]

        # Преобразуем матрицу в CSV-строку
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        for row in matrix:
            writer.writerow(row)

        csv_data = csv_buffer.getvalue().encode()  # Преобразуем в бинарный формат

        # Сохраняем CSV в базу данных
        save_csv_to_db(self.username, csv_data)

        QMessageBox.information(self, "Сохранение", "Биматричные данные сохранены в базе данных.")

    def load_from_db(self):
        """Загружает биматричную матрицу из базы данных"""
        conn, cursor = db.get_db_connection()

        # Проверяем, есть ли данные в базе
        cursor.execute("SELECT csv_file FROM users WHERE username = ?", (self.username,))
        result = cursor.fetchone()

        if not result or not result[0]:
            QMessageBox.warning(self, "Ошибка", "Нет сохраненных данных в базе данных.")
            conn.close()
            return

        csv_data = result[0]  # Получаем бинарные данные CSV

        # Записываем временный CSV-файл
        temp_csv_path = f"{self.username}_temp.csv"
        with open(temp_csv_path, "wb") as f:
            f.write(csv_data)

        # Открываем CSV и загружаем в таблицу
        try:
            with open(temp_csv_path, "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)

                if not data:
                    QMessageBox.warning(self, "Ошибка", "Файл CSV пуст.")
                    return

                # Настроим размер таблицы
                self.matrix_table.setRowCount(len(data))
                self.matrix_table.setColumnCount(len(data[0]))

                # Заполняем таблицу данными
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.matrix_table.setItem(i, j, QTableWidgetItem(value))

            QMessageBox.information(self, "Загрузка", "Биматричные данные загружены из базы данных.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить CSV: {str(e)}")

        finally:
            conn.close()