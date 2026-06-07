import datetime

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QLineEdit, \
    QMessageBox
import sys


FILE = 'D:\Program Files\pythonProject9\заметки и шифры'
# FILE = 'D:\записки.txt'

def time_all():
    time = datetime.datetime.now()
    hour = time.hour
    minute = time.minute
    month_dist = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
                  8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    day = time.day
    for key, values in month_dist.items():
        if time.month == key:
            month = values
    if int(hour) < 10:
        hour = '0' + str(hour)
    if int(minute) < 10:
        minute = '0' + str(minute)
    if int(day) < 10:
        day = '0' + str(day)
    return f'{time.year}: {day} {month} - {hour}:{minute}'


class TXT_File:
    def __init__(self, file):
        self.name: str = file

    def read(self):
        with open(self.name, 'r', encoding='utf-8') as file:
            text: str = file.read()
        return text

    def get(self, text):
        with open(self.name, 'a', encoding='utf-8') as file:
            file.write(f'ЗАМЕТКА: {text}\nДАТА СОХРАНЕНИЯ: {time_all()}\n\n')

    def clear(self):
        with open(self.name, 'w', encoding='utf-8') as file:
            file.write('')

class Window(QWidget):
    def __init__(self):
        global FILE
        super().__init__()
        self.setWindowTitle('Мини заметки')
        self.setWindowIcon(QIcon('image\info.png'))
        self.setFixedSize(400,400)
        self.TXT_File = TXT_File(FILE)
        self.initUI()
        self.style()


    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.line_info = QTextEdit()
        self.line_info.setReadOnly(True)
        self.line_info.setText(self.TXT_File.read())

        main_layout.addWidget(self.line_info)

        layout_input = QHBoxLayout()

        self.label_input = QLabel('Введите текст: ')
        layout_input.addWidget(self.label_input)

        self.line_user = QLineEdit()
        self.line_user.setPlaceholderText('Введите заметку')
        layout_input.addWidget(self.line_user)

        main_layout.addLayout(layout_input)


        self.button_input = QPushButton('Добавить заметку')
        self.button_input.clicked.connect(self.get)
        main_layout.addWidget(self.button_input)

        self.button_clear = QPushButton('Очистить заметки')
        self.button_clear.clicked.connect(self.clear)
        main_layout.addWidget(self.button_clear)

        self.button_exit = QPushButton('Выйти')
        self.button_exit.clicked.connect(self.leave)
        main_layout.addWidget(self.button_exit)


    def get(self):
        if self.line_user.text().strip():
            self.TXT_File.get(self.line_user.text().strip())
            self.line_info.setText(self.TXT_File.read())
        else:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon('image\info.png'))
            msg.setWindowTitle('Предупреждение!')
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Введите заметку!')
            msg.show()
            msg.exec_()

    def clear(self):
        self.TXT_File.clear()
        self.line_info.setText(self.TXT_File.read())

    def style(self):
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
            color: black;
            font: Arial;
            font-size: 14px;
            border: 3px solid #90EE90;
            border-radius: 10px;
        }
        QTextEdit {
            color: black;
            font: Arial;
            font-size: 14px;
            border: 3px solid #90EE90;
            border-radius: 10px;
        }    
        """)

    def leave(self):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())