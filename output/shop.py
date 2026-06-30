import sqlite3
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QLineEdit, QRadioButton, \
    QMessageBox
from PyQt5.QtGui import QPixmap, QIntValidator, QDoubleValidator, QIcon
from PyQt5.QtCore import Qt
import voice


connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()

def exesise(kol, price):
    return kol*price


conn = sqlite3.connect('product_users.db')

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS product_user (
    product TEXT,
    count INTEGER,
    price REAL
    )
    """)


def connect(name, count, price):
    cursor.execute("""
    INSERT INTO product_user VALUES (?,?,?)
    """, (name, count, price))
    conn.commit()

def connect_file(name,count,price):
    with open('product.txt', 'a', encoding='utf-8') as file:
        file.write(f'Продукт: {name}\nКоличество: {count}\nЦена за всё: {price}\n')



class Shop(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Помощник составления списков продуктов')
        self.setFixedSize(500,400)
        self.setWindowIcon(QIcon(f'{path[0][0]}\image\ptransate_icon.png'))

        self.label_pix = QLabel()
        pix = QPixmap(f'{path[0][0]}\image\shop.jpg')
        self.label_pix.setPixmap(pix.scaled(300,180))
        self.label_pix.setAlignment(Qt.AlignCenter)


        self.line_product = QLineEdit()
        self.line_product.setPlaceholderText('Введите название продукта...')

        self.line_kol = QLineEdit()
        self.line_kol.setPlaceholderText('Введите количество продукта...')
        self.line_kol.setValidator(QIntValidator(1,1000000))

        self.line_price = QLineEdit()
        self.line_price.setPlaceholderText('Введите цену 1-го продукта(в рублях российских)...')
        self.line_price.setValidator(QDoubleValidator())

        self.button_save = QPushButton('Сохранить')
        self.button_save.clicked.connect(self.save_p)

        self.button_save_text1 = QRadioButton('Сохранить в базу данных')
        self.button_save_text2 = QRadioButton('Сохранить в файл txt')

        layout = QVBoxLayout()
        layout.addWidget(self.line_product)
        layout.addWidget(self.line_kol)
        layout.addWidget(self.line_price)
        layout.addWidget(self.button_save_text1)
        layout.addWidget(self.button_save_text2)
        layout.addWidget(self.button_save)

        line_widget = QWidget()
        line_widget.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_pix)
        main_layout.addWidget(line_widget)

        self.setLayout(main_layout)
        self.check_color()

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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #90EE90;
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #C0C0C0;
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #FF69B4;
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #B8860B;
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
                QLineEdit {
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
            }
                QRadioButton {
                    font-size: 14px;
                }
                """)






    def save_p(self):
        if self.line_product.text().strip() == '' or self.line_kol.text().strip() == '' or self.line_price.text().strip() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите все поля ввода!')
            msg.show()
            msg.exec_()
        else:
            name = self.line_product.text()
            kol = int(self.line_kol.text())

            n = self.line_price.text()
            if ',' in n:
                n1 = n.replace(',', '.')
            else:
                n1 = n
            price_all = exesise(kol, float(n1))
            if self.button_save_text1.isChecked():
                connect(name, kol, price_all)
                self.line_product.clear()
                self.line_kol.clear()
                self.line_price.clear()
                voice.speaker('Успешно сохранено в базу данных!')
            elif self.button_save_text2.isChecked():
                connect_file(name, kol, price_all)
                self.line_product.clear()
                self.line_kol.clear()
                self.line_price.clear()
                voice.speaker('Успешно сохранено в файл тииксти формата!')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Предупреждение!')
                msg.setText('Пожалуйста, выберете тип созранения!')
                msg.show()
                msg.exec_()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Shop()
    w.show()
    sys.exit(app.exec_())
