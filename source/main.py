#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QLabel, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from styles import styles
from parsing_static import search
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(styles)
        self.sendButton = QPushButton('Ask', self)
        self.sendButton.setObjectName('sendButton')
        self.sendButton.setShortcut('Return')
        self.questionEdit = QLineEdit(self)
        self.answer=QLabel(self)
        self.answer.setWordWrap(True)
        self.answer.setAlignment(Qt.AlignTop)
        grid = QGridLayout(self)
        grid.setSpacing(10)
        grid.addWidget(self.questionEdit, 1, 0)
        grid.addWidget(self.sendButton, 1, 1)
        grid.addWidget(self.answer, 2,0)
        self.sendButton.clicked.connect(self.getAnswer)
        self.setLayout(grid)
        self.resize(500, 100)
        self.setMinimumSize(self.sizeHint())
        self.center()
        self.setWindowTitle('Answerer')
        self.setWindowIcon(QIcon('img/books-icon.png'))
        self.show()

    def getAnswer(self):
        text = self.questionEdit.text()
        if len(text)>=1:
            text = search(text)
            text=str(text)
            self.answer.setText(text)
        else:
            self.answer.setText("Specify your question")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my = MyApp()
    sys.exit(app.exec_())