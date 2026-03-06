from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5 import uic


class BasicWindow(QWidget):
    def __init__(self, db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day):
        super().__init__()
        uic.loadUi('./ui/проектUI.ui', self)
        self.initUI(db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day)

    def initUI(self, db, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day):
        self.week_days, self.list_teachers = week_days, list(sorted(list_teachers))
        self.list_subjects, self.db = list(sorted(list_subjects)), db
        self.list_classes, self.max_subject_in_day = list_classes, max_subject_in_day
        self.object_classes = {}
        self.create_db_table()
        self.create_teachers_table()
        self.create_schedule_table()
        self.create_classes_table()
        self.db_table_save_info.clicked.connect(self.add_info)
        #  self.db_table_edit_info.clicked.connect()
        #  self.db_table_save_table.clicked.connect()
        self.check_boxes()

    def create_classes_table(self):
        for elem in self.list_classes:
            table = QTableWidget()
            table.setHorizontalHeaderLabels(self.week_days)
            self.classes_table.addTab(table, elem)
            self.object_classes[elem] = table

    def create_teachers_table(self):
        for elem in self.week_days:
            self.teachers_comboBox.addItem(elem)
        n_subject = [str(n) for n in range(1, self.max_subject_in_day + 1)]
        self.teachers_table.setHorizontalHeaderLabels(['id', 'teacher'] + n_subject)

    def create_schedule_table(self):
        for elem in self.week_days:
            self.schedule_comboBox.addItem(elem)
        self.teachers_table.setHorizontalHeaderLabels(self.list_classes)

    def create_db_table(self):
        self.db_table.setColumnCount(6)
        self.db_table.setRowCount(0)
        header = ['id', 'класс', 'преподаватель', 'предмет', 'день недели', 'номер урока']
        self.db_table.setHorizontalHeaderLabels(header)

    def check_boxes(self):
        # self.db_table_teacher.clear()
        [self.db_table_teacher.addItem(elem) for elem in self.list_teachers]

        # self.db_table_class.clear()
        [self.db_table_class.addItem(elem) for elem in self.list_classes]

        # self.db_table_subject.clear()
        [self.db_table_subject.addItem(elem) for elem in self.list_subjects]

        # self.db_table_week_day.clear()
        [self.db_table_week_day.addItem(elem) for elem in self.week_days]

        # self.db_table_lesson_number.clear()
        number_lessons = [str(n) for n in range(1, self.max_subject_in_day + 1)]
        [self.db_table_lesson_number.addItem(elem) for elem in number_lessons]

    def add_info(self):
        row = self.db_table.rowCount()
        class_elem, teacher = self.db_table_class.currentText(), self.db_table_teacher.currentText()
        subject, week_day = self.db_table_subject.currentText(), self.db_table_week_day.currentText()
        lesson_number = self.db_table_lesson_number.currentText()

        self.db_table.setRowCount(row + 1)
        self.db_table.setItem(row, 0, QTableWidgetItem(row + 1))
        self.db_table.setItem(row, 1, QTableWidgetItem(class_elem))
        self.db_table.setItem(row, 2, QTableWidgetItem(teacher))
        self.db_table.setItem(row, 3, QTableWidgetItem(subject))
        self.db_table.setItem(row, 4, QTableWidgetItem(week_day))
        self.db_table.setItem(row, 5, QTableWidgetItem(lesson_number))

        id_class, id_teacher = self.db.get_id_class(class_elem), self.db.get_id_teacher(teacher)
        id_subject = self.db.get_id_subject(subject)
        self.db.data_from_table(id_class, id_teacher, id_subject, week_day, lesson_number)



