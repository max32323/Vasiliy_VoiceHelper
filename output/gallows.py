from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from  PyQt5.QtCore import Qt
import sys
import sqlite3
import random
import pygame

def play_sound(sound: str):
    pygame.init()
    sound_file = sound
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(0.5)
    sound.play()
    while pygame.mixer.get_busy():
        continue
    pygame.quit()


connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()


def get_word():
    words = [
        'лист', 'холод', 'стадион', 'туман', 'телевизор', 'игра', 'шепот', 'счастье', 'море', 'сила', 'тепло',
        'болезнь', 'семя', 'свет', 'вражда', 'улица', 'школа', 'банан', 'аромат', 'свобода', 'солнце', 'дерево', 'кафе',
        'врач', 'кинотеатр', 'год', 'планшет', 'друг', 'ложь', 'смех', 'взгляд', 'сон', 'жизнь', 'радуга', 'тишина',
        'секунда', 'покой', 'время', 'боль', 'облако', 'дружба', 'проблема', 'звезда', 'животное', 'идея', 'эхо',
        'город', 'молния', 'корень', 'гостиница', 'ритм', 'аэропорт', 'ночь', 'начало', 'плод', 'интернет', 'гора',
        'победа', 'яблоко', 'поезд', 'грусть', 'минута', 'поражение', 'груша', 'плач', 'учитель', 'самокат', 'птица',
        'опыт', 'парк', 'дом', 'река', 'камень', 'запах', 'радость', 'деревня', 'мир', 'ветер', 'выставка', 'магазин',
        'голос', 'танец', 'урок', 'навык', 'ддорога', 'ягода', 'песок', 'телефон', 'вечер', 'работа', 'ощущение',
        'ответ', 'рыба', 'тьма', 'решение', 'земля', 'цель', 'шум', 'мелодия', 'любовь', 'утро', 'машина', 'рабство',
        'план', 'музей', 'песня', 'умение', 'зло', 'кино', 'вкус', 'путь', 'цвет', 'насекомое', 'папа', 'час',
        'компьютер', 'день', 'пациент', 'добро', 'звук', 'лекарство', 'улыбка', 'театр', 'мечта', 'больница', 'жест',
        'библиотека', 'здоровье', 'крик', 'вопрос', 'конец', 'отдых', 'лес', 'снег', 'тень', 'гроза', 'цветок', 'мама',
        'велосипед', 'автобус', 'книга', 'чувство', 'знание', 'бодрствование', 'небо', 'вода', 'спорт', 'куст', 'трава',
        'правда', 'музыка', 'огонь', 'воздух', 'лечение', 'вокзал', 'слабость', 'мысль', 'движение', 'война',
        'ресторан', 'дождь', 'смерть'
    ]
    return random.choice(words)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.bool_game = False
        self.bool_win = False
        self.word = get_word()
        self.pop = 9
        self.index = 0
        self.word_password = str('_ ' * len(self.word)).strip()
        self.syms_password = self.word_password.split(' ')

        self.setWindowTitle('Виселица')
        self.setWindowIcon(QIcon('game_images/vis.png'))
        self.setFixedSize(350,300)
        self.initUI()
        self.check_color()


    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.label_text = QLabel('Угадай слово')
        self.label_text.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.label_text)

        self.label_word = QLabel(f'Ваше слово: ')
        main_layout.addWidget(self.label_word)

        self.user_answer = QLabel(f'Статус угадывания: ')
        main_layout.addWidget(self.user_answer)

        self.label_pop = QLabel(f'Количество попыток: {self.pop+1}')
        main_layout.addWidget(self.label_pop)


        layout_user = QHBoxLayout()

        self.label_user = QLabel('Введите букву:')
        layout_user.addWidget(self.label_user)

        self.line_user = QLineEdit()
        self.line_user.setPlaceholderText('Введите букву(русскую)')
        self.line_user.setEnabled(False)

        layout_user.addWidget(self.line_user)
        layout_user.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(layout_user)

        self.button_check = QPushButton('Проверить')
        self.button_check.clicked.connect(self.check)
        self.button_check.setEnabled(False)
        main_layout.addWidget(self.button_check)

        self.button_start = QPushButton('Начать')
        self.button_start.clicked.connect(self.start)
        main_layout.addWidget(self.button_start)

        self.button_exit = QPushButton('Выход')
        self.button_exit.clicked.connect(self.exit)
        main_layout.addWidget(self.button_exit)

    def exit(self):
        sys.exit()

    def start(self):
        play_sound('click.mp3')
        self.line_user.setEnabled(True)
        self.button_check.setEnabled(True)
        self.button_start.setEnabled(False)
        self.bool_game = True
        self.bool_win = False
        self.word = get_word()
        self.word_password = str('_ ' * len(self.word)).strip()
        self.syms_password = self.word_password.split(' ')

        self.label_pop.setText(f'Количество попыток: {self.pop + 1}')
        self.label_word.setText(f'Ваше слово: {self.word_password}')
        self.user_answer.setText('Статус угадывания:')

    def check(self):
        play_sound('click.mp3')
        if self.bool_game and self.pop != 0:
            print(self.syms_password)
            if self.line_user.text().strip().lower() == self.word[self.index]:
                self.user_answer.setText('Статус угадывания: Вы угадали!')
                self.syms_password[self.index] = self.word[self.index]
                word = ''.join(self.syms_password)
                self.label_word.setText(f'Ваше слово: {word}')
                self.pop += 3
                self.label_pop.setText(f'Количество попыток: {self.pop + 1}')
                self.index += 1
                self.check_word()
                self.line_user.clear()
            else:
                self.user_answer.setText('Статус угадывания: Вы не угадали!')
                self.pop -= 1
                self.label_pop.setText(f'Количество попыток: {self.pop+1}')
                self.line_user.clear()
        else:
            self.check_word()

    def check_word(self):
        if ''.join(self.syms_password) == self.word:
            self.bool_win = True
            self.bool_game = False
            self.user_answer.setText('Статус угадывания: Вы прошли!')
            self.index = 0
            self.line_user.clear()
            self.line_user.setEnabled(False)
            self.button_check.setEnabled(False)
            self.button_start.setEnabled(True)
        elif self.pop == 0:
            self.bool_win = False
            self.bool_game = False
            self.label_pop.setText(f'Количество попыток: {self.pop}')
            self.user_answer.setText('Статус угадывания: Вы проиграли!')
            self.index = 0
            self.line_user.clear()
            self.line_user.setEnabled(False)
            self.button_check.setEnabled(False)
            self.button_start.setEnabled(True)
            self.pop = 9

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())