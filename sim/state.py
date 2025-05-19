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
    def __init__(self, spots_available):
        self.spots_available = spots_available
        self.active_vehicles = []  # list of Vehicle
        self.waiting_queue = []  # list of Vehicle

    def remove_spot(self):
        self.spots_available = self.spots_available - 1
    
    def add_spot(self):
        self.spots_available = self.spots_available + 1


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
        self.type = type  # 'Vehicle Arrives', 'Charging Starts', 'Charging Ends', 'Vehicle Departs'
        self.vehicle_id = vehicle_id


class State:
    def __init__(self, parking_lots, cables):
        self.time = 0.0
        self.vehicles = {}  # Dict[int, Vehicle]
        self.parking_lots = parking_lots # Dict[int, ParkingLot]
        self.cables = cables  # Dict[int, Cable]
        self.event_queue = []  # List[Event]
        self.solar_panels = {}  # Dict[int, float]
    
    def schedule_event(self, event): 
        if len(self.event_queue) == 0:
            self.event_queue.append(event)
        elif len(self.event_queue) == 1:
            if event.time < self.event_queue[0].time:
                self.event_queue.insert(0, event)
            else:
                self.event_queue.append(event)
        else:
            time, pos = event.time, len(self.event_queue)-1
            for x in range(len(self.event_queue)):
                if time < self.event_queue[x].time:
                    pos = x
                    break
            self.event_queue.insert(pos, event)

    def pop_event(self):
        self.event_queue.pop(0)