#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, time
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QDialog,
                             QLabel, QLineEdit, QGridLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QCalendarWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QVariant, QDate, QDateTime
from styles import styles
from data import vksearch, create_dataframe
from datetime import datetime
import xlsxwriter

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(styles)
        self.sendButton = QPushButton('Шукати', self)
        self.sendButton.setObjectName('sendButton')
        self.sendButton.setShortcut('Return')
        self.questionEdit = QLineEdit(self)
        self.answer=QLabel(self)
        self.enddate = QLabel(self)
        self.startdate = QLabel(self)
        self.answer = QLabel(self)
        self.answer2 = QLabel(self)
        self.answer.setWordWrap(True)
        self.answer.setAlignment(Qt.AlignTop)
        self.answer2.setAlignment(Qt.AlignTop|Qt.AlignRight)
        self.tableView = QTableWidget(self)
        self.buttonSave = QPushButton('Зберегти', self)
        self.buttonDate = QPushButton('Час', self)
        self.buttonDate.setToolTip('Задати часовий проміжок пошуку')
        grid = QGridLayout(self)
        grid.setSpacing(10)
        grid.addWidget(self.questionEdit, 1, 0)
        grid.addWidget(self.sendButton, 1, 1)
        grid.addWidget(self.answer, 2,0)
        grid.addWidget(self.enddate, 3, 0)
        grid.addWidget(self.startdate, 3, 0)
        grid.addWidget(self.answer2, 2, 1)
        self.enddate.setText(str(int(time.time())))
        self.startdate.setText(str(1160438400))
        grid.addWidget(self.tableView, 4,0)
        grid.addWidget(self.buttonSave, 2, 1)
        grid.addWidget(self.buttonDate, 1, 2)
        self.tableView.hide()
        self.buttonSave.hide()
        self.enddate.hide()
        self.startdate.hide()
        self.answer2.hide()
        self.sendButton.clicked.connect(self.getResult)
        self.buttonSave.clicked.connect(self.handleSave)
        self.buttonDate.clicked.connect(self.dateDialog)
        self.setLayout(grid)
        self.resize(500, 100)
        self.setMinimumSize(self.sizeHint())
        self.center()
        self.setWindowTitle('VK Searcher alpha 0.0.1')
        self.setWindowIcon(QIcon('img/in-ico.ico'))
        self.show()

    def dateDialog(self):
        d = QDialog(None, Qt.WindowCloseButtonHint)
        d.setStyleSheet(styles)
        grid2 = QGridLayout()
        grid2.setSpacing(5)
        b1 = QPushButton("Задати", d)
        cal1 = QCalendarWidget()
        cal2 = QCalendarWidget()
        startlabel = QLabel(self)
        startlabel.setText("Почати пошук з:")
        endlabel = QLabel(self)
        endlabel.setText("Закінчити пошук на:")
        cal1.clicked[QDate].connect(self.startDate)
        cal2.clicked[QDate].connect(self.endDate)
        grid2.addWidget(b1, 1, 1)
        grid2.addWidget(startlabel, 2, 0)
        grid2.addWidget(cal1, 3, 0)
        grid2.addWidget(endlabel, 2, 1)
        grid2.addWidget(cal2, 3, 1)
        d.setLayout(grid2)
        self.setMinimumSize(self.sizeHint())
        d.setWindowTitle("Вибір часового проміжку")
        date = cal1.selectedDate()
        date1 = cal2.selectedDate()
        self.enddate.setText(str(int(QDateTime(date).toMSecsSinceEpoch()/1000)))
        self.startdate.setText(str(int(QDateTime(date1).toMSecsSinceEpoch() / 1000)))
        b1.clicked.connect(d.close)
        d.exec_()

    def endDate(self, date):
        text = 'Обрано кінцеву дату: %s' % date.toString("dd.MM.yyyy")
        self.answer.setText(text)
        self.enddate.setText(str(int(QDateTime(date).toMSecsSinceEpoch() / 1000)))
    def startDate(self, date1):
        text = 'Обрано початкову дату: %s' % date1.toString("dd.MM.yyyy")
        self.answer2.setText(text)
        self.answer2.show()
        self.startdate.setText(str(int(QDateTime(date1).toMSecsSinceEpoch() / 1000)))

    def getResult(self):
        text = self.questionEdit.text()
        enddate=int(self.enddate.text())
        startdate = int(self.startdate.text())

        if len(text)>=1:
            res=vksearch(text,enddate,startdate)
            res_quant=len(res)
            text = 'Знайдено <b style="color: green;">%d</b> повідомлень із 1000 можливих:' % res_quant
            self.answer.setText(text)
            self.answer2.hide()
            self.tableView.show()
            self.tableView.setRowCount(len(res))
            self.tableView.setSortingEnabled(True)
            self.tableView.setColumnCount(7)
            self.tableView.setColumnWidth(0, 300)
            self.tableView.setColumnWidth(1, 450)
            self.tableView.setColumnWidth(2, 260)
            self.tableView.setColumnWidth(3, 150)
            self.tableView.setColumnWidth(4, 180)
            self.tableView.setColumnWidth(5, 170)
            self.tableView.setHorizontalHeaderLabels(["Посилання", "Текст", "Дата і час",
                                                      'Коментарі', 'Подобається',
                                                      'Поширення','Σ'])

            for i in range(0, len(res)):
                self.tableView.setItem(i, 0, QTableWidgetItem(create_dataframe(res)[0][i]))
                self.tableView.setItem(i, 1, QTableWidgetItem(create_dataframe(res)[1][i]))
                self.tableView.setItem(i, 2, QTableWidgetItem(str(create_dataframe(res)[2][i])))
                it3 = QTableWidgetItem()
                it3.setData(Qt.EditRole, QVariant(create_dataframe(res)[3][i]))
                self.tableView.setItem(i, 3, it3)
                it4 = QTableWidgetItem()
                it4.setData(Qt.EditRole, QVariant(create_dataframe(res)[4][i]))
                self.tableView.setItem(i, 4, it4)
                it5 = QTableWidgetItem()
                it5.setData(Qt.EditRole, QVariant(create_dataframe(res)[5][i]))
                self.tableView.setItem(i, 5, it5)
                it6 = QTableWidgetItem()
                it6.setData(Qt.EditRole, QVariant(create_dataframe(res)[3][i]
                                                  +create_dataframe(res)[4][i]
                                                  +create_dataframe(res)[5][i]))
                self.tableView.setItem(i, 6, it6)
            self.setMinimumSize(self.sizeHint())
            self.buttonSave.show()

        else:
            self.answer.setText("Введіть запит для пошуку")

    def handleSave(self):
        filename=QFileDialog.getSaveFileName(self, 'Зберегти',
                                             self.questionEdit.text(),
                                             'Excel files(*.xlsx)')
        if not filename[0]:
            return None
        else:
            workbook = xlsxwriter.Workbook(str(filename[0]))
            f = workbook.add_worksheet()
            f.write_row(0, 0,["Дата і час", "Текст", "Коментарі", 'Подобається',
                        'Поширення', 'Посилання'])
            date3 = []
            text1 = []
            comments1 = []
            likes1 = []
            reposts1 = []
            url2 = []
            enddate = int(self.enddate.text())
            startdate = int(self.startdate.text())
            for item in vksearch(self.questionEdit.text(),enddate,startdate):
                date3.append(datetime.fromtimestamp(item['date']))
                text1.append(item['text'])
                comments1.append(item['comments']['count'])
                likes1.append(item['likes']['count'])
                reposts1.append(item['reposts']['count'])
                if item['post_type']=="post":
                    url='https://vk.com/wall'+str(item['owner_id'])+'_'+str(item['id'])
                elif item['post_type']=="reply":
                    url = 'https://vk.com/wall' + str(item['owner_id']) + '_' \
                          + str(item['post_id'])+'?reply='+str(item['id'])
                else:
                    url='other URL'
                url2.append(url)
            format_date = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})
            format_first = workbook.add_format({'bold': True, 'align': 'center',
                                                'font_size':16, 'bg_color':'silver'})
            f.set_row(0, None, format_first)
            f.write_column('A2', date3, format_date)
            f.write_column('B2', text1)
            f.write_column('C2', comments1)
            f.write_column('D2', likes1)
            f.write_column('E2', reposts1)
            f.write_column('F2', url2)
            f.set_column('A:F', 20)
            workbook.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my = MyApp()
    sys.exit(app.exec_())