import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import pyperclip, voice
from g4f import ChatCompletion
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
        num_error = 0
        self.button_give_text.setEnabled(False)
        if self.user_text.toPlainText().strip() != '':
            play_sound('went.mp3')
            self.answer_II.clear()
            with open(f'{path[0][0]}\my_name', 'r', encoding='utf-8') as file:
                name = file.read()
                if name == '':
                    name = 'Неизвестная личность'

            while True:
                response: str = ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": (
                        f"Твоего пользователя зовут {name}. Ты добрый человек который готов помочь пользователю ответить на любой вопрос. Страрайся давать ответ на русском языке")},
                              {"role": "user", "content": f'Ты - Василий, а твоего пользователя зовут {name}. Запрос: {self.user_text.toPlainText()}'}],
                )
                print(response)
                if response == '流量异常,请尝试更换网络环境' or response == 'Model not found or too long input. Or any other error (xD)' or response == 'Too many messages in a row' or response == 'Request ended with status code 404' or response == 'No message received':
                    pass
                elif response == 'sorry, 您的ip已由于触发防滥用检测而被封禁,本服务网址是https://chat18.aichatos8.com 或者 https://cat.chatavx.com/ 如果你不在本网站，请前往本网站使用即可 如需合作接口调用请联系微信kelemm220 或者前往 https://binjie09.shop 自助购买key, 认为是误封需要解封的请前往https://www.ip.cn/ 查询ip信息,并发送信息至邮件 gpt33@binjie.site ，站长会定期看邮件并处理解封和合作问题，如需调用接口请见接口文档https://apifox.com/apidoc/shared-803d9df6-a071-4b3e-9d69-ea1281614d82，如需合作接口调用请联系微信chatkf123 或者前往 https://cat.chatavx.com/  注册使用（可付费使用gpt4 注册可免费使用3.5）' or "sorry" in response:
                    pass
                elif 'простите' in response.lower() or 'извините' in response.lower():
                    num_error += 1
                    if num_error >= 6:
                        play_sound('make_answer.mp3')
                        self.answer_II.setText(response)
                        break
                else:
                    play_sound('make_answer.mp3')
                    self.answer_II.setText(response)
                    break
            self.button_give_text.setEnabled(True)
            num_error = 0

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
