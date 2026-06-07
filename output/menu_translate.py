import sqlite3
from translate import Translator
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import sys
import pyperclip as pyp

import voice

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()


connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('| Переводчик:')
        self.setFixedSize(550,350)
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\ptransate_icon.png'))
        self.initUI()
    def initUI(self):
        self.user_label = QLabel('| Текст:')
        self.user_text = QLineEdit(self)

        self.answer_text = QLineEdit(self)
        self.answer_text.setReadOnly(True)
        self.answer_label = QLabel('| Перевод')


        self.combo_user_label = QLabel('| Исходный текст:')
        self.combo_user = QComboBox(self)
        to = [
            'en English',
            'af Afrikaans',
            'am Amharic',
            'ar Arabic',
            'az Azerbaijani',
            'be Belarusian',
            'bg Bulgarian',
            'bn Bengali',
            'bs Bosnian',
            'ca Catalan',
            'ceb Cebuano',
            'co Corsican',
            'cs Czech',
            'cy Welsh',
            'da Danish',
            'de German',
            'el Greek',
            'eo Esperanto',
            'es Spanish',
            'et Estonian',
            'eu Basque',
            'fa Persian',
            'fi Finnish',
            'fr French',
            'fy Frisian',
            'ga Irish',
            'gd Scots Gaelic',
            'gl Galician',
            'gu Gujarati',
            'ha Hausa',
            'haw Hawaiian',
            'hi Hindi',
            'hmn Hmong',
            'hr Croatian',
            'ht Haitian Creole',
            'hu Hungarian',
            'hy Armenian',
            'id Indonesian',
            'ig Igbo',
            'is Icelandic',
            'it Italian',
            'he Hebrew',
            'ja Japanese',
            'jv Javanese',
            'ka Georgian',
            'kk Kazakh',
            'km Khmer',
            'kn Kannada',
            'ko Korean',
            'ku Kurdish',
            'ky Kyrgyz',
            'la Latin',
            'lb Luxembourgish',
            'lo Lao',
            'lt Lithuanian',
            'lv Latvian',
            'mg Malagasy',
            'mi Maori',
            'mk Macedonian',
            'ml Malayalam',
            'mn Mongolian',
            'mr Marathi',
            'ms Malay',
            'mt Maltese',
            'my Burmese',
            'ne Nepali',
            'nl Dutch',
            'no Norwegian',
            'ny Chichewa',
            'or Oriya',
            'pa Punjabi',
            'pl Polish',
            'ps Pashto',
            'pt Portuguese',
            'ro Romanian',
            'ru Russian',
            'sd Sindhi',
            'si Sinhala',
            'sk Slovak',
            'sl Slovenian',
            'sm Samoan',
            'sn Shona',
            'so Somali',
            'sq Albanian',
            'sr Serbian',
            'st Sesotho',
            'su Sundanese',
            'sv Swedish',
            'sw Swahili',
            'ta Tamil',
            'te Telugu',
            'tg Tajik',
            'th Thai',
            'tl Filipino',
            'tr Turkish',
            'ug Uyghur',
            'uk Ukrainian',
            'ur Urdu',
            'uz Uzbek',
            'vi Vietnamese',
            'xh Xhosa',
            'yi Yiddish',
            'yo Yoruba',
            'zh Chinese',
            'zu Zulu'
        ]
        self.combo_user.addItems(to)
        self.combo_user.setFixedSize(370,20)

        self.combo_answer_label = QLabel('| Перевод текста:')
        self.combo_answer = QComboBox(self)
        self.combo_answer.addItems(to)
        self.combo_answer.setFixedSize(370,20)

        self.button_clear = QPushButton('Очистка текста')
        self.button_clear.clicked.connect(self.clear)

        self.button_copy = QPushButton('Копировать перевод')
        self.button_copy.clicked.connect(self.copy)

        self.button_exit = QPushButton('Выход')
        self.button_exit.clicked.connect(self.exit)
        self.button_tr = QPushButton('Перевести текст')
        self.button_tr.clicked.connect(self.transl)

        self.pictures = QLabel(self)
        self.pix = QPixmap(f'{path[0][0]}\image\ptransate_menu.jpg')
        self.pictures.setPixmap(self.pix.scaled(200,160))


        self.pix_label = QLabel('| Добро пожаловать в переводик!', self)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()

        hbox.addWidget(self.combo_user_label)
        hbox.addWidget(self.combo_user)

        hbox2.addWidget(self.user_label)
        hbox2.addWidget(self.user_text)


        hbox3.addWidget(self.button_clear)
        hbox3.addWidget(self.button_tr)
        hbox3.addWidget(self.button_copy)

        hbox4.addWidget(self.answer_label)
        hbox4.addWidget(self.answer_text)

        hbox5.addWidget(self.combo_answer_label)
        hbox5.addWidget(self.combo_answer)

        hbox6.addWidget(self.pictures)
        hbox6.addWidget(self.pix_label)

        vbox.addLayout(hbox6)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.button_exit)

        self.setLayout(vbox)
        self.check_color()

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
                font-size: 14px;
                border: 2px solid;
                border-radius: 7px;
            }   
            QLineEdit {
                font: Arial;
                font-size: 14px;
                border: 3px solid #E0FFFF;
                border-radius: 10px;
            }
            QRadioButton {
                font-size: 14px;
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
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                }   
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #E9967A;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                } 
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #006400;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                } 
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid black;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                } 
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #C71585;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid black;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
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
                    font-size: 14px;
                    border: 2px solid;
                    border-radius: 7px;
                } 
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #4B0082;
                    border-radius: 10px;
                }
                QRadioButton {
                    font-size: 14px;
                }
                """)

    def transl(self):
        try:
            user_lang = self.combo_user.currentText().split()[0]
            answer_lang = self.combo_answer.currentText().split()[0]
            translator = Translator(from_lang=str(user_lang), to_lang=str(answer_lang))
            text = str(self.user_text.text())
            answer = str(translator.translate(text))
            self.answer_text.setText(str(answer))
            voice.speaker("Фраза была переведена!")
        except:
            voice.speaker("Ошибка! Попробуйте позже или проверьте соединение с интернетом!")

    def exit(self):
        sys.exit()
    def clear(self):
        self.user_text.clear()
        self.answer_text.clear()

    def copy(self):
        text = self.answer_text.text()
        voice.speaker('Скопировал ваш перевод!')
        pyp.copy(text)
        self.answer_text.setText('Текст скопирован!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())



