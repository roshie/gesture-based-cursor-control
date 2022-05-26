
from PyQt5.QtCore import pyqtSlot, Qt, QRect
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QDesktopWidget, QPushButton, QGridLayout

class KeyboardBtn(QPushButton):
    def __init__(self, char, window):
        super().__init__(char, window) 
        self.mc = window.mousecontrols
        self.setStyleSheet("font-size: 30px; padding: 10px;")
        self.val = char
        self.clicked.connect(self.keyPressed)

    def keyPressed(self):
        self.mc.enterCharacter(self.val)

class KeyboardWindow(QWidget):
    def __init__(self, mouseControls):
        super().__init__()
        self.title = 'Keyboard'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 500
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.mousecontrols = mouseControls
        self.initUI()

    def mousePressEvent(self, e):
        print("mousePressEvent", e.globalPos())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.width, self.height)

        btn1 = KeyboardBtn("1", self)
        btn2 = KeyboardBtn("2", self)
        btn3 = KeyboardBtn("3", self)
        btn4 = KeyboardBtn("4", self)
        btn5 = KeyboardBtn("5", self)
        btn6 = KeyboardBtn("6", self)
        btn7 = KeyboardBtn("7", self)
        btn8 = KeyboardBtn("8", self)
        btn9 = KeyboardBtn("9", self)
        btn0 = KeyboardBtn("0", self)

        btnQ = KeyboardBtn("Q", self)
        btnW = KeyboardBtn("W", self)
        btnE = KeyboardBtn("E", self)
        btnR = KeyboardBtn("R", self)
        btnT = KeyboardBtn("T", self)
        btnY = KeyboardBtn("Y", self)
        btnU = KeyboardBtn("U", self)
        btnI = KeyboardBtn("I", self)
        btnO = KeyboardBtn("O", self)
        btnP = KeyboardBtn("P", self)

        btnA = KeyboardBtn("A", self)
        btnS = KeyboardBtn("S", self)
        btnD = KeyboardBtn("D", self)
        btnF = KeyboardBtn("F", self)
        btnG = KeyboardBtn("G", self)
        btnH = KeyboardBtn("H", self)
        btnJ = KeyboardBtn("J", self)
        btnK = KeyboardBtn("K", self)
        btnL = KeyboardBtn("L", self)
        btnColon = KeyboardBtn(";", self)

        btnZ = KeyboardBtn("Z", self)
        btnX = KeyboardBtn("X", self)
        btnC = KeyboardBtn("C", self)
        btnV = KeyboardBtn("V", self)
        btnB = KeyboardBtn("B", self)
        btnN = KeyboardBtn("N", self)
        btnM = KeyboardBtn("M", self)
        btnComma = KeyboardBtn(",", self)
        btnPrd = KeyboardBtn(".", self)
        btnques= KeyboardBtn("?", self)

        # btnSpace = KeyboardBtn("Space", self)
        rand = KeyboardBtn("Space", self)
        btnEnter = KeyboardBtn("Enter", self)
        btnBackSpace = KeyboardBtn("Backspace", self)

        grid = QGridLayout()
        # row 1
        grid.addWidget(btn1, 0, 0)
        grid.addWidget(btn2, 0, 1)
        grid.addWidget(btn3, 0, 2)
        grid.addWidget(btn4, 0, 3)
        grid.addWidget(btn5, 0, 4)
        grid.addWidget(btn6, 0, 5)
        grid.addWidget(btn7, 0, 6)
        grid.addWidget(btn8, 0, 7)
        grid.addWidget(btn9, 0, 8)
        grid.addWidget(btn0, 0, 9)
        # row 2
        grid.addWidget(btnQ, 1, 0)
        grid.addWidget(btnW, 1, 1)
        grid.addWidget(btnE, 1, 2)
        grid.addWidget(btnR, 1, 3)
        grid.addWidget(btnT, 1, 4)
        grid.addWidget(btnY, 1, 5)
        grid.addWidget(btnU, 1, 6)
        grid.addWidget(btnI, 1, 7)
        grid.addWidget(btnO, 1, 8)
        grid.addWidget(btnP, 1, 9)

        # row 3
        grid.addWidget(btnA, 2, 0)
        grid.addWidget(btnS, 2, 1)
        grid.addWidget(btnD, 2, 2)
        grid.addWidget(btnF, 2, 3)
        grid.addWidget(btnG, 2, 4)
        grid.addWidget(btnH, 2, 5)
        grid.addWidget(btnJ, 2, 6)
        grid.addWidget(btnK, 2, 7)
        grid.addWidget(btnL, 2, 8)
        grid.addWidget(btnColon, 2, 9)
        
        # row 4
        grid.addWidget(btnZ, 3, 0)
        grid.addWidget(btnX, 3, 1)
        grid.addWidget(btnC, 3, 2)
        grid.addWidget(btnV, 3, 3)
        grid.addWidget(btnB, 3, 4)
        grid.addWidget(btnN, 3, 5)
        grid.addWidget(btnM, 3, 6)
        grid.addWidget(btnComma, 3, 7)
        grid.addWidget(btnPrd, 3, 8)
        grid.addWidget(btnques, 3, 9)

         # row 5
        grid.addWidget(btnBackSpace, 4, 0, 4, 2)
        grid.addWidget(btnEnter, 4, 2, 4, 3)
        grid.addWidget(rand, 4, 5, 4, 5)

        # self.setLayout(layout)
        self.setLayout(grid)

        self.location_on_the_screen()
        self.show()

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)