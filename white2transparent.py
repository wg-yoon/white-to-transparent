import os
from PIL import Image, ImageQt
import tkinter as tk
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QSlider, QStackedLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from copy import deepcopy
class ImageViewer(QMainWindow):
    front_idx = None
    slider_flag = True
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


    def add_output_widget(self):
        global output_label, img, datas, slider
        self.output_wid = QWidget()
        output_label = QLabel(self)

        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        slider.setSingleStep(2)
        slider.setValue(70)
        value = slider.value()

        btn = QPushButton('Save!', self)
        btn.clicked.connect(self.Save_clicked)

        img = Image.open(file_path)
        img = img.convert('RGBA')
        datas = img.getdata()

        pixmap = QPixmap.fromImage(self.get_transparent_image(value))
        scaled_pixmap=pixmap.scaled(int(self.width*0.7), int(self.height*0.7), Qt.KeepAspectRatio)
        output_label.setPixmap(scaled_pixmap)
        output_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        slider.sliderMoved.connect(self.sliderMoved)

        output_vbox = QVBoxLayout()
        output_vbox.addWidget(output_label)
        output_vbox.addWidget(btn)
        output_vbox.addWidget(slider)

        self.layout_for_wids.addWidget(self.output_wid)
        self.output_wid.setLayout(output_vbox)
        self.output_wid.resize(self.width, self.height)

    def Save_clicked(self):
        fname = QFileDialog.getSaveFileName(self)[0]
        print(fname)
        threshold = 255/100*(slider.value())
        newData = []
        cur_img = deepcopy(img)
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)        
        cur_img.putdata(newData)
        if not fname.endswith("png") or fname.endswith("PNG"):
            fname+='.png'
        cur_img.save(os.path.join(fname), "PNG")

    def sliderMoved(self, val):
        if val > 0:
            pixmap = QPixmap.fromImage(self.get_transparent_image(val))
            scaled_pixmap=pixmap.scaled(int(self.width*0.7), int(self.height*0.7), Qt.KeepAspectRatio)
            output_label.setPixmap(scaled_pixmap)

    # reference : https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        global file_path
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
        file_path = f
        self.add_output_widget()
        self.output_wid.show()
        self.input_wid.hide()
    

    def get_transparent_image(self, scale):
        threshold = 255/100*scale
        newData = []
        cur_img = deepcopy(img)
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)        
        cur_img.putdata(newData)
        qim = ImageQt.ImageQt(cur_img)

        return qim


if __name__ == "__main__":
    app = QApplication([__file__])
    main = ImageViewer()
    main.show()
    sys.exit(app.exec_())