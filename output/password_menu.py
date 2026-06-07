import random
import pyperclip as pyp
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox
from PyQt5.QtGui import QIcon
import string
import sys


"""Создание класса(окна)"""
class Window_password_generate(QWidget):
    def __init__(self):
        super().__init__()
        """Настройка"""
        self.app = QApplication(sys.argv)
        self.setWindowTitle('Генератор пароля на выбор!')
        self.setFixedSize(450,300)
        self.style_window()

        """Создание текста и настройка"""
        self.label_text = QLabel('Случайный пароль: ', self)

        self.label_answer = QLabel('   ', self)
        self.label_answer.setFixedSize(280,100)
        self.label_answer.setStyleSheet("""
        border: 5px solid;
        border-left-color: #DC143C;
        border-right-color: #DC143C;
        border-top-color: #DC143C;
        border-bottom-color: #DC143C;
        border-radius: 15px;
        font: Times New Roman;
        font-size: 30px;
        """)
        """Создание кнопок и настройка"""
        self.button_exit = QPushButton(QIcon('exit.PNG'),' Выход')
        self.button_exit.setToolTip('Нажмите для выхода')

        self.button_exit.clicked.connect(self.leave)

        self.button_generate = QPushButton(QIcon('generator.PNG'),' Сгенерировать пароль')
        self.button_generate.setToolTip('Нажмите для генерации пароля')

        self.button_generate.clicked.connect(self.generate)

        self.button_copy = QPushButton(QIcon('save.PNG'),' Скопировать и сохранить')
        self.button_copy.setToolTip('Нажмите для сохранения пароля в буфет обмена')

        self.button_copy.clicked.connect(self.save_and_copy)


        """Создание мини окошка выбора размера пароля и настройка"""
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['4','5','6','7','8','9','10','11','12'])
        self.combo_box.setFixedSize(300,30)
        self.label_size = QLabel('Длина пароля: ', self)


        """Добавление холстов на окно"""
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        hbox.addWidget(self.label_text)
        hbox.addWidget(self.label_answer)


        hbox1.addWidget(self.button_generate)
        hbox1.addWidget(self.button_copy)

        hbox2.addWidget(self.label_size)
        hbox2.addWidget(self.combo_box)


        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.button_exit)
        self.setLayout(vbox)

    """Тема окна"""
    def style_window(self):
        style = """
        QWidget {
            background-color: #00BFFF;
        }
        QLabel {
            color: black;
            font: Arial;
            font-size: 14px;
        }
        QComboBox {
            background-color: #87CEEB;
            color: black;
            font: Arial;
            font-size: 14px;
            border: 2px solid;
            border-radius: 7px;
        }
        QPushButton {
            background-color: #87CEEB;
            color: black;
            font: Arial;
            font-size: 14px;
            border: 2px solid;
            border-radius: 7px;
        }   
        QLineEdit {
            background-color: #B0E0E6;
            color: black;
            font: Arial;
            font-size: 14px;
            border: 2px solid;
            border-radius: 7px;
        }   
        QComboBox {
            color: black;
            background-color: white;
            font: Arial;
            font-size: 15px;
            border: 3px solid;
            border-left-color: #CD5C5C;
            border-right-color: #CD5C5C;
            border-top-color: #CD5C5C;
            border-bottom-color: #CD5C5C;
            border-radius: 13px;
            padding: 7px 8px;
        }
        """
        self.setStyleSheet(style)

    def leave(self):
        self.close()

    """Генерация пароля"""
    def generate(self):
        alpha = string.digits + string.ascii_lowercase + string.ascii_uppercase
        size = self.combo_box.currentText()
        random_password = ''
        for i in range(int(size)):
            piece_random_password = random.choice(alpha)
            random_password += piece_random_password
        self.label_answer.setText(f'  {random_password}')


    """Сохранение и копирование пароля"""
    def save_and_copy(self):
        if self.label_answer.text() == '     Сначало нужно\n       соглашение!':
            self.generate()
        pyp.copy(self.label_answer.text().strip())
        with open('password', 'a', encoding='utf-8') as file:
            file.write(f'Ваш пароль: {self.label_answer.text().strip()}\n')
            file.close()



def generate_v2():
    alpha = string.digits + string.ascii_lowercase + string.ascii_uppercase
    size = random.randint(4,12)
    random_password = ''
    for i in range(int(size)):
        piece_random_password = random.choice(alpha)
        random_password += piece_random_password
    pyp.copy(random_password)
    with open('password', 'a', encoding='utf-8') as file:
        file.write(f'Ваш пароль: {random_password}\n')
        file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window_password_generate()
    w.show()
    sys.exit(app.exec_())
