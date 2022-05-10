import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QDesktopWidget, QPushButton, QGridLayout, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QFont
from VideoStreamThread import Thread
from qt_material import apply_stylesheet

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
        self.label1.setText("Facial-Gesture based mouse")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-weight: bold; font-size: 40px;")

        self.label2 = QLabel(self)
        self.label2.setText("Set Cursor Sensitivity")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("font-size: 30px;")

        minLabel = QLabel(self)
        minLabel.setText("1")
        minLabel.setAlignment(Qt.AlignCenter)
        minLabel.setStyleSheet("font-size: 25px;")

        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(self.setCursorSensitivity)
        slider.setMinimum(5)
        slider.setMaximum(15)
        slider.setValue(10)

        maxLabel = QLabel(self)
        maxLabel.setText("10")
        maxLabel.setAlignment(Qt.AlignCenter)
        maxLabel.setStyleSheet("font-size: 25px;")

        self.button = QPushButton("Start Camera", self)
        self.button.clicked.connect(self.on_pushButton_clicked)
        self.button.setStyleSheet("font-size: 25px;")

        rowLayout = QHBoxLayout()
        # Add widgets to the layout
        rowLayout.addWidget(minLabel)
        rowLayout.addWidget(slider, 5)
        rowLayout.addWidget(maxLabel)

        rowLayoutWrapper = QLabel()
        rowLayoutWrapper.setLayout(rowLayout)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label1, 0, 0)
        self.layout.addWidget(self.label2, 1, 0)
        self.layout.addWidget(rowLayoutWrapper, 2, 0)
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
        self.inputMode = False
        self.scrollMode = False
        self.percentile = 0
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
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def onClose(self):
        self.close()
        self.videoStreamThread.terminate()
        self.intro = IntroWindow()
        self.intro.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.width, self.height)
        # create a label
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(800, 800)
        self.videoStreamThread = Thread(self, self.CursorSensitivity)
        self.videoStreamThread.changePixmap.connect(self.setImage)
        self.videoStreamThread.start()

        eyebrowLiftPercent = QLabel(f"{'' if not self.percentile else str(self.percentile) + '%'}")
        eyebrowLiftPercent.setStyleSheet("font-size: 30px;")

        # input mode
        inputModeLabel = QLabel("INPUT MODE: ")
        inputModeLabel.setStyleSheet("font-size: 30px;")

        inputStatus = QLabel(f"{'ON' if self.inputMode else 'OFF'}")
        inputStatus.setStyleSheet(f"color: {'green' if self.inputMode else 'red'}; font-size: 40px;")

        inputModeRow = QHBoxLayout()
        inputModeRow.addWidget(inputModeLabel)
        inputModeRow.addWidget(inputStatus)
        inputModeRowWrapper = QLabel()
        inputModeRowWrapper.setLayout(inputModeRow)

        inputModeHelperText = QLabel(" (Lift your eyebrows for 3 seconds to turn on)")
        inputModeHelperText.setAlignment(Qt.AlignTop)
        inputModeHelperText.setStyleSheet("font-size: 25px;")

        # Scroll Mode
        scrollModeLabel = QLabel("SCROLL MODE: ")
        scrollModeLabel.setStyleSheet("font-size: 30px;")

        scrollStatus = QLabel(f"{'ON' if self.scrollMode else 'OFF'}")
        scrollStatus.setStyleSheet(f"color: {'green' if self.scrollMode else 'red'}; font-size: 40px;")

        scrollModeRow = QHBoxLayout()
        scrollModeRow.addWidget(scrollModeLabel)
        scrollModeRow.addWidget(scrollStatus)
        scrollModeRowWrapper = QLabel()
        scrollModeRowWrapper.setLayout(scrollModeRow)

        # Buttons row
        helpbtn = QPushButton("Help?", self)
        helpbtn.setStyleSheet("font-size: 25px;")
        closeBtn = QPushButton("Close", self)
        closeBtn.setStyleSheet("font-size: 25px;")
        closeBtn.clicked.connect(self.onClose)

        buttonsRow = QHBoxLayout()

        keyboardbtn = QPushButton("Show Keyboard", self)
        keyboardbtn.setStyleSheet("font-size: 25px;")
        buttonsRow.addWidget(keyboardbtn)

        buttonsRow.addWidget(helpbtn)
        buttonsRow.addWidget(closeBtn)
        buttonsRowWrapper = QLabel()
        buttonsRowWrapper.setLayout(buttonsRow)
        
        leftCell = QVBoxLayout()
        leftCell.addWidget(eyebrowLiftPercent)
        leftCell.addWidget(inputModeRowWrapper)
        leftCell.addWidget(inputModeHelperText)
        leftCell.addWidget(scrollModeRowWrapper)
        leftCell.addWidget(buttonsRowWrapper)
        leftCellWrapper = QLabel()
        leftCellWrapper.setLayout(leftCell)

        layout = QHBoxLayout()
        layout.addWidget(leftCellWrapper)
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

        self.location_on_the_screen()
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    intro = IntroWindow()
    # Debug
    # camwindow = CamWindow(10)
    apply_stylesheet(app, theme='dark_teal.xml', extra={'density_scale': '5'})
    sys.exit(app.exec_())