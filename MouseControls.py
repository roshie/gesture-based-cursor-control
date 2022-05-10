import pyautogui as pyag
from pygame import mixer

# Import Click sound
clickSound = 'sounds/MouseClick.mp3'

class MouseControls():
    def __init__(self, drag, scrollOffset):
        self.drag = drag # values - 40 to 50
        self.scrollOffset = scrollOffset
        mixer.init()
        
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
        mixer.music.load(clickSound)
        mixer.music.play()