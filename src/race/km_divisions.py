import random
from dataclasses import dataclass, field
from abc import ABC
from scipy import stats
import math

class Aid(ABC):  #service in aid station
    num_queues:int = math.inf
    prob_some_use:float = 1
    period_use:float
    mean_duration:float

    def __init__(self, num_queues=None):
        if num_queues is not None:
            self.num_queues = num_queues

    def prob_use(self, time_since_last_use:float):
        return stats.expon.cdf(time_since_last_use, scale=self.period_use)*self.prob_some_use
    
    def decide_use(self, time_since_last_use:float):
        return random.random() < self.prob_use(time_since_last_use)
    
    def duration(self):
        return abs(random.normalvariate(self.mean_duration, self.mean_duration*0.3))
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    def __str__(self) -> str:
        return self.__class__.__name__

class WC(Aid):
    period_use=5*60
    prob_some_use=0.25
    mean_duration=45/60

class Water(Aid):
    period_use=20
    mean_duration=5/60

class Food(Aid):
    period_use=40
    mean_duration=5/60

TOTAL_LENGTH = 42.195 #km marathon
    
@dataclass
class KM: #start, aid station or finish
    km_point:float
    services:list[Aid] = field(default_factory=list)

AID_STATIONS = [
    KM(0),
    KM(5,    [WC(20), Water(60)]),
    KM(10,   [WC(20), Water(45)]),
    KM(15,   [WC(20), Water(30)]),
    KM(20,   [WC(20), Water(30), Food(20)]),
    KM(25,   [WC(20), Water(20), Food(20)]),
    KM(27.5, [WC(20), Water(20)]),
    KM(30,   [WC(20), Water(20), Food(20)]),
    KM(35,   [WC(20), Water(20), Food(20)]),
    KM(37.5, [WC(20), Water(20)]),
    KM(40,   [WC(20), Water(20), Food(20)]),
    KM(TOTAL_LENGTH)
]
# source: https://www.zurichmaratobarcelona.es/wp-content/uploads/2024/05/Mapa-Circuit-ZMB25-1.pdf

KM0 = AID_STATIONS[0]

km_points = [km.km_point for km in AID_STATIONS]

stretches = list(zip(km_points[:-1], km_points[1:]))

def stretch_col(start, end):
    if 27.5 in (start, end): start, end = 25, 30
    if 37.5 in (start, end): start, end = 35, 40
    return f'{start}-{end}K'

__NEXT_KM_POINT = {start:end for start,end in stretches}
__DICT_STATIONS = {km.km_point:km for km in AID_STATIONS}

def next(current:KM|tuple[float,float]) -> KM|tuple[float,float]:
    if isinstance(current, KM):
        current_km = current.km_point
        next_km = __NEXT_KM_POINT.get(current_km)
        if next_km is None:
            return None
        else:
            return current_km, next_km
    else:
        _, km = current
        return __DICT_STATIONS.get(km)
