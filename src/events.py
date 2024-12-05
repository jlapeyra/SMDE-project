from collections.abc import Iterable, Callable
from utils import join

class Event():
    def __init__(self, time:float, name:str=None, action:Callable=None):
        self.time = time
        self.action = action
        self.name = join(name, f'Event @ {time}')

    def __lt__(self, other:'Event'):
        return self.time < other.time
    
    def run(self):
        print(self.name)
        if self.action != None:
            self.action()


def getEnterExitEvents(start_time:float, duration:float, name:str=None, action:Callable=None):
    enter = Event(time=start_time,
                  action=action,
                  name=join('Enter', name))
    exit = Event(time=start_time+duration,
                 name=join('Exit', name))
    return enter, exit


