from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PyQt6.QtGui import QIcon
from auth import register_user, validate_user
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 200)
        self.setWindowIcon(QIcon('gm.png'))

        layout = QVBoxLayout()
        
        self.label_user = QLabel("Логин:")
        self.username_entry = QLineEdit()
        layout.addWidget(self.label_user)
        layout.addWidget(self.username_entry)
        
        self.label_pass = QLabel("Пароль:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.password_entry)
        
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)

    def login(self):
        if validate_user(self.username_entry.text(), self.password_entry.text()):
            self.close()
            self.main_window = MainWindow(self.username_entry.text())
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
    
    def register(self):
        if register_user(self.username_entry.text(), self.password_entry.text()):
            QMessageBox.information(self, "Успех", "Регистрация успешна!")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует!")
