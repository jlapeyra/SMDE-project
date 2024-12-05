import heapq
from events import Event, getEnterExitEvents


def event_scheduling_simulation(events:list[Event]):
    events = heapq.heapify(events)
    while events: #and simulation_clock <= max_simulation_time:
        event = heapq.heappop(events)  # Get the first event (smallest time)
        event.run()
        