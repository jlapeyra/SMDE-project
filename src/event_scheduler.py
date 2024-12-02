import heapq

class Event:
    def __init__(self, time, action):
        self.time = time
        self.action = action

    def __lt__(self, other:'Event'):
        return self.time < other.time

def event_scheduling_simulation(max_simulation_time):
    # Initialization
    simulation_clock = 0
    event_list = []
    
    def initialize_events():
        """Add initial events to the event list."""
        heapq.heappush(event_list, Event(2, "Event A"))
        heapq.heappush(event_list, Event(5, "Event B"))
        heapq.heappush(event_list, Event(8, "Event C"))

    def run_event(event:Event):
        """Simulate running an event."""
        print(f"Running {event.action} at time {event.time}")

    # Step 1: Initialize simulation
    initialize_events()

    # Step 2: Process events until end of simulation
    while event_list and simulation_clock <= max_simulation_time:
        # Get the first event (smallest time)
        next_event:Event = heapq.heappop(event_list)
        simulation_clock = next_event.time

        # Run the event
        run_event(next_event)

    # Step 3: Output results
    print("Simulation complete. Final time:", simulation_clock)

# Run the simulation
event_scheduling_simulation(max_simulation_time=10)




