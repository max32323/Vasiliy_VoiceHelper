import sqlite3

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QApplication, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import file

connect_color = sqlite3.connect('color_main_menu.db')
cursor_color = connect_color.cursor()

cursor_color.execute(
    """
    CREATE TABLE IF NOT EXISTS color_menu (
    color TEXT
    )
    """
)


connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()
print(path[0][0])

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700,600)
        self.setWindowTitle("Генератор презентаций")
        self.initUI()
        self.check_color()
    def initUI(self):

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.setWindowIcon(QIcon('нужные картинки/generate.png'))

        layout_name_project = QHBoxLayout()

        self.label_name_project = QLabel("Название презентации: ")

        self.line_name_project = QLineEdit()
        self.line_name_project.setPlaceholderText("Введите название")
        self.line_name_project.setMaxLength(84)

        layout_name_project.addWidget(self.label_name_project)
        layout_name_project.addWidget(self.line_name_project)

        main_layout.addLayout(layout_name_project)

        layout_name_project2 = QHBoxLayout()

        self.label_name_aftor = QLabel("ФИО создателя презентации: ")

        self.line_name_aftor = QLineEdit()
        self.line_name_aftor.setPlaceholderText("Введите ФИО")
        self.line_name_aftor.setMaxLength(58)

        layout_name_project2.addWidget(self.label_name_aftor)
        layout_name_project2.addWidget(self.line_name_aftor)

        main_layout.addLayout(layout_name_project2)

        self.label_plan = QLabel("План презентации")
        self.label_plan.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_plan)

        self.line_plan = QTextEdit()
        self.line_plan.setFixedSize(676,350)
        main_layout.addWidget(self.line_plan)

        layout_button = QHBoxLayout()

        self.button_delete = QPushButton("Удалить данные")
        self.button_delete.clicked.connect(self.remove_all)

        self.button_generate = QPushButton("Сгенерировать")
        self.button_generate.clicked.connect(self.generate_presentation)

        self.button_exit = QPushButton("Выйти")
        self.button_exit.clicked.connect(self.leave)

        layout_file = QHBoxLayout()

        self.label_file_project = QLabel("Название файла: ")

        self.line_file_project = QLineEdit()
        self.line_file_project.setPlaceholderText("Введите название файла")
        self.line_file_project.setMaxLength(84)

        layout_file.addWidget(self.label_file_project)
        layout_file.addWidget(self.line_file_project)

        layout_button.addWidget(self.button_delete)
        layout_button.addWidget(self.button_generate)
        layout_button.addWidget(self.button_exit)

        main_layout.addLayout(layout_button)
        main_layout.addLayout(layout_file)

        self.check_path = QCheckBox('Сделать сохранение на рабочий стол?')

        main_layout.addWidget(self.check_path)



    def remove_all(self):
        self.line_name_project.clear()
        self.line_name_aftor.clear()
        self.line_plan.clear()

    def leave(self):
        sys.exit()

    def generate_presentation(self):
        if(self.line_plan.toPlainText().strip() !='' and self.line_name_project.text().strip()!=''):
            if self.line_file_project.text().strip() == '':
                file2 = 'example.pptx'
            elif '.pptx' in self.line_file_project.text().strip():
                file2 = self.line_file_project.text().strip()
            else:
                file2 = self.line_file_project.text().strip() + '.pptx'
            plan = self.line_plan.toPlainText().strip().split('\n')
            name = self.line_name_project.text().strip()
            aftor = self.line_name_aftor.text().strip()
            if aftor == '':
                with open(f'{path[0][0]}\my_name', 'r', encoding='utf-8') as f:
                    aftor = f.read()
                    if aftor.strip() == '':
                        aftor = 'Неизвестно'
            if self.check_path.isChecked():
                file.generate_presintation(str(name), aftor, plan, file2, True)
            else:
                file.generate_presintation(name, aftor, plan, file2, False)

        else:
            msg = QMessageBox()
            # msg.setWindowIcon(QIcon('image/yy.png'))
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Предупреждение!')
            msg.setText('Пожалуйста, введите название и план презентации!')
            msg.show()
            msg.exec_()


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
            QTextEdit {
                color: white;
                font: Arial;
                font-size: 14px;
                border: 3px solid #E0FFFF;
                border-radius: 10px;
            }
            QCheckBox {
                color: black;
                font: Arial;
                font-size: 18px;
            }

            """)
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #E0FFFF;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: black;
                    font: Arial;
                    font-size: 18px;
                }
                """)
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #E9967A;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: black;
                    font: Arial;
                    font-size: 18px;
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #90EE90;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: black;
                    font: Arial;
                    font-size: 18px;
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #C0C0C0;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: write;
                    font: Arial;
                    font-size: 18px;
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #FF69B4;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: black;
                    font: Arial;
                    font-size: 18px;
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #B8860B;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: white;
                    font: Arial;
                    font-size: 18px;
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
                QTextEdit {
                    color: white;
                    font: Arial;
                    font-size: 14px;
                    border: 3px solid #BA55D3;
                    border-radius: 10px;
                }
                QCheckBox {
                    color: black;
                    font: Arial;
                    font-size: 18px;
                }
                """)



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
