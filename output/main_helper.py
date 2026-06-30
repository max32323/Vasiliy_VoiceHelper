"""импорт нужных модулей и библиотек"""
import os
import random
import cv2
import imutils
import voice
import voicehelper
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
# import skills
import sqlite3

en = 'abcdefghijklmnopqrstuvwxyz'
num = '1234567890'
"""БАЗА ДАННЫЙ ДЛЯ АВАТАРА ПОЛЬЗОВАТЕЛЯ!"""
connect = sqlite3.connect('user_helper.db')
cursor = connect.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_help 
    (
    user_pix TEXT
    )
    """
)
connect.commit()

"""БАЗА ДАННЫЙ ДЛЯ СОХРАНЕНИЯ ЦВЕТА МЕНЮ!"""
connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

cursor_color.execute(
    """
    CREATE TABLE IF NOT EXISTS color_menu (
    color TEXT
    )
    """
)
"""БАЗА ДАННЫХ ДЛЯ ПУТЯ"""
connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""
    CREATE TABLE IF NOT EXISTS your_path (
    path TEXT,
    path_tg TEXT
    )
""")
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()
"""приложение"""
class My_helper_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() #меню
        self.image_set()
    def initUI(self):
        """Настройка меню"""
        self.setWindowTitle('Меню голосового ассистента Василия')
        self.setFixedSize(750,600)
        self.setWindowIcon(QIcon('image\yy.png'))

        """Создание виджетов"""
        self.label_helper = QLabel(' Голосовой ассистент\n Василий')
        self.label_helper.setAlignment(Qt.AlignCenter)

        self.pix = QLabel()
        self.pix.setAlignment(Qt.AlignCenter)

        self.button_info_helper = QPushButton('Инфо')
        self.button_info_helper.setToolTip('Краткая информация про ассистента')
        self.button_info_helper.clicked.connect(self.info)

        self.button_start = QPushButton('Начать разговор')
        self.button_start.setToolTip('Начать работать с ассистентом')
        self.button_start.clicked.connect(self.start)

        self.button_pix = QPushButton('Выбрать иконку')
        self.button_pix.setToolTip('Ваша иконка')
        self.button_pix.clicked.connect(self.load)

        self.button_del = QPushButton('Удалить иконку')
        self.button_del.setToolTip('Сделать базовую иконку(рекомендуем при больших кол. замены иконки)')
        self.button_del.clicked.connect(self.delete_pix)

        self.button_path = QPushButton('Добавить путь')
        self.button_path.setToolTip('добавления путя для работы')
        self.button_path.clicked.connect(self.check_path)

        self.button_exit = QPushButton('Выйти из программы')
        self.button_exit.setToolTip('Завершение работы с ассистентом')
        self.button_exit.clicked.connect(self.leave)


        self.label_name = QLabel('Введите ваше имя: ')
        self.line_name = QLineEdit()
        self.line_name.setToolTip('Введите ваше имя(необязательный параметр)')
        self.line_name.textChanged.connect(self.check_name)
        self.line_name.setPlaceholderText('Введите ваше имя на русском языке:')

        self.label_path = QLabel('Введите путь проекта: ')
        self.line_path = QLineEdit()
        self.line_path.setToolTip('Путь проекта. Пример: D:\Program Files\pythonProject9')
        self.line_path.setPlaceholderText('Путь проекта. Пример: D:\Program Files\pythonProject9')

        self.label_path_tg = QLabel('Введите путь до телеграмма: ')
        self.line_path_tg = QLineEdit()
        self.line_path_tg.setToolTip('Путь проекта. Пример: D:\Program Files\Telegram Desktop\Telegram.exe')
        self.line_path_tg.setPlaceholderText('Пример: D:\Program Files\Telegram Desktop\Telegram.exe')

        self.label_status_color = QLabel('Цвет дизайна(q или й): ')
        button_status_color = QPushButton('Очистить историю цветов')
        button_status_color.setToolTip('Очистить историю всех цветов(Рекомендуем часто очищать историю)')
        button_status_color.clicked.connect(self.clear_color)

        self.button_set_info = QPushButton('Инфо о пользователе')
        self.button_set_info.setToolTip('Добавить информацию о себе')
        self.button_set_info.clicked.connect(self.info_user)


        """Группировка виджетов"""
        main_layout = QVBoxLayout()
        layout_button = QHBoxLayout()


        layout_button.addWidget(self.button_info_helper)
        layout_button.addWidget(self.button_start)

        layout_name = QHBoxLayout()
        layout_name.addWidget(self.label_name)
        layout_name.addWidget(self.line_name)

        layout_path = QHBoxLayout()
        layout_path.addWidget(self.label_path)
        layout_path.addWidget(self.line_path)

        layout_path_tg = QHBoxLayout()
        layout_path_tg.addWidget(self.label_path_tg)
        layout_path_tg.addWidget(self.line_path_tg)

        # layout_helper = QHBoxLayout()

        main_layout.addWidget(self.pix)
        main_layout.addWidget(self.label_helper)
        main_layout.addLayout(layout_button)
        main_layout.addWidget(self.button_pix)
        main_layout.addWidget(self.button_del)
        main_layout.addWidget(self.button_path)
        main_layout.addWidget(self.button_set_info)
        main_layout.addWidget(button_status_color)
        main_layout.addWidget(self.button_exit)
        main_layout.addWidget(self.label_status_color)

        main_layout.addLayout(layout_name)
        main_layout.addLayout(layout_path)
        main_layout.addLayout(layout_path_tg)

        self.setLayout(main_layout)

        self.check_color()
    def check_path(self):
        if self.line_path.text().strip() == '' or self.line_path_tg.text().strip() == '':
            msg = QMessageBox()
            msg.setWindowIcon(QIcon('image/yy.png'))
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите путь и тг')
            msg.show()
            msg.exec_()
        else:
            voice.speaker('Добавил путь!')
            cursor_path.execute("""SELECT * FROM your_path""")
            all = cursor_path.fetchall()
            if not all:
                cursor_path.execute("""INSERT INTO your_path VALUES (?,?)""", (self.line_path.text().strip(), self.line_path_tg.text().strip(),))
            else:
                cursor_path.execute('DELETE FROM your_path')
                cursor_path.execute("""INSERT INTO your_path VALUES (?,?)""", (self.line_path.text().strip(), self.line_path_tg.text().strip(),))
            connect_path.commit()
    def check_name(self):
        for i in self.line_name.text().lower().strip():
            if i in en or i in num:
                self.line_name.clear()

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
            self.label_status_color.setText('Цвет дизайна(q или й): Aqua(Классический)')
        else:
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
                self.label_status_color.setText('Цвет дизайна(q или й): Aqua(Классический)')
            elif rand == 'red':
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')

    """Инфо"""
    def info(self):
        voice.speaker('Открываю инфо обо мне')
        window = QMessageBox()
        window.setWindowTitle('Инфо про Василия')
        window.setWindowIcon(QIcon('image\yy.png'))
        window.setText('Василий - это голосовой ассистент c ИИ, который готов помочь вам.\n                                         Версия Василия: 2.1.0')
        window.exec_()


    def load(self):
        voice.speaker('Устанавливаю')
        self.filepath = QFileDialog.getOpenFileName(filter="Image (*.png *.svg *.jpg)")[0]
        print(self.filepath)
        self.image = cv2.imread(self.filepath)
        self.set_pix(self.image)

    def set_pix(self, image):
        if image is not None:
            image = imutils.resize(image, width=640)
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.pix.setPixmap(QPixmap.fromImage(image.scaled(200,200)))
            cursor.execute("""INSERT INTO user_help VALUES (?)""", (self.filepath,))
            connect.commit()


    def image_set(self):
        try:
            cursor.execute("""SELECT * FROM user_help""")
            self.filepath = ''
            for i in cursor.fetchall()[-1]:
                self.filepath = self.filepath + i
            print(self.filepath)
            ik = cv2.imread(self.filepath)
            self.set_pix(ik)
        except:
            print('нет фото')
            im = QPixmap('image\my_n')
            self.pix.setPixmap(im.scaled(200,200))

    def delete_pix(self):
        voice.speaker('Удаляю')
        cursor.execute('DELETE FROM user_help')
        im = QPixmap('image\my_n')
        self.pix.setPixmap(im.scaled(200,200))
        connect.commit()

    """Начало работы"""
    def start(self):
        cursor_path.execute("""SELECT * FROM your_path""")
        all = cursor_path.fetchall()
        if not all:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon('image/yy.png'))
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите путь и тг!')
            msg.show()
            msg.exec_()

        else:
            if self.line_name.text().strip() != '':
                cursor_path.execute("""SELECT * FROM your_path""")
                all = cursor_path.fetchall()
                with open(f'{all[0][0]}\my_name', 'w', encoding='utf-8') as file:
                    file.write(self.line_name.text().strip())
                    file.close()
                self.close()
                voice.speaker('Можете начать диалог')
                voicehelper.main()
            else:
                self.close()
                voice.speaker('Можете начать диалог')
                voicehelper.main()
        # except:
        #     msg = QMessageBox()
        #     msg.setWindowIcon(QIcon('image/yy.png'))
        #     msg.setIcon(QMessageBox.Warning)
        #     msg.setWindowTitle('Предупреждение!')
        #     msg.setText('Пожалуйста, введите путь и тг!.')
        #     msg.show()
        #     msg.exec_()
            # with open(f'{path[0][0]}\my_name', 'r', encoding='utf-8') as file:
            # self.close()
            # voice.speaker('Можете начать диалог')
            # voicehelper.main()

    def leave(self):
        voice.speaker('до скорых встреч!')
        sys.exit()

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if str(key) == '81' or str(key) == '1049':
            list_color = ['red', 'green', 'dark', 'pink', 'brown', 'violet']
            rand = random.choice(list_color)
            cursor_color.execute("""INSERT INTO color_menu VALUES (?)""", (rand,))
            connect_color.commit()
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')
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
                self.label_status_color.setText(f'Цвет дизайна(q или й): {str(rand).capitalize()}')

    def info_user(self):
        file_path = 'd:\\\\program files\\\\pythonproject9\\\\output\\\\user_data.exe'
        if os.path.exists(file_path):
            voice.speaker('Открываю')
            os.startfile(file_path)
        else:
            voice.speaker('Ошибка загрузки! Попробуйте позже')

    def clear_color(self):
        cursor_color.execute("""DELETE FROM color_menu""")
        connect_color.commit()
        self.check_color()


voice.speaker('Добро пожаловать!')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = My_helper_window()
    w.show()
    sys.exit(app.exec_())
