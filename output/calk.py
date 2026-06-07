import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QCheckBox, \
    QMessageBox
import sys
import voice
connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()

class Window_math(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Калькулятор')
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\calk.jpg'))
        self.setFixedSize(500,300)
        self.initUI()
        self.style()
    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.pix = QLabel()
        self.pix.setAlignment(Qt.AlignCenter)
        self.image = QPixmap(f'{path[0][0]}\image\math.PNG')
        self.pix.setPixmap(self.image.scaled(250,150))
        main_layout.addWidget(self.pix)

        layout_user_example = QHBoxLayout()

        self.label_text = QLabel("Введите ваш пример: ")
        layout_user_example.addWidget(self.label_text)
        self.user_example = QLineEdit()
        self.user_example.setPlaceholderText('Ваш пример')
        layout_user_example.addWidget(self.user_example)
        main_layout.addLayout(layout_user_example)

        self.label_answer = QLabel('Ответ: ')
        main_layout.addWidget(self.label_answer)

        self.button_start = QPushButton('Решить пример')
        self.button_start.setToolTip('Решить пример')
        self.button_start.clicked.connect(self.start)
        main_layout.addWidget(self.button_start)


        self.button_leave = QPushButton('Выйти')
        self.button_leave.clicked.connect(self.leave)
        main_layout.addWidget(self.button_leave)


    def leave(self):
        voice.speaker('До свидание!')
        sys.exit()
    def start(self):
        if self.user_example.text().strip() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите ваш пример')
            msg.show()
            msg.exec_()
        else:
            try:
                answer = eval(self.user_example.text().strip())
                self.label_answer.setText(f'Ответ: {str(answer)}')
            except:
                self.label_answer.setText('Ответ: пример введён некорректно!')
    def style(self):
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
                QLineEdit {
                    font: Arial;
                    font-size: 18px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
                }
                """)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window_math()
    w.show()
    sys.exit(app.exec_())