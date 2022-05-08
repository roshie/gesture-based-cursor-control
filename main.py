import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QDesktopWidget, QPushButton, QGridLayout, QSlider
from PyQt5.QtCore import pyqtSlot, Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QFont
from VideoStreamThread import Thread

class IntroWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Mouse Control'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 700
        self.cursorSensitivity = 10
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.width, self.height)
        # create a label
        self.label1 = QLabel(self)
        self.label1.setText("Mouse With Facial Gestures")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont('Calibri', 14))

        self.label2 = QLabel(self)
        self.label2.setText("Set Cursor Sensitivity")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont('Calibri', 10))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.setCursorSensitivity)
        self.slider.setMinimum(5)
        self.slider.setMaximum(15)
        self.slider.setValue(self.cursorSensitivity)

        self.minLabel = QLabel(self)
        self.minLabel.setText("1")
        self.minLabel.setAlignment(Qt.AlignRight)

        self.maxLabel = QLabel(self)
        self.maxLabel.setText("10")

        self.button = QPushButton("Start Camera", self)
        self.button.clicked.connect(self.on_pushButton_clicked)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label1, 0, 0)
        self.layout.addWidget(self.label2, 1, 0)
        self.layout.addWidget(self.minLabel, 2, 0)
        self.layout.addWidget(self.slider, 2, 1)
        self.layout.addWidget(self.maxLabel, 2, 2)
        self.layout.addWidget(self.button, 3, 0)

        self.setLayout(self.layout)

        self.location_on_the_screen()
        self.show()
 
    def on_pushButton_clicked(self):
        self.close()
        self.camwindow = CamWindow(self.cursorSensitivity)
        self.camwindow.show()

    def setCursorSensitivity(self, value):
        self.cursorSensitivity = value

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)
class CamWindow(QWidget):
    def __init__(self, CursorSensitivity):
        super().__init__()
        self.title = 'Mouse Control'
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 700
        self.CursorSensitivity = CursorSensitivity
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUI()
    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.width, self.height)
        # create a label
        self.label = QLabel(self)
        self.label.move(800, 0)
        self.label.resize(800, 800)
        self.label.setMargin(0)
        th = Thread(self, self.CursorSensitivity)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.location_on_the_screen()
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    intro = IntroWindow()
    sys.exit(app.exec_())