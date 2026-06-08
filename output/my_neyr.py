import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import pyperclip, voice
import openai
import pygame

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()
connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()

def play_sound(sound: str):
    pygame.init()
    sound_file = sound
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(0.5)
    sound.play()
    while pygame.mixer.get_busy():
        continue
    pygame.quit()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Мини чат с ИИ')
        self.setFixedSize(850,700)
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\yrane.jpg'))
        self.initUI()
        self.style()
        self.voice = False
        self.speak = False

        self.b = True

    def initUI(self):
        self.label_norm = QLabel('Запрос:')
        self.label_norm.setToolTip('макс. 1000 символов')
        self.label_norm.setAlignment(Qt.AlignCenter)
        self.user_text = QTextEdit()
        self.user_text.textChanged.connect(self.limit_text_length)

        self.user_text.setFixedSize(825,100)


        layout_main = QVBoxLayout()


        self.label_II = QLabel('Ответ нейросети:')
        self.label_II.setToolTip('ответ занимает максимум 5 мин.')
        self.label_II.setAlignment(Qt.AlignCenter)

        layout_main.addWidget(self.label_norm)
        layout_main.addWidget(self.user_text)
        layout_main.addWidget(self.label_II)

        self.answer_II = QTextEdit()
        self.answer_II.setReadOnly(True)



        layout_main.addWidget(self.answer_II)


        self.setLayout(layout_main)

        layout_button = QHBoxLayout()

        self.button_give_text = QPushButton(' Отправить запрос')
        self.button_give_text.setToolTip('Напишите запрос для ответа')
        self.button_give_text.setIcon(QIcon(f'{path[0][0]}\image\go.png'))
        self.button_give_text.clicked.connect(self.II)
        layout_button.addWidget(self.button_give_text)

        self.button_copy = QPushButton(' Копировать ответ')
        self.button_copy.setToolTip('Копировать полученный ответ ИИ')
        self.button_copy.setIcon(QIcon(f'{path[0][0]}\image\copy.jpg'))
        self.button_copy.clicked.connect(self.copy)
        layout_button.addWidget(self.button_copy)

        self.button_exit = QPushButton(' Выйти')
        self.button_exit.setToolTip('Завершение работы')
        self.button_exit.setIcon(QIcon(f'{path[0][0]}\image\exit.PNG'))
        self.button_exit.setFixedSize(825,25)
        self.button_exit.clicked.connect(self.exit)

        self.button_clear = QPushButton(' Очистить чат')
        self.button_clear.setToolTip('Очистить запрос и ответ ИИ')
        self.button_clear.setIcon(QIcon(f'{path[0][0]}\image\clear.jpg'))
        self.button_clear.clicked.connect(self.clear)
        layout_button.addWidget(self.button_clear)

        # layout_button2 = QHBoxLayout()

        # self.button_audio = QPushButton('    Включить функцию\n записи запроса голосом ')
        # self.button_audio.setIcon(QIcon('hugh.jpg'))
        # self.button_audio.setFixedSize(825,60)

        # self.button_audio.clicked.connect(self.audio)


        layout_main.addLayout(layout_button)
        # layout_main.addWidget(self.button_audio)
        layout_main.addWidget(self.button_exit)
        self.check_color()

    def limit_text_length(self):
        if len(self.user_text.toPlainText()) > 1000:
            cursor = self.user_text.textCursor()
            cursor.deletePreviousChar()
            self.user_text.setTextCursor(cursor)

    # def audio(self):
    #     try:
    #         self.button_audio.setEnabled(False)
    #         play_sound('make_text_n.mp3')
    #         self.user_text.setText(voicehelper.main_2())
    #         self.button_audio.setEnabled(True)
    #     except:
    #         voice.speaker('Плохое подключение к микрофону!')
    def clear(self):
        self.answer_II.clear()
        self.user_text.clear()

    def exit(self):
        voice.speaker('До встречи!')
        sys.exit()

    def copy(self):
        pyperclip.copy(self.answer_II.toPlainText())

    def II(self):
        self.button_give_text.setEnabled(False)
        if self.user_text.toPlainText().strip() != '':
            play_sound('went.mp3')
            self.answer_II.clear()
            with open(f'{path[0][0]}\my_name', 'r', encoding='utf-8') as file:
                name = file.read()
                if name == '':
                    name = 'Неизвестная личность'

            try:
                with open('API_KEY.txt', 'r', encoding='utf-8') as file:
                    api = file.read().strip()
                openai.api_key = api
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": f"Твоего пользователя зовут {name}. Ты добрый человек который готов помочь пользователю ответить на любой вопрос. Страрайся давать ответ на русском языке"},
                        {"role": "user",
                         "content": f"Ты - Василий, а твоего пользователя зовут {name}. Запрос: {self.user_text.toPlainText()}'"}
                    ]
                )
                reply = chat_completion.choices.message.content
                play_sound('make_answer.mp3')
                self.answer_II.setText(reply)
                self.button_give_text.setEnabled(True)
            except:
                play_sound('make_answer.mp3')
                self.answer_II.setText('Ошибка! Проверьте ваш api ключ и соеденение с интернетом!')
                self.button_give_text.setEnabled(True)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите текст перед отправкой!')
            msg.show()
            msg.exec_()
            self.button_give_text.setEnabled(True)

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
            QTextEdit {
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
                """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
