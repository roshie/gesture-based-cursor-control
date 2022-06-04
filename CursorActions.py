from turtle import pos
import pyautogui as pyag
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import logging as log
log.basicConfig(format='[%(levelname)s] %(message)s', level=log.DEBUG)

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
        self.drag = 15 + drag # values - 0 to 10
        self.scrollOffset = scrollOffset
        mixer.init()
        self.clickQueue = []

    def enterCharacter(self, char):
        if not len(self.clickQueue):
            log.debug("No Textfield is focussed")
            return

        x,y = self.clickQueue[-1]
        
        commands = {
            'Space': ' ',
            'Enter': 'enter',
            'Backspace': 'backspace',
        }
        currentMousePosX, currentMousePosY = pyag.position()
        pyag.click(x=x, y=y)
        if char in commands.keys():
            if char == "Space":
                pyag.hotkey('space')
            else:
                pyag.press(commands[char])
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
            log.debug(f"invalid input: {char}")
            pyag.moveTo(currentMousePosX, currentMousePosY)
            return
        self.playSound()
        log.debug("Character %s entered at Position %s, %s", char, x, y)
        pyag.moveTo(currentMousePosX, currentMousePosY)
        
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
        pyag.click(button=button)
        self.recordClick(pyag.position())
        self.playSound()

    def recordClick(self, position, dimension=None):
        x, y = position

        if not dimension: 
            dimension = self.screenWidth()-(self.screenWidth() * CAM_WINDOW_WIDTH), self.screenWidth() - (self.screenHeight() * CAM_WINDOW_HEIGHT)

            log.debug("Window Dimension (%s, %s)", dimension[0], dimension[1])
            
            if x < dimension[0] and y < dimension[1]:

                self.clickQueue.append((x,y))
                if len(self.clickQueue) > 5:
                    self.clickQueue.pop(0)
        
            log.debug("Front element in Click queue is (%s, %s)", self.clickQueue[-1][0], self.clickQueue[-1][1])
    
    def playSound(self):
        mixer.music.load(clickSound)
        mixer.music.play()

    def screenWidth(self) -> int:
        return pyag.size().width

    def screenHeight(self) -> int:
        return pyag.size().height
