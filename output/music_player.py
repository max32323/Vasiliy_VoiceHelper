from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QMessageBox, QVBoxLayout, QFileDialog, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import sqlite3
import voice

conn_mus = sqlite3.connect("music_list.db")
cursor_mus = conn_mus.cursor()

conn_path = sqlite3.connect("user_path.db")
cursor_path = conn_path.cursor()
cursor_path.execute("SELECT * FROM your_path")
path_image = cursor_path.fetchall()

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()


cursor_mus.execute("""
    CREATE TABLE IF NOT EXISTS list (
    name TEXT,
    id INTEGER
    )
""")

def check():
    global cursor_mus
    cursor_mus.execute("SELECT * FROM list")
    all = cursor_mus.fetchall()
    if all:
        return all[0][0]
    else:
        return ''

class Window(QWidget):
    def __init__(self):
        global path_image
        super().__init__()
        self.path_mus = check()
        print(self.path_mus)
        self.number_mus = 0
        self.setWindowTitle("Музыкальный проигрыватель")
        self.setWindowIcon(QIcon(f'{path_image[0][0]}\image\music.jpg'))
        self.setFixedSize(600, 400)
        self.player = QMediaPlayer()
        self.initUI()
        self.style()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.list_music = QTextEdit()
        self.list_music.setReadOnly(True)
        main_layout.addWidget(self.list_music)
        # self.update_music_list()
        self.set_music()

        self.layout_button = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add)
        self.add_button.setToolTip("Нажмите, чтобы добавить песню в плей лист")
        self.layout_button.addWidget(self.add_button)

        self.del_button = QPushButton("Удалить")
        self.del_button.clicked.connect(self.delete)
        self.del_button.setToolTip("Нажмите, чтобы удалить песню из плей листа")
        self.layout_button.addWidget(self.del_button)

        self.found_button = QPushButton("Выбрать")
        self.found_button.clicked.connect(self.choose)
        self.found_button.setToolTip("Нажмите, чтобы выбрать песню из плей листа")
        self.layout_button.addWidget(self.found_button)

        main_layout.addLayout(self.layout_button)

        self.play_sound = QPushButton("Прослушать песню")
        self.play_sound.clicked.connect(self.play)
        self.play_sound.setToolTip("Нажмите, чтобы прослушать выбранную песню")
        main_layout.addWidget(self.play_sound)

        self.layout_option_sound = QHBoxLayout()

        self.stop_sound = QPushButton("Остановить песню")
        self.stop_sound.clicked.connect(self.stop)
        self.stop_sound.setToolTip("Нажмите, чтобы остановить песню из плей листа")
        self.layout_option_sound.addWidget(self.stop_sound)

        self.pause_sound = QPushButton("Поставить на паузу")
        self.pause_sound.clicked.connect(self.pause)
        self.pause_sound.setToolTip("Нажмите, чтобы поставить на паузу")
        self.layout_option_sound.addWidget(self.pause_sound)

        main_layout.addLayout(self.layout_option_sound)

        self.leave = QPushButton('Выйти')
        self.leave.setToolTip('Нажмите, чтобы выйти')
        self.leave.clicked.connect(self.exit)
        main_layout.addWidget(self.leave)

    def exit(self):
        voice.speaker('До встречи')
        sys.exit()

    def add(self):
        global cursor_mus, conn_mus
        self.path_mus = QFileDialog.getOpenFileName(filter="Music (*.mp3 *.wav)")[0]
        cursor_mus.execute("SELECT * FROM list")
        all_records = cursor_mus.fetchall()
        if not all_records:
            new_id = 1
        else:
            new_id = all_records[-1][1] + 1
        if self.path_mus:
            cursor_mus.execute("INSERT INTO list VALUES (?,?)", (self.path_mus, new_id))
            conn_mus.commit()
            # self.update_music_list()
            self.set_music()
        self.path_mus = ''

    def delete(self):
        global cursor_mus, conn_mus
        cursor_mus.execute("SELECT * FROM list")
        all = cursor_mus.fetchall()
        if str(all) != "[]":
            n = 0
            text = self.list_music.toPlainText().split('\n')
            print(text)
            for i in text:
                if "✅" in i:
                    self.number_mus = n
                    break
                n += 1

            cursor_mus.execute("""DELETE FROM list WHERE name=(?)""",(text[self.number_mus][2:],))
            conn_mus.commit()
            self.set_music()
            cursor_mus.execute("SELECT * FROM list")
            all_2 = cursor_mus.fetchall()
            n = 1
            print('ок')
            if all_2:
                for i in all:
                    if i[0] == all_2[n-1][0]:
                        cursor_mus.execute("UPDATE list SET id=? WHERE name=?", (n, i[0],))
                        conn_mus.commit()
                        n += 1
            voice.speaker('Песня была удалена')

    def play(self):
        global cursor_mus, conn_mus
        cursor_mus.execute("SELECT * FROM list")
        all = cursor_mus.fetchall()
        if not all:
            w = QMessageBox()
            w.setWindowIcon(QIcon(f'{path_image[0][0]}\image\music.jpg'))
            w.setWindowTitle('Внимание!')
            w.setIcon(QMessageBox.Warning)
            w.setText('Пожалуйста, добавьте музыку и выберете её')
            w.show()
            w.exec_()
        else:
            list_musics = self.list_music.toPlainText().split('\n')
            for i in list_musics:
                if '✅' in i:
                    self.path_mus = i[2:]
            url = QUrl(self.path_mus)
            cont = QMediaContent(url)
            self.player.setMedia(cont)
            self.player.play()

    def stop(self):
        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl('')))

    def pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def choose(self):
        global cursor_mus
        cursor_mus.execute("SELECT * FROM list")
        all = cursor_mus.fetchall()
        if all:
            full = len(all)
            if self.number_mus+1 == full:
                self.number_mus = 0
            else:
                self.number_mus += 1
            self.path_mus = all[self.number_mus][0]
            print(self.path_mus)
            self.set_music()

    def set_music(self):
        global cursor_mus
        cursor_mus.execute("SELECT * FROM list")
        all = cursor_mus.fetchall()
        if all:
            text = "\n".join(rec[0] for rec in all).split('\n')
            print(text)
            text[self.number_mus] = "✅ "+text[self.number_mus]
            text_norm = '\n'.join(i for i in text)

            self.list_music.setText(text_norm)
        else:
            self.list_music.setText('')

    def style(self):
        global cursor_color, connect_color
        cursor_color.execute("""SELECT * FROM color_menu""")
        all = cursor_color.fetchall()
        print(all)
        if not all:
            self.setStyleSheet("""
            QWidget {
                background-color: #00BFFF;
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
                font-size: 16px;
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
                    font-size: 16px;
                    border: 3px solid #E9967A;
                    border-radius: 10px;
            }
                """)
            elif rand == 'green':
                self.setStyleSheet("""
                QWidget {
                    background-color: #32CD32;
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
                    font-size: 16px;
                    border: 3px solid #90EE90;
                    border-radius: 10px;
            }
                """)
            elif rand == 'dark':
                self.setStyleSheet("""
                QWidget {
                    background-color: #696969;
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
                    font-size: 16px;
                    border: 3px solid #C0C0C0;
                    border-radius: 10px;
            }
                """)
            elif rand == 'pink':
                self.setStyleSheet("""
                QWidget {
                    background-color: #C71585;
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
                    font-size: 16px;
                    border: 3px solid #FF69B4;
                    border-radius: 10px;
            }
                """)
            elif rand == 'brown':
                self.setStyleSheet("""
                QWidget {
                    background-color: #A52A2A;
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
                    font-size: 16px;
                    border: 3px solid #B8860B;
                    border-radius: 10px;
            }
                """)
            elif rand == 'violet':
                self.setStyleSheet("""
                QWidget {
                    background-color: #9932CC;
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
                    font-size: 16px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
            }
                """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())