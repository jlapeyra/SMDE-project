import random
from km_divisions import TOTAL_LENGTH
from events import Event, Task, add_task
import numpy as np
import pandas as pd
import groups
import km_divisions as km
from scipy.stats import gaussian_kde
import random
from weather_effect import Weather, reverse_effect

__RUNNER_DATA = pd.read_csv('data/runner_data.csv')

__RUNNER_DATA = __RUNNER_DATA.apply(reverse_effect, axis=1)

def notna(data):
    return list(filter(pd.notna, data))

def __kde_partial_relative_speeed() -> dict[tuple,gaussian_kde]:
    retorn = {}
    DATA_PRS = pd.read_csv('data/partial_relative_speed.csv')
    for group_id, group in groups.getGroups(DATA_PRS, ['Time']).items():
        for stretch in km.stretches:
            data = DATA_PRS[group][km.stretch_col(*stretch)]
            retorn[group_id, stretch] = gaussian_kde(notna(data))
    return retorn

def __kde_total_time() -> dict[tuple,gaussian_kde]:
    retorn = {}
    for group_id, group in groups.getGroups(__RUNNER_DATA, ['Gender', 'Age']).items():
        data = __RUNNER_DATA[group]['Time']
        retorn[group_id] = gaussian_kde(notna(data))
    return retorn

def __kde_age() -> dict[str,gaussian_kde]:
    return {g : gaussian_kde(notna(
            __RUNNER_DATA[__RUNNER_DATA['Gender'] == g]['Age']
        )) 
        for g in ('F', 'M')}

def __rate_males() -> dict[str,float]:
    return float(np.mean(__RUNNER_DATA['Gender'] == 'M'))

KDE_PARTIAL_RELATIVE_SPEED = __kde_partial_relative_speeed()
KDE_TOTAL_TIME = __kde_total_time()
KDE_AGE = __kde_age()
RATE_MALES = __rate_males()

def kde_estimate(kde:gaussian_kde):
    return kde.resample(1)[0][0]



class Runner:
    def __init__(self, bib, event_list:list, queues:dict, weather:Weather=None):
        self.bib = bib
        self.gender = ['M', 'F'][random.random() > RATE_MALES]
        self.age = int(kde_estimate(KDE_AGE[self.gender]))
        self.age_group = groups.getGroup(self.age, 'Age')
        self.expected_time = float(kde_estimate(KDE_TOTAL_TIME[self.gender, self.age_group]))
        if weather:
            self.expected_time *= weather.effect(self.gender)
        self.expected_speed = TOTAL_LENGTH/self.expected_time
        self.time_group = groups.getGroup(self.expected_time, 'Time')

        self.last_use = {
            km.WC.__name__: 0,
            km.Water.__name__: 0,
            km.Food.__name__: 0
        }

        self.current = km.KM0
        self.pending = []
        self.event_list = event_list
        self.queues = queues


    def getTimeStretch(self, stretch:tuple[float,float]):
        stretch_length = stretch[1] - stretch[0]
        speed = self.expected_speed * kde_estimate(KDE_PARTIAL_RELATIVE_SPEED[(self.time_group,), stretch])
        time = stretch_length/speed
        return time
    
    def __next(self, time) -> Task:
        while self.pending:
            aid = self.pending.pop(0)
            key = aid.__class__.__name__
            if aid.decide_use(time - self.last_use[key]):
                def reset_use(event:Event):
                    self.last_use[key] = event.time
                return Task(
                    duration=aid.duration(), 
                    name=f'{self.name()} {key} at km{self.current.km_point}',
                    queue=self.queues.get(id(aid)),
                    action=reset_use,
                    notify=self.next
                )
        
        self.current = km.next(self.current)

        if not self.current:
            return None

        if isinstance(self.current, km.KM):
            self.pending = list(self.current.services) #copy
            return self.__next(time)
        
        stretch = self.current
        start, end = stretch
        return Task(
            duration=self.getTimeStretch(stretch),
            name=f'{self.name()} run km{start}-{end}',
            notify=self.next
        )
    

    def next(self, event:Event):
        task = self.__next(event.time)
        if task:
            if task.queue:
                task.enqueue_me(event.time)
            else:
                add_task(self.event_list, task, event.time)

    def name(self):
        return f'Runner {self.bib}_{self.age}{self.gender}_{format_time(self.expected_time)}'
    
    def start(self):
        self.next(Event(time=0))

                
def format_time(x):
    return f'{int(x//60)}H{int(x%60):02}'