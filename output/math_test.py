import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QRadioButton, QWidget, QHBoxLayout, \
    QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import random as rnd
import voice

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()
class Math_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.point = 0
        self.good = 0
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\math_test_icon.png'))
        self.setWindowTitle('Математический тренажёр')
        self.setFixedSize(450,300)
        self.initUI()
        self.check_color()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.example_label = QLabel('Ваш пример: ')
        self.example_text = QLineEdit()
        self.example_text.setReadOnly(True)
        layout_example = QHBoxLayout()
        layout_example.addWidget(self.example_label)
        layout_example.addWidget(self.example_text)
        main_layout.addLayout(layout_example)

        self.user_label = QLabel('Ваш ответ:   ')
        self.user_answer = QLineEdit()
        layout_example = QHBoxLayout()
        layout_example.addWidget(self.user_label)
        layout_example.addWidget(self.user_answer)
        main_layout.addLayout(layout_example)

        self.button_prov = QPushButton('Сохранить ответ')
        self.button_prov.setEnabled(False)
        self.button_prov.clicked.connect(self.check)
        main_layout.addWidget(self.button_prov)

        self.label_power = QLabel('Уровень сложности:')
        self.label_power.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_power)

        self.easy_button = QRadioButton('Лёгкий(целые значения)')
        # self.easy_button.setStyleSheet("""
        #     color: green;
        #     font-size: 16px;
        # """)
        self.normal_button = QRadioButton('Средний(целые значения)')
        # self.normal_button.setStyleSheet("""
        #     color: yellow;
        #     font-size: 16px;
        # """)
        self.hard_button = QRadioButton('Сложный(целые значения)')
        # self.hard_button.setStyleSheet("""
        #     color: red;
        #     font-size: 16px;
        # """)
        main_layout.addWidget(self.easy_button)
        main_layout.addWidget(self.normal_button)
        main_layout.addWidget(self.hard_button)

        self.itog_label = QLabel('Итог: ')
        main_layout.addWidget(self.itog_label)

        self.button_start = QPushButton('Начать мини тест')
        self.button_start.clicked.connect(self.start)
        main_layout.addWidget(self.button_start)

        self.button_leave = QPushButton('Выйти')
        self.button_leave.clicked.connect(self.leave)
        main_layout.addWidget(self.button_leave)

        self.setLayout(main_layout)

    def leave(self):
        voice.speaker('До свидание')
        sys.exit()

    def start(self):
        if self.easy_button.isChecked():
            if self.easy_button.isEnabled():
                voice.speaker('начинаю тест на лёгком уровне')
            self.itog_label.setText('Итог: ')
            self.button_start.setEnabled(False)
            self.button_prov.setEnabled(True)
            self.easy_button.setEnabled(False)
            self.normal_button.setEnabled(False)
            self.hard_button.setEnabled(False)

            if self.point < 10:
                num_1 = rnd.randint(1,10)
                num_2 = rnd.randint(1,10)
                list_do = ['+','-', '//', '*']
                r = rnd.choice(list_do)
                self.example_main = str(num_1) + r + str(num_2)
                if r == '//':
                    r = '÷'
                example_new = str(num_1) + r + str(num_2)
                self.example_text.setText(example_new)
            elif self.point == 10:
                voice.speaker('Вы прошли тест!')
                self.itog_label.setText(f'Итог: Вы ответили {self.good} из {self.point}')
                self.easy_button.setEnabled(True)
                self.normal_button.setEnabled(True)
                self.hard_button.setEnabled(True)
                self.button_prov.setEnabled(False)
                self.button_start.setEnabled(True)
                self.point = 0
                self.good = 0

        elif self.normal_button.isChecked():
            if self.normal_button.isEnabled():
                voice.speaker('начинаю тест на среднем уровне')
            self.itog_label.setText('Итог: ')
            self.button_start.setEnabled(False)
            self.button_prov.setEnabled(True)
            self.easy_button.setEnabled(False)
            self.normal_button.setEnabled(False)
            self.hard_button.setEnabled(False)

            if self.point < 10:
                num_1 = rnd.randint(1,10)
                num_2 = rnd.randint(1,10)
                list_do = ['+','-', '//', '*', '**']
                r = rnd.choice(list_do)
                self.example_main = str(num_1) + r + str(num_2)
                if r == '//':
                    r = '÷'
                elif r == '**':
                    num_2 = rnd.randint(1,3)
                    self.example_main = str(num_1) + r + str(num_2)
                    r = '^'
                else:
                    self.example_main = str(num_1) + r + str(num_2)
                example_new = str(num_1) + r + str(num_2)
                self.example_text.setText(example_new)
            elif self.point == 10:
                voice.speaker('Вы прошли тест!')
                self.itog_label.setText(f'Итог: Вы ответили {self.good} из {self.point}')
                self.easy_button.setEnabled(True)
                self.normal_button.setEnabled(True)
                self.hard_button.setEnabled(True)
                self.button_prov.setEnabled(False)
                self.button_start.setEnabled(True)
                self.point = 0
                self.good = 0

        elif self.hard_button.isChecked():
            if self.hard_button.isEnabled():
                voice.speaker('начинаю тест на сложном уровне')
            self.itog_label.setText('Итог: ')
            self.button_start.setEnabled(False)
            self.button_prov.setEnabled(True)
            self.easy_button.setEnabled(False)
            self.normal_button.setEnabled(False)
            self.hard_button.setEnabled(False)

            if self.point < 10:
                num_1 = rnd.randint(1,10)
                num_2 = rnd.randint(1,10)
                num_3 = rnd.randint(1,5)
                list_do = ['+', '-', '//', '*', '**']
                list_do2 = ['+', '-', '*']
                r = rnd.choice(list_do)
                r2 = rnd.choice(list_do2)
                self.example_main = str(num_1) + r + str(num_2) + r2 + str(num_3)
                if r == '//':
                    r = '÷'
                elif r == '**':
                    num_2 = rnd.randint(1,4)
                    self.example_main = str(num_1) + r + str(num_2) + r2 + str(num_3)
                    r = '^'
                else:
                    self.example_main = str(num_1) + r + str(num_2) + r2 + str(num_3)
                example_new = str(num_1) + r + str(num_2) + r2 + str(num_3)
                self.example_text.setText(example_new)
            elif self.point == 10:
                voice.speaker('Вы прошли тест!')
                self.itog_label.setText(f'Итог: Вы ответили {self.good} из {self.point}')
                self.easy_button.setEnabled(True)
                self.normal_button.setEnabled(True)
                self.hard_button.setEnabled(True)
                self.button_prov.setEnabled(False)
                self.button_start.setEnabled(True)
                self.point = 0
                self.good = 0
        else:
            voice.speaker('Ошибка!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, выберете сложность!')
            msg.show()
            msg.exec_()

    def check(self):
        if self.user_answer.text().strip() != '':
            if int(self.user_answer.text().strip()) == int(eval(self.example_main)):
                self.good += 1
                self.point += 1
            else:
                self.point += 1
            print('Ваш ответ: ', int(self.user_answer.text().strip()))
            print('Ответ: ', int(eval(self.example_main)))
            print('Правильные ответы: ', self.good)
            print('Попытки: ', self.point)
            self.user_answer.clear()
            self.start()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, напишите ответ!')
            msg.show()
            msg.exec_()

    def check_color(self):
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
            QLineEdit {
                font: Arial;
                font-size: 14px;
                border: 3px solid #E0FFFF;
                border-radius: 10px;
            }
            QRadioButton {
                font-size: 14px;
                }
            """)
        else:
            rand_l = []
            for i in all:
                for rand in i:
                    pass
            print(rand)
            if rand == 'aqua':
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
                QRadioButton {
                    font-size: 14px;
                    }
                """)
            elif rand == 'red':
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
                    border: 3px solid #E9967A;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                QRadioButton {
                    font-size: 14px;
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
                QRadioButton {
                    font-size: 14px;
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
                QRadioButton {
                    font-size: 14px;
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
                QRadioButton {
                    font-size: 14px;
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
                QRadioButton {
                    font-size: 14px;
                }
                """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Math_Window()
    w.show()
    sys.exit(app.exec_())