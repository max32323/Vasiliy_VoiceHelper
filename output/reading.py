from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton,QTextEdit, QVBoxLayout, QApplication, QWidget, \
    QMessageBox, QFileDialog
import sys
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
        global path
        self.setWindowTitle('Мини читалка')
        self.setWindowIcon(QIcon(f'{path[0][0]}/image/info.png'))
        self.setFixedSize(350,400)
        self.path = ''
        self.initUI()
        self.check_color()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.show_text = QTextEdit()
        self.show_text.setReadOnly(True)
        main_layout.addWidget(self.show_text)

        self.button_path = QPushButton('Выбрать файл')
        self.button_path.setToolTip('Выбор файла для чтения')
        self.button_path.clicked.connect(self.open)

        main_layout.addWidget(self.button_path)

        self.button_clear = QPushButton('Очистить поле')
        self.button_clear.setToolTip('Очистить поле')
        self.button_clear.clicked.connect(self.clear)
        main_layout.addWidget(self.button_clear)

        self.button_leave = QPushButton('Выход')
        self.button_leave.setToolTip('Кнонка для завершения программы')
        self.button_leave.clicked.connect(self.leave)

        main_layout.addWidget(self.button_leave)

    def open(self):
        path = QFileDialog.getOpenFileName(self, filter='TXT (*.txt)')[0]
        try:
            if path:
                with open(path, 'r', encoding='utf-8') as file:
                    text = file.read()
                self.show_text.setText(text)
            else:
                self.show_text.setText('')
        except:
            msg = QMessageBox()
            msg.setWindowTitle('Внимание!')
            msg.setWindowIcon(QIcon(f'{path[0][0]}/image/info.png'))
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Пожалуйста проверьте файл на доступность!')
            msg.show()
            msg.exec_()

    def leave(self):
        sys.exit()

    def clear(self):
        self.path = ''
        self.show_text.setText('')

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
            QTextEdit {
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
                QTextEdit {
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
                    font-size: 14px;
                    border: 3px solid #006400;
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
                    font-size: 14px;
                    border: 3px solid black;
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
                    font-size: 14px;
                    border: 3px solid #C71585;
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
                QComboBox {
                    background-color: #A0522D;
                    color: black;
                    font: Arial;
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                } 
                QTextEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid black;
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
                    font-size: 14px;
                    border: 3px solid #4B0082;
                    border-radius: 10px;
                }
                """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())