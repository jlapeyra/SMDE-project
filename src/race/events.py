from collections.abc import Iterable, Callable
from utils import join
import math
import heapq

def format_time(x):
    return f'{int(x//60)}:{int(x%60):02}:{int(x*60%60):02}.{int(x*600%10):01}'

class Event:
    type = 'Event'
    def __init__(self, time:float, name:str=None, action:Callable=None):
        self.time = time
        self.action = action
        self.name = f'{format_time(time)} {self.type}\t{name or ""}'

    def __lt__(self, other:'Event'):
        return self.time < other.time
    
    def run(self):
        print(self.name)
        if self.action is not None: 
            return self.action(self)
        

class Enter(Event):
    type = 'Enter Event'
    # def __init__(self, event:Event, duration:float):
    #     super().__init__(event.time, event.name, event.action)
    #     self.duration = duration

    # def exitEvent(self, notify:Callable = None, queue:'Queue' = None) -> 'Exit':
    #     return Exit(time=self.time + self.duration, name=self.name, notify=notify, queue=queue)

class Exit(Event):
    type = 'Exit  Event'

    def __init__(self, time, name:str = None, action:Callable = None,
                 notify:Callable = None, queue:'Queue' = None):
        super().__init__(time, name, action)
        self.notify = notify
        self.queue = queue

    def run(self):
        super().run()
        if self.notify is not None: self.notify(self)
        if self.queue is not None: self.queue.free(self)

class Task:
    def __init__(self, duration:float, name:str=None, 
                 notify:Callable = None, queue:'Queue' = None, action:Callable=None):
        self.duration = duration
        self.name = name
        self.notify = notify
        self.queue = queue
        self.action = action

    def events(self, time) -> tuple[Enter, Exit]:
        enter = Enter(time=time, name=self.name)
        exit = Exit(time=time+self.duration, name=self.name, notify=self.notify, queue=self.queue)
        return enter, exit
    
    def enqueue_me(self, time):
        assert self.queue
        self.queue.enqueue(self, time)

def add_task(event_list:list[Event], task:Task, time:float):
    enter, exit = task.events(time)
    heapq.heappush(event_list, enter)
    heapq.heappush(event_list, exit)


class Queue:
    def __init__(self, event_list:list, slots:int=math.inf):
        self.queue:list[Task] = []
        self.event_list = event_list
        self.slots = max(1, slots)
        self.occupied = 0
        self.max_occupied = 0
        self.count_queued = 0
        self.time_waiting = 0
        self.max_wait = 0

    def enqueue(self, task:Task, time:float):
        self.queue.append((task, time))
        self.__try_dequeue(time)

    #def enqueue(self, duration:float, name:str=None, notify:Callable = None):
    #    task = Task(duration=duration, name=name, notify=notify, queue=self)
    #    self.queue.append(task)
    
    def __try_dequeue(self, time):
        while self.queue and self.occupied < self.slots:
            task, time_queued = self.queue.pop(0)
            self.count_queued += 1
            self.time_waiting += time - time_queued
            self.max_wait = max(self.max_wait, time - time_queued)
            add_task(self.event_list, task, time)
            self.occupied += 1
            self.max_occupied = max(self.max_occupied, self.occupied)

    def free(self, event:Event):
        self.occupied -= 1
        self.__try_dequeue(event.time)

