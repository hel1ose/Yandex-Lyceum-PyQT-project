from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5 import uic

from errors import (FlagNotPressedError, EmptyTeacherListError, QuantitySubjectError, EmptySubjectListError,
                    EmptyClassesListError, error_message)
from database import DataBase
from basic_window import BasicWindow


class InformationBase(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/информация.ui', self)
        self.initUI()

    def initUI(self):
        self.back_button.clicked.connect(self.click)
        self.next_button.clicked.connect(self.click)
        self.save_info.clicked.connect(self.check)

        self.quantity_subject.setMinimum(0)
        self.back_button.setEnabled(False)

    def click(self):
        index = self.stackedWidget.currentIndex()
        if self.sender() == self.back_button and index != 0:
            self.stackedWidget.setCurrentIndex(index - 1)
        elif self.sender() == self.next_button and index != 4:
            self.stackedWidget.setCurrentIndex(index + 1)
        self.button_on_clicked(self.stackedWidget.currentIndex())

    def button_on_clicked(self, index):
        if index == 0:
            self.back_button.setEnabled(False)
        elif index == 4:
            self.next_button.setEnabled(False)
        else:
            self.back_button.setEnabled(True)
            self.next_button.setEnabled(True)

    def check(self):
        try:
            if not(self.checkBox.isChecked() or self.checkBox2.isChecked() or self.checkBox3.isChecked() or
                   self.checkBox4.isChecked() or self.checkBox5.isChecked() or self.checkBox6.isChecked() or
                   self.checkBox7.isChecked()):
                raise FlagNotPressedError('Вы не ответили на первый вопрос')
            elif len(list(filter(lambda x: len(x) > 0, self.list_teachers.toPlainText().split('\n')))) == 0:
                raise EmptyTeacherListError('Список преподавателей пуст')
            elif len(list(filter(lambda x: len(x) > 0, self.list_subjects.toPlainText().split('\n')))) == 0:
                raise EmptySubjectListError('Список предметов пуст')
            elif len(list(filter(lambda x: len(x) > 0, self.list_classes.toPlainText().split('\n')))) == 0:
                raise EmptySubjectListError('Список классов/групп пуст')
            elif self.quantity_subject.value() == 0:
                raise QuantitySubjectError('Не выбрано максимальное количество уроков в день')
            self.add_data()
        except FlagNotPressedError as error:
            error_message(error)
        except EmptyTeacherListError as error:
            error_message(error)
        except QuantitySubjectError as error:
            error_message(error)
        except EmptySubjectListError as error:
            error_message(error)
        except EmptyClassesListError as error:
            error_message(error)

    def add_data(self):
        db = DataBase('mydatabase.sqlite')
        db.create_db()
        group = [self.checkBox, self.checkBox2, self.checkBox3, self.checkBox4, self.checkBox5, self.checkBox6,
                 self.checkBox7]
        week_days = [widget.text() for widget in group if widget.isChecked() is True]
        list_teachers = list(filter(lambda x: len(x) > 0, self.list_teachers.toPlainText().split('\n')))
        list_subjects = list(filter(lambda x: len(x) > 0, self.list_subjects.toPlainText().split('\n')))
        list_classes = list(filter(lambda x: len(x) > 0, self.list_classes.toPlainText().split('\n')))
        max_subject_in_day = self.quantity_subject.value()
        db.add_data(week_days, list_teachers, list_subjects, list_classes, max_subject_in_day)
        self.basic_window(db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day)

    def basic_window(self,db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day):
        self.w = BasicWindow(db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day)
        self.w.show()
        self.hide()