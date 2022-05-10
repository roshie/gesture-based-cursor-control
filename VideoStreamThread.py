import cv2
import sys
import pyautogui as pyag
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from FacialMouse import FacialMouse
from Notifier import Notifier

class Thread(QThread, Notifier):
    changePixmap = pyqtSignal(QImage)
    mouseSensitivity = 5

    def __init__(self, window, mouseSensitivity) -> None:
        super().__init__(window)
        self.mouseSensitivity = mouseSensitivity

    def changInputMode(self, val):
        self.changeInputMode(val)

    def changScrollMode(self, val):
        self.changeScrollMode(val)

    def updatPercentage(self, val):
        self.updatePercentage(val)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        
        facial_mouse = FacialMouse(self.mouseSensitivity)
        facial_mouse.attach(self)
        
        while True:
            ret, frame = self.cap.read()
            frame = facial_mouse.setFrame(frame)

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(750, 750, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                
    def __del__(self):
        # Destroy 
        cv2.destroyAllWindows()
        self.cap.release()