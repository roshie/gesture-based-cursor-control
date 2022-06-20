import cv2
import sys
import pyautogui as pyag
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from CursorController import CursorController
from Notifier import Notifier
import logging as log
log.basicConfig(format='[%(levelname)s] %(message)s', level=log.DEBUG)

class Thread(QThread, Notifier):
    changePixmap = pyqtSignal(QImage)
    loading = True

    def __init__(self, window, mouseControls) -> None:
        super().__init__(window)
        self.window = window
        self.mouseControls = mouseControls
        log.info("Starting Camera...")

    # notifier handlers
    def changInputMode(self, val):
        self.changeInputMode(val)

    def changScrollMode(self, val):
        self.changeScrollMode(val)

    def updatPercentage(self, val):
        self.updatePercentage(val)

    def run(self):
        try: 
            self.cap = cv2.VideoCapture(0)
            
            facial_mouse = CursorController(self.mouseControls)
            facial_mouse.attach(self)
            
            while True:
                if self.loading: 
                    self.loading = False
                    # self.window.movie.stop()
                    log.info("Camera Started")
                ret, frame = self.cap.read()
                frame = facial_mouse.setFrame(frame)

                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(self.window.width//2, self.window.height, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)

        except Exception as e:
            log.error("Line 56, %s",str(e))

    def terminate(self) -> None:
        log.info("Camera Off")
        cv2.destroyAllWindows()
        self.cap.release()
        return super().terminate()
                
    def __del__(self):
        # Destroy 
        cv2.destroyAllWindows()
        self.cap.release()