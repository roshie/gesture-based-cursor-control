import cv2
import sys
import pyautogui as pyag
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from CursorController import CursorController
from Notifier import Notifier

class Thread(QThread, Notifier):
    changePixmap = pyqtSignal(QImage)
    mouseSensitivity = 5
    loading = True

    def __init__(self, window, mouseControls) -> None:
        super().__init__(window)
        self.mouseControls = mouseControls
    def changInputMode(self, val):
        self.changeInputMode(val)

    def changScrollMode(self, val):
        self.changeScrollMode(val)

    def updatPercentage(self, val):
        self.updatePercentage(val)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        
        facial_mouse = CursorController(self.mouseControls)
        facial_mouse.attach(self)
        
        while True:
            if self.loading: self.loading = False
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