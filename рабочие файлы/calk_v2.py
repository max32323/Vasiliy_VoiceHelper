import sys
from math import factorial

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QMessageBox
from PyQt5.QtGui import QIcon
import pygame
import sqlite3


def play_sound(sound: str):
    try:
        pygame.init()
        sound_file = sound
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(0.5)
        sound.play()
        while pygame.mixer.get_busy():
            continue
        pygame.quit()
    except:
        pass

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.round_ans = False
        self.float_ans = True

        self.example = ''
        self.setWindowTitle('Мини калькулятор')
        self.setWindowIcon(QIcon('image/calk.jpg'))
        self.setFixedSize(350,450)
        self.initUI()
        self.style()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.line_answer = QLineEdit()
        self.line_answer.setReadOnly(True)
        self.line_answer.setFixedSize(325,100)
        self.line_answer.setToolTip('Ответ на пример')

        main_layout.addWidget(self.line_answer)

        numbers_buttons = QGridLayout()

        self.num_0 = QPushButton('0')
        self.num_0.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_0, 0,0)

        self.num_1 = QPushButton('1')
        self.num_1.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_1, 0,1)

        self.num_2 = QPushButton('2')
        self.num_2.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_2, 0,2)

        self.num_3 = QPushButton('3')
        self.num_3.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_3, 1,0)

        self.num_4 = QPushButton('4')
        self.num_4.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_4, 1,1)

        self.num_5 = QPushButton('5')
        self.num_5.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_5, 1,2)

        self.num_6 = QPushButton('6')
        self.num_6.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_6, 2,0)

        self.num_7 = QPushButton('7')
        self.num_7.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_7, 2,1)

        self.num_8 = QPushButton('8')
        self.num_8.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_8, 2,2)

        self.num_9 = QPushButton('9')
        self.num_9.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_9, 3,0)

        self.num_sum = QPushButton('+')
        self.num_sum.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_sum, 3,1)

        self.num_nim = QPushButton('-')
        self.num_nim.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_nim, 3,2)

        self.num_um = QPushButton('*')
        self.num_um.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_um, 4,0)

        self.num_raz = QPushButton('/')
        self.num_raz.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_raz, 4,1)

        self.num_raz = QPushButton('√')
        self.num_raz.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_raz, 4,2)

        self.num_degree = QPushButton('^')
        self.num_degree.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_degree, 5,0)

        self.num_left = QPushButton('(')
        self.num_left.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_left, 5,1)

        self.num_right = QPushButton(')')
        self.num_right.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_right, 5,2)

        self.num_dot = QPushButton('.')
        self.num_dot.clicked.connect(self.num_input)
        numbers_buttons.addWidget(self.num_dot, 6,0)

        self.num_fact = QPushButton('!')
        self.num_fact.clicked.connect(self.fact)
        numbers_buttons.addWidget(self.num_fact, 6,1)

        self.button_clear = QPushButton('Очистить пример')
        self.button_clear.clicked.connect(self.clear)

        layout_answer_type = QHBoxLayout()

        self.button_round = QPushButton('Ответ округлённый\n(в > сторону!)')
        self.button_round.setToolTip('Сделать ответ равный, к примеру из 3.4 сделать просто 3')
        self.button_round.clicked.connect(self.round)

        layout_answer_type.addWidget(self.button_round)

        self.button_not_round = QPushButton('Ответ не округлённый')
        self.button_not_round.setFixedSize(160,38)
        self.button_round.setToolTip('Обычный ответ с дробной частью')
        self.button_not_round.clicked.connect(self.not_round)

        self.button_exit = QPushButton('Выход')
        self.button_exit.setToolTip('Выход')
        self.button_exit.clicked.connect(self.leave)

        layout_answer_type.addWidget(self.button_not_round)
        main_layout.addLayout(numbers_buttons)
        main_layout.addWidget(self.button_clear)
        main_layout.addLayout(layout_answer_type)
        main_layout.addWidget(self.button_exit)

    def leave(self):
        sys.exit()

    def clear(self):
        play_sound('click.mp3')
        self.line_answer.setText('')
        self.example = ''

    def round(self):
        play_sound('click.mp3')
        self.round_ans = True
        self.float_ans = False

    def not_round(self):
        play_sound('click.mp3')
        self.round_ans = False
        self.float_ans = True

    def num_input(self):
        play_sound('click.mp3')
        sym = self.sender().text()
        if sym == '√':
            sym = '**0.5'
        elif sym == '^':
            sym = '**'
        elif sym == '!':
            pass
        self.example += sym
        print(self.example)
        try:
            if self.round_ans:
                self.line_answer.setText(str(round(eval(self.example))))
            else:
                self.line_answer.setText(str(eval(str(self.example))))
        except:
            self.line_answer.setText('Ошибка!')

    def fact(self):
        play_sound('click.mp3')
        try:
            self.example = str(factorial(int(eval(str(self.example)))))
            if self.round_ans:
                self.line_answer.setText(str(round(eval(self.example))))
            else:
                self.line_answer.setText(str(eval(str(self.example))))
        except:
            self.line_answer.setText('Ошибка!')
            msg = QMessageBox()
            msg.setText('Предупреждение! Факториал работает только с готовым ответом на пример. Проверьте, правильно ли вы его записали.')
            msg.setWindowTitle('Предупреждение')
            msg.setIcon(QMessageBox.Warning)
            msg.show()
            msg.exec_()

    def style(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #32CD32;
        }
        QPushButton {
            background-color: #3CB371;
            color: black;
            font: Arial;
            font-size: 14px;
            border: 2px solid;
            border-radius: 7px;
        }
        QLineEdit {
            font: Arial;
            color: black;
            font-size: 14px;
            border: 3px solid #006400;
            border-radius: 10px;
        }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())