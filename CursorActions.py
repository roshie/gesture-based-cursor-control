import pyautogui as pyag
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import logging as log
log.basicConfig(format='[%(levelname)s] %(message)s', level=log.DEBUG)

from GlobalVars import CLICK_SOUND, WINDOW_TITLES
from utils import get_resource_path

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
        # self.clickQueue = []
        self.windowQueue = []

    def enterCharacter(self, char):
        if not len(self.windowQueue) or not len(self.windowQueue[-1]) or (len(self.windowQueue) == 1 and self.windowQueue[-1] == "Search"):
            log.debug("No Window is focussed")
            return
        lastFocussedWindow = self.windowQueue[-1] if self.windowQueue[-1] != "Search" else self.windowQueue[-2]
        
        commands = {
            'Space': ' ',
            'Enter': 'enter',
            'Backspace': 'backspace',
        }
        
        if char in commands.keys():
            if char == "Space":
                pyag.getWindowsWithTitle(lastFocussedWindow)[0].activate(); pyag.hotkey('space')
            else:
                pyag.getWindowsWithTitle(lastFocussedWindow)[0].activate(); pyag.press(commands[char])
            return

        splChars = lambda char : char == "?" or char == "." or char == "@" or char == "," 
        Num = lambda char : ord(char) >= 48 and ord(char) <= 58 
        uppercase = lambda char: ord(char) >= 65 and ord(char) <= 90

        if splChars(char) or Num(char):
            pyag.getWindowsWithTitle(lastFocussedWindow)[0].activate(); pyag.press(char)
        elif uppercase(char):
            pyag.getWindowsWithTitle(lastFocussedWindow)[0].activate(); pyag.press(chr(ord(char)+32))
        self.playSound()
        log.debug("Character %s hit on %s", char, lastFocussedWindow)


        
    def moveMouse(self, direction: str, boost: int):
        w, h = pyag.size()
        x, y = pyag.position()
        dist = self.drag * boost
        if direction == 'right' and x+dist <= w:
            pyag.moveRel(dist, 0)
        elif direction == 'left':
            pyag.moveRel(-dist, 0)
        elif direction == 'up':
            pyag.moveRel(0, -dist)
        elif direction == 'down' and y+dist <= h:
            pyag.moveRel(0, dist)
                
    def scrollVertically(self, direction: str, boost: int):
        w, h = pyag.size()
        x, y = pyag.position()
        dist = self.drag * boost

        if direction == 'right' and x+dist <= w:
            pyag.moveRel(dist, 0)
        elif direction == 'left':
            pyag.moveRel(-dist, 0)
        elif direction == 'up':
            pyag.scroll(self.scrollOffset*boost)
        elif direction == 'down' and y+dist <= h:
            pyag.scroll(-self.scrollOffset*boost)

    def click(self, button: str):
        pyag.click(button=button)
        self.recordClick()
        self.playSound()

    def recordClick(self):
        if pyag.getActiveWindow():
            try:
                currentWindowName = pyag.getActiveWindow().title
                if currentWindowName.strip() == "":
                    currentWindowName = "Taskbar"

            except Exception as e:
                log.error("line 112: %s",str(e))

            if currentWindowName not in WINDOW_TITLES and currentWindowName != "Taskbar":
                self.windowQueue.append(currentWindowName)

                if len(self.windowQueue) > 5:
                    self.windowQueue.pop(0)

                log.debug(f"Clicked on **{currentWindowName}**")

            else:
                log.debug("Clicked on its own Window")
    
    def playSound(self):
        mixer.music.load(get_resource_path(CLICK_SOUND))
        mixer.music.play()

    def screenWidth(self) -> int:
        return pyag.size().width

    def screenHeight(self) -> int:
        return pyag.size().height
