from main_window import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
import backend
from dialog import Ui_Dialog

class MainWindowUi(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonStart.clicked.connect(self.turn_page_start)
        self.pushButtonGenerate_2.clicked.connect(self.turn_page_start)

    def turn_page_start(self):
        self.stackedWidget.setCurrentIndex(1)

    def turn_page_continue(self):
        self.stackedWidget.setCurrentIndex(2)

    def fetch_info_1(self):
        name = self.lineEditName.text()
        relation = self.lineEditRelation.text()
        birthday = self.dateEditBirthday_2.text()
        return name, relation, birthday

    def clear_info(self):
        self.lineEditName.clear()
        self.lineEditRelation.clear()

    def fetch_info_2(self):
        name = self.comboBoxPeople.currentText()
        today = self.dateEditToday_2.text()
        n = self.lineEditN_2.text()
        return name, today, int(n)

    def display_result(self, name, nextbirthday, today_to_nextbirthday, planday, today_to_planday):
        text = f"Name: {name}\nNext birthday: {nextbirthday}\nDays from today to next birthday:{today_to_nextbirthday}\n" \
               f"Original day to make birthday plan:{planday}\nCorrected day to make birthday plan:{today_to_planday}"
        self.textBrowser_2.setText(text)

    def display_table(self, dic):
        i = 0
        self.tableWidget.setRowCount(len(dic))
        for k, v in dic.items():
            name = k
            relation = v[0]
            birthday = v[1]
            item0 = QtWidgets.QTableWidgetItem(name)
            item1 = QtWidgets.QTableWidgetItem(relation)
            item2 = QtWidgets.QTableWidgetItem(birthday)
            self.tableWidget.setItem(i, 0, item0)
            self.tableWidget.setItem(i, 1, item1)
            self.tableWidget.setItem(i, 2, item2)
            i += 1



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
        self.d = {}
        self.n = []
        self.main_window.stackedWidget.setCurrentIndex(0)
        self.main_window.pushButtonGenerate.clicked.connect(self.on_click_generate)
        self.dialog.pushButtonYes.clicked.connect(self.on_click_yes)
        self.dialog.pushButtonNo.clicked.connect(self.dialog.on_click_no)
        self.main_window.pushButtonAdd.clicked.connect(self.on_click_add)
        self.main_window.pushButtonContinue.clicked.connect(self.on_click_continue)


    def on_click_generate(self):
        name, today, n = self.main_window.fetch_info_2()
        days, next_birthday = backend.days_from_today_to_next_birthday(today, self.d[name][1])
        planday, isSaturday = backend.compute_planday(next_birthday, n)
        self.main_window.display_result(name, next_birthday, days, planday, planday)
        if not isSaturday:
            self.dialog.show()

    def on_click_yes(self):
        name, today, n = self.main_window.fetch_info_2()
        days, next_birthday = backend.days_from_today_to_next_birthday(today, self.d[name][1])
        planday, isSaturday = backend.compute_planday(next_birthday, n)
        corrected_planday = backend.correct_planday(planday)
        self.main_window.display_result(name, next_birthday, days, planday, corrected_planday)
        self.dialog.close()

    def on_click_add(self):
        name, relation, birthday = self.main_window.fetch_info_1()
        self.d[name] = [relation, birthday]
        self.n.append(name)
        self.main_window.clear_info()
        self.main_window.display_table(self.d)

    def on_click_continue(self):
        self.main_window.comboBoxPeople.clear()
        self.main_window.comboBoxPeople.addItems(self.n)
        self.main_window.stackedWidget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    # buss.main_window.exec()
    buss.main_window.show()
    sys.exit(app.exec_())
