import heapq
from numbers import Number
from collections.abc import Iterable, Callable
from utils import join_nullables
import math

class Event():
    def __init__(self, time:float, name:str=None, action:Callable=None, next:'Iterable[Event]|Callable[[],Iterable[Event]]'=None):
        self.time = time
        self.action = action
        self.next = next
        self.name = join_nullables(name, f'Event @ {time}')

    def __lt__(self, other:'Event'):
        return self.time < other.time
    
    def run(self):
        print(self.name)
        if self.action != None:
            self.action()
    
    def getNext(self, time) -> Iterable['Event']:
        if self.next == None: return []
        if isinstance(self.next, Iterable): return self.next
        if isinstance(self.next, Callable): return self.next()
        raise ValueError('next must be None, Iterable or Callable')


def event_scheduling_simulation(events:list[Event]):
    events = heapq.heapify(events)
    while events: #and simulation_clock <= max_simulation_time:
        event = heapq.heappop(events)  # Get the first event (smallest time)
        event.run()
        for event in event.getNext():
            heapq.heappush(event)


def getEnterExitEvents(start_time, duration, name=None, action=None, next=None):
    enter = Event(time=start_time,
                  action=action,
                  name=join_nullables('Enter', name))
    exit = Event(time=start_time+duration,
                 next=next,
                 name=join_nullables('Exit', name))
    return enter, exit

class QueueEvent(Event):
    queue:list['QueueEvent']

    def __init__(self, queue:list['QueueEvent'], current_time:float, name: str = None, action: Callable = None, next: Iterable[Event] | Callable[[], Iterable[Event]] = None):
        self.queue = queue
        time = current_time #if queue is empty, execute now, else 
        super().__init__(time=time, name=name, action=action, next=next)

    def getNext(self) -> Iterable[Event]:
        self.queue.pop(0)
        return super().getNext()


