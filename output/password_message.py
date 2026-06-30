import random
import sqlite3
import sys
from PyQt5.QtCore import Qt
# import voicehelper
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, \
    QMessageBox
from PyQt5.QtGui import QIcon
import datetime
import string
import voice
from check_password import check


connect = sqlite3.connect('password_server.db')

cursor = connect.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS password (
    name TEXT,
    password TEXT,
    time TEXT
    )
    """
)
connect.commit()
connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()

class Password_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Пароли')
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\key.png'))
        self.setFixedSize(600,500)
        self.count = random.randint(8,16)
        self.initUI()
        self.style()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.server = QLabel('Название: ')
        self.server.setToolTip(' Название сайта или сервиса для сохранения пароля')
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText(' Напишите название сайта')
        layout_serves = QHBoxLayout()
        layout_serves.addWidget(self.server)
        layout_serves.addWidget(self.server_input)

        self.password = QLabel('Пароль: ')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(' Задайте пароль')
        layout_password = QHBoxLayout()
        layout_password.addWidget(self.password)
        layout_password.addWidget(self.password_input)

        layout_all = QHBoxLayout()
        layout_all.addLayout(layout_serves)
        layout_all.addLayout(layout_password)
        main_layout.addLayout(layout_all)

        layout_button = QHBoxLayout()


        # button_say = QPushButton(' Задать сайт голосом')
        # button_say.setIcon(QIcon('image/micro.png'))
        # button_say.setToolTip('Задайте название голосом')
        # button_say.clicked.connect(self.say)
        # layout_button.addWidget(button_say)

        button_password = QPushButton(' Сгенерировать случайный пароль')
        button_password.setIcon(QIcon(f'{path[0][0]}\image\diffrent.png'))
        button_password.setToolTip('Случайный пароль')
        button_password.clicked.connect(self.password_generate)
        layout_button.addWidget(button_password)

        main_layout.addLayout(layout_button)
        button_save = QPushButton(' Сохранение')
        button_save.setIcon(QIcon(f'{path[0][0]}\image\save.png'))
        button_save.setToolTip('Сохраните пароль и сайт')
        button_save.clicked.connect(self.save)
        main_layout.addWidget(button_save)

        all_password = QLabel('Все пароли')
        main_layout.addWidget(all_password)
        all_password.setAlignment(Qt.AlignCenter)

        self.menu_password = QTextEdit()
        self.menu_password.setReadOnly(True)
        main_layout.addWidget(self.menu_password)
        cursor.execute("""SELECT * FROM password""")
        all = cursor.fetchall()
        print(all)
        self.text = ''
        for i in all:
            self.text += i[0] + ': ' + i[1] + ' ' + i[2] + '\n'
            self.menu_password.setPlainText(self.text)

        button_remove = QPushButton(' Удалить все данные')
        button_remove.setIcon(QIcon(f'{path[0][0]}\image\delete.PNG'))
        button_remove.setToolTip(' Очистка всех паролей и названий из базы данных')
        button_remove.clicked.connect(self.remove_all)
        main_layout.addWidget(button_remove)

        button_leave = QPushButton(' Выход')
        button_leave.setIcon(QIcon(f'{path[0][0]}\image\exit.PNG'))
        button_leave.setToolTip('Выход')
        button_leave.clicked.connect(self.leave)
        main_layout.addWidget(button_leave)

    def leave(self):
        voice.speaker('До встречи!')
        sys.exit()

    def password_generate(self):
        alpha = string.digits + string.ascii_lowercase + string.ascii_uppercase + '!@#$%^&*()-—_=+№%[]{},.<>?;:"\\|\\\\`~–'
        password = ''
        while True:
            for _ in range(self.count):
                piece_password = random.choice(alpha)
                password += piece_password
            if check(password):
                self.password_input.setText(password)
                break
            else:
                password = ''

    # def say(self):
    #     play_sound('make_text_n.mp3')
    #     self.server_input.setText(voicehelper.main_2())

    def save(self):
        if self.server_input.text().strip() != '' and self.password_input.text().strip() != '':
            time = datetime.datetime.now()
            hour = time.hour
            minute = time.minute
            day = time.day
            month_dist = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
                          8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
            for key, values in month_dist.items():
                if time.month == key:
                    month = values
            if int(hour) < 10:
                hour = '0' + str(hour)
            if int(minute) < 10:
                minute = '0' + str(minute)
            if int(day) < 10:
                day = '0' + str(day)
            name = self.server_input.text()
            password = self.password_input.text()
            time_now = str(f'{time.year}: {day} {month} - {hour}:{minute}')
            if check(password):
                self.menu_password.setPlainText(f'{name} - {password}: {time_now}')
                cursor.execute("""INSERT INTO password VALUES (?,?,?)""", (name, password, time_now,))
                connect.commit()
                cursor.execute("""SELECT * FROM password""")
                all = cursor.fetchall()
                print(all)
                self.text = ''
                for i in all:
                    self.text += i[0] + ': ' + i[1] + ' ' + i[2] + '\n'
                    self.menu_password.setPlainText(self.text)
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Внимание')
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Пожалуйста измените пароль. Он слишком простой!')
                msg.show()
                msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, напишите название и пароль!')
            msg.show()
            msg.exec_()

    def remove_all(self):
        voice.speaker('Данные были успешно удалены!')
        cursor.execute("""DELETE FROM password""")
        connect.commit()
        # cursor.execute("""SELECT * FROM password""")
        self.menu_password.setPlainText('')

    def style(self):
        cursor_color.execute("""SELECT * FROM color_menu""")
        all = cursor_color.fetchall()
        print(all)
        if not all:
            self.setStyleSheet("""
            QWidget {
                background-color: #00BFFF;
            }
            QLabel {
                color: black;
                font: Arial;
                font-size: 18px;
            }
            QPushButton {
                background-color: #87CEEB;
                color: black;
                font: Arial;
                font-size: 16px;
                border: 2px solid;
                border-radius: 7px;
            }
            QTextEdit {
                font: Arial;
                font-size: 18px;
                border: 3px solid #E0FFFF;
                border-radius: 10px;
            }
            QLineEdit {
                font: Arial;
                font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #F08080;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #E9967A;
                    border-radius: 10px;
                }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #3CB371;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #90EE90;
                    border-radius: 10px;
            }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #708090;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #C0C0C0;
                    border-radius: 10px;
                }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #FF69B4;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #FF69B4;
                    border-radius: 10px;
                }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #A0522D;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #B8860B;
                    border-radius: 10px;
                }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
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
                    font-size: 18px;
                }
                QPushButton {
                    background-color: #EE82EE;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                QTextEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
                }
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
                }
                """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Password_Window()
    w.show()
    sys.exit(app.exec_())