import os
from PIL import Image, ImageQt
import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMainWindow, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        main_label = QLabel("<font size=20>↓</font><br/>Drag and Drop<br/>Image here!")
        main_label.setStyleSheet("color: gray;"
                             "font: bold;"
                             "qproperty-alignment: AlignCenter;"
                             "border-style: solid;"
                             "border-radius: 10px;"
                             "border-width: 2px;"
                             "border-color: gray;"
                             "border-radius: 30px")

        vbox = QVBoxLayout()
        vbox.addWidget(main_label)
        self.setLayout(vbox)
        self.setWindowTitle('White to Transparent')
        self.setGeometry(300, 300, 300, 200)
        self.show()


    ## reference : https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)


    def get_transparent_image(self):
        img = Image.open('test_signature.png')
        img = img.convert('RGBA')
        datas = img.getdata()
        threshold = 230
        newData = []
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        return ImageQt(img)


if __name__ == "__main__":
    app = QApplication([__file__])
    ex = ImageViewer()
    sys.exit(app.exec_())