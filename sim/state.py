class Vehicle:
    def __init__(self, id, arrival_time, charging_volume, connection_time,
                 adapted_departure_time, charging_status, assigned_parking=None):
        self.id = id
        self.arrival_time = arrival_time
        self.charging_volume = charging_volume
        self.connection_time = connection_time
        self.adapted_departure_time = adapted_departure_time
        self.charging_status = charging_status  # 'waiting', 'charging', 'finished'
        self.assigned_parking = assigned_parking  # int or None
        self.parking_attempts = []  # list of int
        self.charging_start_time = None  # float or None
        self.charging_end_time = None  # float or None


class ParkingLot:
    def __init__(self, num_stations):
        self.num_stations = num_stations
        self.active_vehicles = []  # list of Vehicle
        self.waiting_queue = []  # list of Vehicle


class Cable:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.current_load = 0.0
        self.load_time_series = []  # list of (time, load)
        self.overload_time = 0.0
        self.blackout_time = 0.0


class Event:
    def __init__(self, time, type, vehicle_id):
        self.time = time
        self.type = type  # 'Vehicle Arrives', 'Connection Starts', 'Connection Ends', 'Vehicle Departs'
        self.vehicle_id = vehicle_id


class State:
    def __init__(self, parking_lots, cables):
        self.time = 0.0
        self.vehicles = {}  # Dict[int, Vehicle]
        self.parking_lots = parking_lots # Dict[int, ParkingLot]
        self.cables = cables  # Dict[int, Cable]
        self.event_queue = []  # List[Event]
        self.solar_panels = {}  # Dict[int, float]
    
    # SLOW code that schedules events by resorting the list upon arrival of ANY event
    def schedule_event(self, event):
        self.event_queue.append(event)
        self.event_queue.sort(key=lambda e: e.time)
        
        # Assuming event is already sorted by time
            # if len(self.event_queue) == 0:
            #     self.event_queue.append(event)
            # else:
            #     time, pos = event.time, len(self.event_queue)-1
            #     for x in range(len(self.event_queue)):
            #         if time < self.event_queue[x].time:
            #             pos = x
            #             break
            #     self.event_queue.insert(pos, event)

    def pop_event(self):
        # Since this is one line I feel like we could simply just remove this method and add to the run.py but I don't really mind
        self.event_queue.pop(0)