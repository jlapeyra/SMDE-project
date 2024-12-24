import random
from dataclasses import dataclass, field
from abc import ABC
from scipy import stats

class Aid(ABC):  #service in aid station
    num_queues:int = None
    period_use:float
    mean_duration:float

    def prob_use(self, time_since_last_use:float):
        return stats.expon.cdf(time_since_last_use, scale=self.period_use)
    
    def decide_use(self, time_since_last_use:float):
        return random.random() < self.prob_use(time_since_last_use)
    
    def duration(self):
        return abs(random.normalvariate(self.mean_duration, self.mean_duration*0.3))
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    def __str__(self) -> str:
        return self.__class__.__name__

class WC(Aid):
    num_queues=10
    period_use=4*60
    mean_duration=1

class Water(Aid):
    num_queues=30
    period_use=20
    mean_duration=5/60

class Food(Aid):
    num_queues=30
    period_use=40
    mean_duration=5/60

TOTAL_LENGTH = 42.195 #km marathon
    
@dataclass
class KM: #start, aid station or finish
    km_point:float
    services:list[Aid] = field(default_factory=list)

aid_stations = [
    KM(0),
    KM(5,    [WC, Water]),
    KM(10,   [WC, Water]),
    KM(15,   [WC, Water]),
    KM(20,   [WC, Water, Food]),
    KM(25,   [WC, Water, Food]),
    KM(27.5, [WC, Water]),
    KM(30,   [WC, Water, Food]),
    KM(35,   [WC, Water, Food]),
    KM(37.5, [WC, Water]),
    KM(40,   [WC, Water, Food]),
    KM(TOTAL_LENGTH)
]
# source: https://www.zurichmaratobarcelona.es/wp-content/uploads/2024/05/Mapa-Circuit-ZMB25-1.pdf

km_points = [km.km_point for km in aid_stations]
TOTAL_LENGTH_COL = f'{TOTAL_LENGTH}K'