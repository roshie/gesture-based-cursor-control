import pyautogui as pyag
from pygame import mixer

# Import Click sound
clickSound = 'sounds/MouseClick.mp3'

class MouseControls():
    def __init__(self, drag, scrollOffset):
        self.drag = drag # values - 40 to 50
        self.scrollOffset = scrollOffset
        mixer.init()

    def enterCharacter(self, char):
        print(f"Pressed Key: {char}")
        commands = {
            'Space': ' ',
            'Enter': 'enter',
            'Backspace': 'backspace',
        }

        if char in commands.keys():
            if char == "Space":
                pyag.hotkey('space')
            else:
                pyag.press(commands[char])
            print(f"pressed {char}")
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
        print(f"pressed {char}")
        
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