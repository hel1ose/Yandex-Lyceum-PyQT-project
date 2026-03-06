from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

import sys

from base_info import InformationBase
from database import DataBase


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/Стартовое окно.ui', self)
        self.initUI()

    def initUI(self):
        self.downland_button.clicked.connect(self.downland)
        self.new_table_button.clicked.connect(self.info_window)

    def downland(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "(*.sqlite);;Все файлы (*)",
                                                   options=options)
        DataBase(fname)

    def info_window(self):
        self.hide()
        self.info = InformationBase()
        self.info.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())