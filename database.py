import sqlite3

from errors import UnsuitableDataBaseError, error_message


class DataBase:
    def __init__(self, fname):
        self.fname = fname

    def open_db(self):
        self.conn = sqlite3.connect(self.fname)
        self.cursor = self.conn.cursor()
        try:
            if (len(self.cursor.execute('''SELECT * FROM base_information''').fetchall()) == 0 or
                    len(self.cursor.execute('''SELECT * FROM classes''').fetchall()) == 0 or
                    len(self.cursor.execute('''SELECT * FROM teachers''').fetchall()) == 0 or
                    len(self.cursor.execute('''SELECT * FROM subject''').fetchall()) or
                    len(self.cursor.execute('''SELECT * FROM table_information''').fetchall())):
                raise UnsuitableDataBaseError
        except UnsuitableDataBaseError:
            error_message('Данная таблица данных не подходит для работы приложения')

    def create_db(self):
        self.conn = sqlite3.connect(self.fname)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''DROP TABLE IF EXISTS base_information''')
        self.cursor.execute('''DROP TABLE IF EXISTS classes''')
        self.cursor.execute('''DROP TABLE IF EXISTS teachers''')
        self.cursor.execute('''DROP TABLE IF EXISTS subjects''')
        self.cursor.execute('''DROP TABLE IF EXISTS table_information''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS base_information
                                (week_days TEXT,
                                max_subject_in_day INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS classes
                                (id INTEGER PRIMARY KEY,
                                class TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS teachers
                                (id INTEGER PRIMARY KEY,
                                teacher TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subjects
                                (id INTEGER PRIMARY KEY,
                                subject TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS table_information 
                                (id INTEGER PRIMARY KEY,
                                idclass INTEGER,
                                idteacher INTEGER,
                                idsubject INTEGER,
                                lesson_number INTEGER, 
                                week_day TEXT)''')
        self.conn.commit()

    def add_data(self, week_days, list_teachers, list_subjects, list_classes, max_subject_in_day):
        week_days = ', '.join(week_days)
        self.cursor.execute(f'''INSERT INTO base_information(week_days, max_subject_in_day) 
        VALUES('{week_days}', {max_subject_in_day})''')
        for i in range(len(list_classes)):
            self.cursor.execute(f'''INSERT INTO classes(class) VALUES('{list_classes[i]}')''')
        for i in range(len(list_teachers)):
            self.cursor.execute(f'''INSERT INTO teachers(teacher) VALUES('{list_teachers[i]}')''')
        for i in range(len(list_subjects)):
            self.cursor.execute(f'''INSERT INTO subjects(subject) VALUES('{list_subjects[i]}')''')
        self.conn.commit()

    def data_from_table(self, class_elem, teacher, subject, week_day, lesson_number):
        self.cursor.execute(f'''INSERT INTO table_information(idclass, idteacher, idsubject, lesson_number, week_day)
            VALUES({class_elem}, {teacher}, {subject}, {lesson_number}, '{week_day}')''')
        self.conn.commit()

    def get_id_class(self, class_elem):
        return self.cursor.execute(f'''SELECT id FROM classes WHERE class = "{class_elem}"''').fetchall()[0][0]

    def get_id_teacher(self, teacher):
        return self.cursor.execute(f'''SELECT id FROM teachers WHERE teacher = "{teacher}"''').fetchall()[0][0]

    def get_id_subject(self, subject):
        return self.cursor.execute(f'''SELECT id FROM subjects WHERE subject = "{subject}"''').fetchall()[0][0]