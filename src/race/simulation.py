from scheduler import event_scheduling_simulation
import events as ev
import km_divisions as km
from runner import Runner

events:list[ev.Event] = []
queues = {}
for station in km.AID_STATIONS:
    for aid in station.services:
        queues[id(aid)] = ev.Queue(events)

runners = [
    Runner(i, events, queues)
    for i in range(1, 10+1)
]

for r in runners:
    r.start()

event_scheduling_simulation(events)