from main_window import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
import backend
from dialog import Ui_Dialog

class MainWindowUi(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

    def fetch_info(self):
        today = self.dateEditToday.text()
        birthday = self.dateEditBirthday.text()
        n = self.lineEditN.text()
        return today, birthday, int(n)

    def display_result(self, nextbirthday, today_to_nextbirthday, planday, today_to_planday):
        text = f"Next birthday: {nextbirthday}\nDays from today to next birthday:{today_to_nextbirthday}\n" \
               f"Original day to make birthday plan:{planday}\nCorrected day to make birthday plan:{today_to_planday}"
        self.textBrowser.setText(text)

class DialogUi(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)

    def on_click_no(self):
        self.close()

class BussLogic:
    def __init__(self):
        self.main_window = MainWindowUi()
        self.dialog = DialogUi()
        self.main_window.pushButton.clicked.connect(self.on_click_generate)
        self.dialog.pushButtonYes.clicked.connect(self.on_click_yes)
        self.dialog.pushButtonNo.clicked.connect(self.dialog.on_click_no)


    def on_click_generate(self):
        today, birthday, n = self.main_window.fetch_info()
        days, next_birthday = backend.days_from_today_to_next_birthday(today, birthday)
        planday, isSaturday = backend.compute_planday(next_birthday, n)
        self.main_window.display_result(next_birthday, days, planday, planday)
        if not isSaturday:
            self.dialog.show()

    def on_click_yes(self):
        today, birthday, n = self.main_window.fetch_info()
        days, next_birthday = backend.days_from_today_to_next_birthday(today, birthday)
        planday, isSaturday = backend.compute_planday(next_birthday, n)
        corrected_planday = backend.correct_planday(planday)
        self.main_window.display_result(next_birthday, days, planday, corrected_planday)
        self.dialog.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    # buss.main_window.exec()
    buss.main_window.show()
    sys.exit(app.exec_())
