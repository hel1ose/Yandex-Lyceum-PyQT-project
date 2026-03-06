from PyQt5.Qt import QMessageBox


class FlagNotPressedError(Exception):
    pass


class EmptyTeacherListError(Exception):
    pass


class QuantitySubjectError(Exception):
    pass


class EmptySubjectListError(Exception):
    pass


class UnsuitableDataBaseError(Exception):
    pass


class EmptyClassesListError(Exception):
    pass


def error_message(error):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowTitle("Ошибка")
    print(error)
    message_box.setText(str(error))
    message_box.exec_()