from turtle import pos
import pyautogui as pyag
from pygame import mixer

from GlobalVars import CAM_WINDOW_HEIGHT, CAM_WINDOW_WIDTH

# Import Click sound
clickSound = 'sounds/MouseClick.mp3'

class CursorActions():
    """
    @params 
    drag: Cursor Sensitivity {0 - 15} ;
    scrollOffset: Scroll value {Default: 40}
    """
    def __init__(self, drag, scrollOffset):
        self.drag = 35 + drag # values - 0 to 10
        self.scrollOffset = scrollOffset
        mixer.init()
        self.clickQueue = []

    def enterCharacter(self, char):
        x, y = 0, 0 if not len(self.clickQueue) else self.clickQueue[-1][-1]
        print(x,y)
        
        commands = {
            'Space': ' ',
            'Enter': 'enter',
            'Backspace': 'backspace',
        }
        pyag.click(x=x, y=y)
        if char in commands.keys():
            if char == "Space":
                pyag.hotkey('space')
            else:
                pyag.press(commands[char])
            print(f"Pressed Key: {char} - at coords x:{x} and y: {y}")
            return

        splChars = lambda char : char == "?" or char == "." or char == ";" or char == ","
        Num = lambda char : ord(char) >= 48 and ord(char) <= 57
        uppercase = lambda char: ord(char) >= 65 and ord(char) <= 90

        if splChars(char) or Num(char):
            pyag.press(char)
        elif uppercase(char):
            pyag.press(chr(ord(char)+32)) 
        # Debug
        else:
            print(f"invalid input: {char}")
            return
        self.playSound()
        print(f"Pressed Key: {char} - at coords x:{x} and y: {y}")
        
    def moveMouse(self, direction: str):
        if direction == 'right':
            pyag.moveRel(self.drag, 0)
        elif direction == 'left':
            pyag.moveRel(-self.drag, 0)
        elif direction == 'up':
            pyag.moveRel(0, -self.drag)
        elif direction == 'down':
            pyag.moveRel(0, self.drag)
                
    def scrollVertically(self, direction: str):
        if direction == 'right':
            pyag.moveRel(self.drag, 0)
        elif direction == 'left':
            pyag.moveRel(-self.drag, 0)
        elif direction == 'up':
            pyag.scroll(self.scrollOffset)
        elif direction == 'down':
            pyag.scroll(-self.scrollOffset)

    def click(self, button: str):
        self.recordClick(pyag.position())
        pyag.click(button=button)
        self.playSound()

    def recordClick(self, position):
        x, y = position
        print(f"position {x} {y} - window width {self.screenWidth()- self.screenWidth() * CAM_WINDOW_WIDTH} Height {self.screenWidth()- self.screenHeight() * CAM_WINDOW_HEIGHT}")
        if (x < self.screenWidth()-self.screenWidth() * CAM_WINDOW_WIDTH and y < self.screenWidth() - self.screenHeight() * CAM_WINDOW_HEIGHT):
            self.clickQueue.append((x,y))
            if len(self.clickQueue) > 5:
                self.clickQueue.pop(0)
        print(self.clickQueue)
    
    def playSound(self):
        mixer.music.load(clickSound)
        mixer.music.play()

    def screenWidth(self) -> int:
        return pyag.size().width

    def screenHeight(self) -> int:
        return pyag.size().height
