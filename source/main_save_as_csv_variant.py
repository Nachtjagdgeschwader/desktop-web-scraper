#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, csv
# import re
# a requirement for text cleaning (see below)
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QLabel, QLineEdit, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QVariant
from styles import styles
from data import vksearch, create_dataframe
from datetime import datetime

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(styles)
        self.sendButton = QPushButton('Search', self)
        self.sendButton.setObjectName('sendButton')
        self.sendButton.setShortcut('Return')
        self.questionEdit = QLineEdit(self)
        self.answer=QLabel(self)
        self.answer.setWordWrap(True)
        self.answer.setAlignment(Qt.AlignTop)
        self.tableView = QTableWidget(self)
        self.buttonSave = QPushButton('Save', self)
        grid = QGridLayout(self)
        grid.setSpacing(10)
        grid.addWidget(self.questionEdit, 1, 0)
        grid.addWidget(self.sendButton, 1, 1)
        grid.addWidget(self.answer, 2,0)
        grid.addWidget(self.tableView, 3,0)
        grid.addWidget(self.buttonSave, 2, 1)
        self.tableView.hide()
        self.buttonSave.hide()
        self.sendButton.clicked.connect(self.getResult)
        self.buttonSave.clicked.connect(self.handleSave)
        self.setLayout(grid)
        self.resize(500, 100)
        self.setMinimumSize(self.sizeHint())
        self.center()
        self.setWindowTitle('VK Searcher')
        self.setWindowIcon(QIcon('img/in-ico.ico'))
        self.show()

    def getResult(self):
        text = self.questionEdit.text()
        if len(text)>=1:
            res=vksearch(text)
            res_quant=len(res)
            text = 'Found <b style="color: green;">%d</b> from a maximum of 1000 messages:' % res_quant
            self.answer.setText(text)
            self.tableView.show()
            self.tableView.setRowCount(len(res))
            self.tableView.setSortingEnabled(True)
            self.tableView.setColumnCount(6)
            self.tableView.setHorizontalHeaderLabels(["URL", "Text", "Date and time",
                                                      'Comments', 'Likes', 'Shares'])
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
            self.setMinimumSize(self.sizeHint())
            self.buttonSave.show()

        else:
            self.answer.setText("Please specify the search query")

    def handleSave(self):
        path = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'CSV (*.csv)')
        f = csv.writer(open(str(path[0]), "w+", newline='\n', encoding='utf-8'),
                       delimiter=';', quotechar='"', dialect='excel')
        f.writerow(["Date and time", "Text", "Comments", 'Likes',
                    'Shares', 'URL'])

        for item in vksearch(self.questionEdit.text()):
            date = datetime.fromtimestamp(item['date'])
            # i = re.sub(" ?(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", " ", item['text'])
            # delete all links from text variable
            # i = re.sub("<[^<]+?>", " ", i)
            # delete all tags from text variable
            # text = re.sub("[^\w .,!?;]", " ", i)
            # delete all except alphanumeric, space and punctuation marks (.,!?;)
            text=item['text']
            comments = item['comments']['count']
            likes = item['likes']['count']
            reposts = item['reposts']['count']
            if item['post_type']=="post":
                url='https://vk.com/wall'+str(item['owner_id'])+'_'+str(item['id'])
            elif item['post_type']=="reply":
                url = 'https://vk.com/wall' + str(item['owner_id']) + '_' \
                      + str(item['post_id'])+'?reply='+str(item['id'])
            else:
                url='other URL'
            f.write_row([date,text,comments,likes,reposts,url])


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my = MyApp()
    sys.exit(app.exec_())