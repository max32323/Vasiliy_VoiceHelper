import random
import sys
import voice
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_point = sqlite3.connect('play_game.db')
cursor_point = connect_point.cursor()

cursor_point.execute(
    """
    CREATE TABLE IF NOT EXISTS rock_paper_scissors 
    (
    points_user INTEGER,
    id INTEGER
    )
    """
)


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
        self.play_game = False
        self.points_bot = 0
        self.points_player = 0
        self.list_motions = ['Камень', 'Ножницы', 'Бумага']
        self.dict_motions = {'Камень': 'stone.png', 'Ножницы': 'nox.png', 'Бумага': 'paper.png'}


        self.setWindowIcon(QIcon('game_images/igra.jpg'))
        self.setWindowTitle('Камень, ножницы, бумага')
        self.setFixedSize(400,350)
        self.initUI()
        self.check_color()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        layout_image = QHBoxLayout()

        self.image_user = QLabel('Вы')
        self.image_user.setAlignment(Qt.AlignCenter)
        self.image_user.setPixmap(QPixmap(f'game_images/igra.jpg').scaled(150, 150))
        layout_image.addWidget(self.image_user)

        self.image_bot = QLabel('Бот')
        self.image_bot.setAlignment(Qt.AlignCenter)
        self.image_bot.setPixmap(QPixmap(f'game_images/igra.jpg').scaled(150, 150))
        layout_image.addWidget(self.image_bot)

        main_layout.addLayout(layout_image)

        self.label_play = QLabel('Счёт 0 : 0')
        self.label_play.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_play)

        cursor_point.execute("""SELECT * FROM rock_paper_scissors""")
        all = cursor_point.fetchall()
        print(all)
        if str(all) == '[]':
            all = 0
        else:
            all = all[0][0]


        self.label_global_points = QLabel(f"Всего побед за все игры: {all}")
        main_layout.addWidget(self.label_global_points)

        layout_user_motion = QHBoxLayout()

        self.label_info = QLabel('Выберете знак:')
        layout_user_motion.addWidget(self.label_info)

        self.combo_element = QComboBox()
        self.combo_element.setFixedSize(240,20)
        self.combo_element.addItems(['Камень', 'Ножницы', 'Бумага'])
        layout_user_motion.addWidget(self.combo_element)

        main_layout.addLayout(layout_user_motion)

        self.button_motion = QPushButton('Проходить')
        self.button_motion.setEnabled(False)
        self.button_motion.clicked.connect(self.play)
        main_layout.addWidget(self.button_motion)

        self.button_start = QPushButton('Начать игру')
        self.button_start.clicked.connect(self.start)
        main_layout.addWidget(self.button_start)

        self.button_exit = QPushButton('Выход')
        self.button_exit.clicked.connect(self.leave)
        main_layout.addWidget(self.button_exit)


    def leave(self):
        sys.exit()

    def start(self):
        self.label_play.setText('Счёт 0 : 0')
        self.play_game = True
        self.button_start.setEnabled(False)
        self.button_motion.setEnabled(True)
        play_sound('make_text_n.mp3')

    def play(self):
        player_motion: str = self.combo_element.currentText()
        bot_motion: str = random.choice(self.list_motions)

        print(self.points_player)
        print(self.points_bot)

        if bot_motion == player_motion:
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif bot_motion == 'Камень' and player_motion == 'Бумага':
            self.points_player += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif bot_motion == 'Ножницы' and player_motion == 'Камень':
            self.points_player += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif bot_motion == 'Бумага' and player_motion == 'Ножницы':
            self.points_player += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif player_motion == 'Камень' and bot_motion == 'Бумага':
            self.points_bot += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif player_motion == 'Ножницы' and bot_motion == 'Камень':
            self.points_bot += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')
        elif player_motion == 'Бумага' and bot_motion == 'Ножницы':
            self.points_bot += 1
            self.label_play.setText(f'Счёт {self.points_player} : {self.points_bot}')

        for key, values in self.dict_motions.items():
            if key == bot_motion:
                self.image_bot.setPixmap(QPixmap(f'game_images/{values}').scaled(150, 150))
            if key == player_motion:
                self.image_user.setPixmap(QPixmap(f'game_images/{values}').scaled(150, 150))

        if self.points_player >= 3:
            voice.speaker('Поздравляю вас с победой!')
            self.play_game = False
            cursor_point.execute("""SELECT * FROM rock_paper_scissors""")
            all = cursor_point.fetchall()
            print(all)
            if str(all) == '[]':
                cursor_point.execute("""INSERT INTO rock_paper_scissors VALUES (?, ?)""", (1, 0))
                connect_point.commit()
                p = 1
                self.label_global_points.setText(f"Всего побед за все игры: {p}")
            else:
                print(all[0][0])
                p = int(all[0][0]) + 1
                self.label_global_points.setText(f"Всего побед за все игры: {p}")
                cursor_point.execute("""UPDATE rock_paper_scissors SET points_user=? WHERE id=?""", (p,0))
                connect_point.commit()

        elif self.points_bot >= 3:
            voice.speaker('Вы проиграли, удачи в следующей игре!')
            self.play_game = False

        if not self.play_game:
            self.button_motion.setEnabled(False)
            self.button_start.setEnabled(True)
            self.points_player = 0
            self.points_bot = 0
            self.image_bot.setPixmap(QPixmap(f'game_images/igra.jpg').scaled(150, 150))
            self.image_user.setPixmap(QPixmap(f'game_images/igra.jpg').scaled(150, 150))


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
            QComboBox {
                background-color: #87CEEB;
                color: black;
                font: Arial;
                font-size: 16px;
                border: 2px solid;
                border-radius: 7px;
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
                QComboBox {
                    background-color: #F08080;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
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
                QComboBox {
                    background-color: #3CB371;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
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
                QComboBox {
                    background-color: #708090;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
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
                QComboBox {
                    background-color: #FF69B4;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
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
                QComboBox {
                    background-color: #EE82EE;
                    color: black;
                    font: Arial;
                    font-size: 16px;
                    border: 2px solid;
                    border-radius: 7px;
                }
                """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())