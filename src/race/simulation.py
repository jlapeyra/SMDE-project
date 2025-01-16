import sys
try:
    NUM_RUNNERS = int(sys.argv[1])
    levels = ['lo', 'me', 'hi']
    WEATHER_PARAMS = [levels[int(sys.argv[2][i])] for i in range(3)]
except Exception as e:
    print(f'USAGE: python {sys.argv[0]} NUM_RUNNERS WEATHER [FILE_OUT]')
    print('\tWEATHER is a 3-long string with characters 0,1,2,')
    print('\trepresenting temperature, humidity, and wind, respectively,')
    print('\twhere values 0,1,2 represent low, medium, and high, repectively')
    print(f'Exemple: python {sys.argv[0]} 1_000 111')
    exit()

from scheduler import event_scheduling_simulation
import events as ev
import km_divisions as km
from weather_effect import Weather
from runner import Runner
import math

weather = Weather(*WEATHER_PARAMS)

events:list[ev.Event] = []
queues = {}
aid_km = {}
for station in km.AID_STATIONS:
    for aid in station.services:
        aid.num_queues = aid.num_queues*NUM_RUNNERS//10_000
        if aid.num_queues <= 4: aid.num_queues += 1
        queues[id(aid)] = ev.Queue(events, aid.num_queues)
        aid_km[id(aid)] = station.km_point, str(aid)

runners = [
    Runner(i, events, queues, weather)
    for i in range(1, NUM_RUNNERS)
]

for r in runners:
    r.start()

event_scheduling_simulation(events)

for id_, queue in queues.items():
    queue:ev.Queue
    kmp, aid = aid_km[id_]
    if queue.count_queued:
        mean_wait = f'mean {queue.time_waiting/queue.count_queued*60:.1f} s, max {queue.max_wait*60:.1f} s'
    else:
        mean_wait = 'NA'
    print(f'Station km {kmp} {aid}:'.ljust(23, ' '),
          f'Wait {mean_wait}'.ljust(30),
          f'Max use {queue.max_occupied}  Capacity {queue.slots}')