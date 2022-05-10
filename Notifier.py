

class Notifier:
    def __init__(self):
 
        """create an empty observer list"""
 
        self._observers = []
 
    def changeInputMode(self, val: bool, modifier = None):
 
        """Alert the observers"""
 
        for observer in self._observers:
            if modifier != observer:
                observer.changInputMode(val)

    def changeScrollMode(self, val: bool, modifier = None):
 
        """Alert the observers"""
 
        for observer in self._observers:
            if modifier != observer:
                observer.changScrollMode(val)

    def updatePercentage(self, val: int, modifier = None):
        for observer in self._observers:
            if modifier != observer:
                observer.updatPercentage(val)        
 
    def attach(self, observer):
 
        """If the observer is not in the list,
        append it into the list"""
 
        if observer not in self._observers:
            self._observers.append(observer)
 
    def detach(self, observer):
 
        """Remove the observer from the observer list"""
 
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
