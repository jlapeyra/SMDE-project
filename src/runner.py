import random
from km_divisions import TOTAL_LENGTH
from events import Event, getEnterExitEvents

class Runner:
    avg_total_time = 4*60

    def getTimeStretch(self, stretch_length:float):
        avg_time = self.avg_total_time/TOTAL_LENGTH * stretch_length
        std_time = avg_time*0.25
        return abs(random.normalvariate(avg_time, std_time))
    
    def getEventsStretch(self, current_time:float, stretch_length:float) -> tuple[Event, Event]:
        duration = self.getEventsStretch(stretch_length)
        return getEnterExitEvents(current_time, duration)
    
    