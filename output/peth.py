import random
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout
import sqlite3

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Тренировка печати')
        self.setFixedSize(400,200)
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\peth.jpg'))
        self.initUI()
        self.check_color()

    def initUI(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.elapsed_time = 0
        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()


        self.label_exesise = QLabel('Текст: Обновите текст')
        hlayout2.addWidget(self.label_exesise)

        self.label_exesise2 = QLabel(self)
        hlayout2.addWidget(self.label_exesise2)

        self.label_answeruser = QLabel('Ввод: ')
        hlayout.addWidget(self.label_answeruser)

        self.edit_answeruser = QLineEdit(self)
        hlayout.addWidget(self.edit_answeruser)

        self.edit_answeruser.textChanged.connect(self.show_text)

        self.button = QPushButton('Обновить текст')
        self.button.setToolTip('Начать игру')
        self.button.clicked.connect(self.randon_text)

        self.label_exesiseuser = QLabel('Ваш текст: Введите текст')

        self.point = 0

        self.label_point = QLabel(f'Слов написано: {self.point}/10')

        self.button_exit = QPushButton('Выйти')
        self.button_exit.setToolTip('Выход')
        self.button_exit.clicked.connect(sys.exit)

        self.timer_label = QLabel('Время: Ч:00 М:00 С:00')

        layout.addLayout(hlayout2)
        layout.addWidget(self.label_exesiseuser)
        layout.addLayout(hlayout)
        layout.addWidget(self.label_point)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.button)
        layout.addWidget(self.button_exit)

        self.setLayout(layout)


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
            QLineEdit {
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #CD5C5C;
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
                QLineEdit {
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
                QLineEdit {
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
                QLineEdit {
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
                QLineEdit {
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
            }
                """)


    def show_text(self):
        try:
            self.label_exesiseuser.setText(f'Ваш текст: {self.edit_answeruser.text()}')
            if str(self.edit_answeruser.text()) == str(self.text):
                self.point += 1
                self.label_point.setText(f'Слов написано: {self.point}/10')
                self.edit_answeruser.clear()
                self.randon_text()
                if self.point == 10:
                    self.timer.stop()
                    self.end()
                    self.button.setEnabled(True)
                    self.point = 0
                    self.label_point.setText(f'Слов написано: {self.point}/10')
                    self.label_exesise.setText('Поздравляю! Вы прошли обучение!')
        except:
            pass

    def end(self):
        self.elapsed_time = 0

    def randon_text(self):
        self.edit_answeruser.clear()
        list = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        size = random.randint(4,12)
        self.text = ''
        for i in range(int(size)):
            r = random.choice(list)
            self.text += r
        self.timer.start(1000)
        # self.rnd = random.choice(list)
        self.label_exesise.setText(f'Текст: {self.text}')
        self.button.setEnabled(False)



    def update_timer(self):
        self.elapsed_time += 1
        house = self.elapsed_time // 3600
        minut = (self.elapsed_time % 3600) // 60
        sec = (self.elapsed_time % 3600) % 60
        self.timer_label.setText(f'Время: Ч:{house:02} М:{minut:02} С:{sec:02}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())