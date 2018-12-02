import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
import forBD2

class work(QtWidgets.QMainWindow, forBD2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.setColumnCount(3)
        self.pushButton.clicked.connect(self.addition)
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.changeData)
        self.pushButton_4.clicked.connect(self.unhideVL1)
        self.pushButton_5.clicked.connect(self.unhideVL2)
        self.pushButton_6.clicked.connect(self.unhideVL3)
        self.pushButton_7.clicked.connect(self.hideAll)
        self.setWindowTitle("Работа с базой данных через SQL-запросы через графический интерфейс QtCreator'a")
        self.tableWidget.setHorizontalHeaderLabels(['name', 'dolj', 'number'])
        self.comboBox.addItem('name')
        self.comboBox.addItem('dolj')
        self.comboBox.addItem('number')
        self.hideAll()
        self.showDB()

    def hideAll(self):
        self.hideVL1()
        self.hideVL2()
        self.hideVL3()

    def showMenu(self):
        self.pushButton_4.show()
        self.pushButton_5.show()
        self.pushButton_6.show()
        self.pushButton_7.hide()

    def hideMenu(self):
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.hide()
        self.pushButton_7.show()

    def hideVL1(self):
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.pushButton.hide()
        self.showMenu()

    def unhideVL1(self):
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.pushButton.show()
        self.hideMenu()

    def hideVL2(self):
        self.comboBox.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.comboBox_3.hide()
        self.lineEdit_6.hide()
        self.pushButton_2.hide()
        self.showMenu()

    def unhideVL2(self):
        self.comboBox.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.comboBox_3.show()
        self.lineEdit_6.show()
        self.pushButton_2.show()
        self.hideMenu()

    def hideVL3(self):
        self.label_8.hide()
        self.comboBox_2.hide()
        self.pushButton_3.hide()
        self.showMenu()

    def unhideVL3(self):
        self.label_8.show()
        self.comboBox_2.show()
        self.pushButton_3.show()
        self.hideMenu()

    def showDB(self):
        for i in range(self.tableWidget.rowCount()): # очистка таблицы
            self.tableWidget.removeRow(0)
        db = sqlite3.connect('misDB')  # подключаем базу
        cursor = db.cursor()  # создаем курсор для обращения к базе через запросы
        cursor.execute("SELECT * FROM human")
        result=cursor.fetchall()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        for i in range(len(result)):
            x=result[i][1]
            y=result[i][2]
            z=result[i][3]
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 0, QTableWidgetItem(x))
            self.tableWidget.setItem(numRows, 1, QTableWidgetItem(y))
            self.tableWidget.setItem(numRows, 2, QTableWidgetItem(z))
            self.comboBox_2.addItem(x)
            self.comboBox_3.addItem(x)
        cursor.close()
        db.close()

    def changeData(self):
        db = sqlite3.connect('misDB')  # подключаем базу
        cursor = db.cursor()  # создаем курсор для обращения к базе через запросы
        name=self.comboBox_3.currentText()
        key=self.comboBox.currentText()
        cursor.execute("SELECT * FROM human WHERE name='" + name + "'")
        value=self.lineEdit_6.text()
        if value == "":
            error = QMessageBox()
            error.setWindowTitle("Ошибка!")
            error.setText('Вы не ввели новое значение!')
            error.show()
            error.exec_()
        else:
            cursor.execute("UPDATE human SET "+ key +"='" + value + "' WHERE name = '" + name + "'")
            self.lineEdit_6.clear()
        db.commit()
        self.showDB()
        cursor.close()
        db.close()

    def delete(self):
        db = sqlite3.connect('misDB')  # подключаем базу
        cursor = db.cursor()  # создаем курсор для обращения к базе через запросы
        name = self.comboBox_2.currentText()
        cursor.execute("DELETE FROM human WHERE name = '" + name + "'")
        db.commit()
        self.showDB()
        db.close()

    def addition(self):
        db = sqlite3.connect('misDB')  # подключаем базу
        cursor = db.cursor()  # создаем курсор для обращения к базе через запросы
        name=self.lineEdit.text()
        dolj=self.lineEdit_2.text()
        number=self.lineEdit_3.text()
        if name=='' or dolj=='' or number=='':
            error=QMessageBox()
            error.setWindowTitle("Ошибка!")
            error.setText('Для добавления в базу данных необходимо заполнить все поля!')
            error.show()
            error.exec_()
        else:
            cursor.execute("INSERT INTO human(name, dolj, number) VALUES ('" + name + "', '" + dolj + "', '" + number + "')")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
        db.commit()
        self.showDB()
        db.close()

def main():
    app=QtWidgets.QApplication(sys.argv)
    window = work()
    window.show()
    app.exec_()

main()