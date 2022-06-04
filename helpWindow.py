import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QDesktopWidget, QPushButton, QGridLayout, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QFont
from VideoStreamThread import Thread
from qt_material import apply_stylesheet

class HelpWindow(QWidget):
    def __init__(self, fontSize):
        super().__init__()
        self.fontSize = fontSize
        self.title = 'Help'
        self.left = 0
        self.top = 0
        pg = QDesktopWidget().availableGeometry()
        self.width = pg.width()//4
        self.height = pg.height()//4
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUI()

    def getFontSize(self, scale) -> str:
        return "font-size: {}px;".format(int(self.fontSize*scale))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.width, self.height)

        self.label1 = QLabel(self)
        self.label1.setText("""
        Input mode Activate / Deactivate:
        Lift your eyebrows for 3 seconds
        """)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet(self.getFontSize(1.2))

        self.label2 = QLabel(self)
        self.label2.setText("""
        Scroll Activate / Deactivate:
        Lift your eyebrows for 1 second
        """)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet(self.getFontSize(1.2))

        self.label3 = QLabel(self)
        self.label3.setText("Left click: Do a quick medium paced blink")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setStyleSheet(self.getFontSize(1.2))

        self.label4 = QLabel(self)
        self.label4.setText("Right click: Do a long blink")
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet(self.getFontSize(1.2))
        

        self.button = QPushButton("Close", self)
        # self.button.resize(50,50)
        self.button.clicked.connect(self.on_close_clicked)
        self.button.setStyleSheet(self.getFontSize(1.2))

        # rowLayout = QVBoxLayout
        # Add widgets to the layout
        

        # rowLayoutWrapper = QLabel()
        # rowLayoutWrapper.setLayout(rowLayout)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label1, 0, 0)
        self.layout.addWidget(self.label2, 1, 0)
        self.layout.addWidget(self.label3, 2, 0)
        self.layout.addWidget(self.label4, 3, 0)

        # self.layout.addWidget(rowLayoutWrapper, 2, 0)
        self.layout.addWidget(self.button, 4, 0)

        self.setLayout(self.layout)

        self.location_on_the_screen()
        self.show()

    def on_close_clicked(self):
        
        self.close()
        # self.camwindow = CamWindow(self.cursorSensitivity)
        # self.camwindow.show()        

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)    