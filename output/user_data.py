import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import sqlite3
import voice


connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

nums = '1234567890'
en = 'abcdefghijklmnopqrstuvwxyz'


conn = sqlite3.connect("user_info.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
    age INTEGER,
    mass INTEGER,
    height INTEGER,
    hobby TEXT,
    city TEXT
    )
""")

class User:
    def __init__(self, age, mass, height, hobby, city):
        self.age = age
        self.height = height
        self.mass = mass
        self.hobby = hobby
        self.city = city
    def add_info(self):
        cursor.execute("""SELECT * FROM user""")
        all = cursor.fetchall()
        if str(all) == "[]":
            cursor.execute("""INSERT INTO user VALUES (?,?,?,?,?)""", (self.age, self.height, self.mass, self.hobby, self.city,))
            conn.commit()
        else:
            cursor.execute("""DELETE FROM user""")
            cursor.execute("""INSERT INTO user VALUES (?,?,?,?,?)""", (self.age, self.height, self.mass, self.hobby, self.city,))
            conn.commit()


class Window_Info(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("image\info.png"))
        self.setWindowTitle("Мини инфо про вас")
        self.setFixedSize(500,400)
        self.initUI()
        self.check_color()
    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.label_info = QLabel("Введите ваше инфо")
        self.label_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_info)

        layout_age = QHBoxLayout()
        self.label_age = QLabel("Ваш возраст: ")
        self.line_age = QLineEdit()
        self.line_age.setValidator(QIntValidator(1,10))
        self.line_age.setPlaceholderText('Введите возраст')
        self.line_age.setToolTip('Введите возраст')
        layout_age.addWidget(self.label_age)
        layout_age.addWidget(self.line_age)
        main_layout.addLayout(layout_age)

        layout_height = QHBoxLayout()
        self.label_height = QLabel("Ваш рост: ")
        self.line_height = QLineEdit()
        self.line_height.textChanged.connect(self.check_height)
        self.line_height.setValidator(QIntValidator(1,100))
        self.line_height.setPlaceholderText('Введите рост')
        self.line_height.setToolTip('Введите рост')
        layout_height.addWidget(self.label_height)
        layout_height.addWidget(self.line_height)
        main_layout.addLayout(layout_height)

        layout_mass = QHBoxLayout()
        self.label_mass = QLabel("Ваш вес: ")
        self.line_mass = QLineEdit()
        self.line_mass.textChanged.connect(self.check_mass)
        self.line_mass.setValidator(QIntValidator(1,100))
        self.line_mass.setPlaceholderText('Введите вес')
        self.line_mass.setToolTip('Введите вес')
        layout_mass.addWidget(self.label_mass)
        layout_mass.addWidget(self.line_mass)
        main_layout.addLayout(layout_mass)

        layout_hobby = QHBoxLayout()
        self.label_hobby = QLabel("Ваше хобби: ")
        self.line_hobby = QLineEdit()
        self.line_hobby.setPlaceholderText('Введите хобби')
        self.line_hobby.setToolTip('Введите хобби')
        self.line_hobby.textChanged.connect(self.check_hobby)
        layout_hobby.addWidget(self.label_hobby)
        layout_hobby.addWidget(self.line_hobby)
        main_layout.addLayout(layout_hobby)

        layout_city = QHBoxLayout()
        self.label_city = QLabel("Ваш город: ")
        self.line_city = QLineEdit()
        self.line_city.setPlaceholderText('Введите ваш город проживания на русском языке')
        regex = QRegExp("[a-zA-Zа-яА-Я ]+")
        validator = QRegExpValidator(regex)
        self.line_city.setValidator(validator)
        self.line_city.setToolTip('Введите ваш город проживания')
        layout_city.addWidget(self.label_city)
        layout_city.addWidget(self.line_city)
        main_layout.addLayout(layout_city)

        self.button_check = QPushButton("Задать данные")
        self.button_check.setToolTip("Проверка данных")
        self.button_check.clicked.connect(self.check_main)
        main_layout.addWidget(self.button_check)

        self.button_remove = QPushButton("Удалить данные")
        self.button_remove.setToolTip("Удаление ваших данных")
        self.button_remove.clicked.connect(self.remove)
        main_layout.addWidget(self.button_remove)

        self.button_exit = QPushButton("Выйти")
        self.button_exit.setToolTip("Выход")
        self.button_exit.clicked.connect(self.leave)
        main_layout.addWidget(self.button_exit)

    def check_height(self):
        try:
            if int(self.line_height.text()) > 250:
                self.line_height.clear()
        except:
            pass

    def check_mass(self):
        try:
            if int(self.line_mass.text()) > 350:
                self.line_mass.clear()
        except:
            pass

    def check_main(self):
        age = self.line_age.text().strip()
        height = self.line_height.text().strip()
        mass = self.line_mass.text().strip()
        hobby = self.line_hobby.text().strip()
        city = self.line_city.text().strip()
        if age == '' or height == '' or mass == '' or hobby == '' or city == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, заполните все поля ввода!')
            msg.show()
            msg.exec_()
        else:
            user = User(int(age), int(height), int(mass), hobby, city)
            user.add_info()
            voice.speaker('Добавил информацию про вас!')
            # self.button_check.setEnabled(False)
            # self.line_age.setEnabled(False)
            # self.line_height.setEnabled(False)
            # self.line_mass.setEnabled(False)
            # self.line_hobby.setEnabled(False)

    def remove(self):
        cursor.execute("""SELECT * FROM user""")
        all = cursor.fetchall()
        print(all)
        if str(all) == '[]':
            voice.speaker('Данных изначально нет!')
        else:
            cursor.execute("""DELETE FROM user""")
            conn.commit()
            voice.speaker('Удалил данные')

    def check_hobby(self):
        for i in self.line_hobby.text().lower().strip():
            if i in en or i in nums:
                self.line_hobby.clear()

    def leave(self):
        sys.exit()

    def check_color(self):
        cursor_color.execute("""SELECT * FROM color_menu""")
        all = cursor_color.fetchall()
        print(all)
        if str(all) == '[]':
            self.setStyleSheet("""
            QWidget {
                background-color: #00BFFF;
            }
            QLabel {
                color: black;
                font: Arial;
                font-size: 24px;
            }
            QPushButton {
                background-color: #87CEEB;
                color: black;
                font: Arial;
                font-size: 16px;
                border: 2px solid;
                border-radius: 7px;
            }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #E0FFFF;
                    border-radius: 10px;
                }
            """)
        else:
            rand_l = []
            for i in all:
                for rand in i:
                    pass
            print(rand)
            if rand == 'red':
                self.setStyleSheet("""
                QWidget {
                    background-color: #CD5C5C;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #F08080;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #E9967A;
                    border-radius: 10px;
                }
                """)
            elif rand == 'green':
                self.setStyleSheet("""
                QWidget {
                    background-color: #32CD32;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #3CB371;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #90EE90;
                    border-radius: 10px;
                }
                """)
            elif rand == 'dark':
                self.setStyleSheet("""
                QWidget {
                    background-color: #696969;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #708090;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #C0C0C0;
                    border-radius: 10px;
                }
                """)
            elif rand == 'pink':
                self.setStyleSheet("""
                QWidget {
                    background-color: #C71585;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #FF69B4;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #FF69B4;
                    border-radius: 10px;
                }
                """)
            elif rand == 'brown':
                self.setStyleSheet("""
                QWidget {
                    background-color: #A52A2A;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #A0522D;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #B8860B;
                    border-radius: 10px;
                }
                """)
            elif rand == 'violet':
                self.setStyleSheet("""
                QWidget {
                    background-color: #9932CC;
                }
                QLabel {
                    color: black;
                    font: Arial;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #EE82EE;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QLineEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
                }
                """)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window_Info()
    w.show()
    sys.exit(app.exec_())
