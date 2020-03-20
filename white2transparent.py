import os
from PIL import Image, ImageQt
import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QSlider, QStackedLayout
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QImage, QPixmap

class ImageViewer(QMainWindow):
    front_idx = None
    height = 400
    width =400
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.layout_for_wids = QStackedLayout()
        self.central_wid = QWidget()

        ## INPUT WIDGET
        self.input_wid = QWidget()
        
        input_label = QLabel("<font size=20>↓</font><br/>Drag and Drop<br/>Image here!")
        input_label.setStyleSheet("color: gray;"
                                "font: bold;"
                                "qproperty-alignment: AlignCenter;"
                                "border-style: solid;"
                                "border-radius: 10px;"
                                "border-width: 2px;"
                                "border-color: gray;"
                                "border-radius: 30px")

        input_vbox = QVBoxLayout()
        input_vbox.addWidget(input_label)
        self.layout_for_wids.addWidget(self.input_wid)
        self.input_wid.setLayout(input_vbox)

        self.central_wid.setLayout(self.layout_for_wids)
        self.setCentralWidget(self.central_wid)

        self.setWindowTitle('White to Transparent')
        self.setGeometry(300, 300, self.width, self.height)
        self.front_wid = 1

    def add_output_widget(self, file_path):
        self.output_wid = QWidget()

        image = QPixmap.fromImage(self.get_transparent_image(file_path, 90))
        self.output_wid.setPixmap = image
        output_label = QLabel(self)
        pixmap = image
        output_label.setPixmap(pixmap)

        output_vbox = QVBoxLayout()
        output_vbox.addWidget(output_label)
        self.layout_for_wids.addWidget(self.output_wid)
        self.output_wid.setLayout(output_vbox)

    
    # reference : https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)

        self.add_output_widget(f)
        self.output_wid.show()
        self.input_wid.hide()
    

    def get_transparent_image(self, image_path, scale):
        img = Image.open(image_path)
        img = img.convert('RGBA')
        datas = img.getdata()
        threshold = 255/100*scale
        print(scale)
        print(threshold)
        newData = []
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)        
        img.putdata(newData)
        qim = ImageQt.ImageQt(img)

        return qim


if __name__ == "__main__":
    app = QApplication([__file__])
    main = ImageViewer()
    main.show()
    sys.exit(app.exec_())