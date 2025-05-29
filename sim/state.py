class Vehicle:
    def __init__(self, id, arrival_time, charging_volume, connection_time,
                 adapted_departure_time, charging_status, assigned_parking):
        self.id = id
        self.arrival_time = arrival_time
        self.charging_volume = charging_volume
        self.adapted_departure_time = adapted_departure_time
        self.charging_status = charging_status  # 'waiting', 'charging', 'finished'
        self.assigned_parking = assigned_parking  # int or None
        self.parking_attempts = []  # list of int
        self.charging_start_time = None  # float or None
        self.charging_end_time = None  # float or None
        self.connection_start_time = None # float or None
        self.connection_end_time = None # float or None

        self.departure_time = None # float or None
 

class ParkingLot:
    def __init__(self, spots_available):
        self.spots_available = spots_available
        self.active_vehicles = []  # list of Vehicle
        self.waiting_queue = []  # list of Vehicle
        self.current_load = 0.0  # current load in kW
    
    #state.parking_lots[1].add_vehicle(vehicle)

    def add_vehicle(self, vehicle):
        self.active_vehicles.append(vehicle)
    def remove_vehicle(self, vehicle):
        self.active_vehicles.remove(vehicle)
    def remove_spot(self):
        self.spots_available = self.spots_available - 1
    
    def add_spot(self):
        self.spots_available = self.spots_available + 1

    # vehicle with 6 kw/h load
    def add_vehicle_load(self):
        self.current_load += 6.0

    def remove_vehicle_load(self):
        self.current_load -= 6.0


class Cable:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.current_load = 0.0
        self.load_time_series = []  # list of (time, load)
        self.overload_time = 0.0
        self.blackout_time = 0.0
        self.is_blacked_out = False


class Event:
    def __init__(self, time, type, vehicle_id):
        self.time = time
        self.type = type  # 'Vehicle Arrives', 'Charging Starts', 'Charging Ends', 'Vehicle Departs'
        self.vehicle_id = vehicle_id


class State:
    def __init__(self, charging_strategy):
        self.charging_strategy = charging_strategy
        self.non_served_vehicles = 0
        self.time = 0.0
        self.vehicles = {}  # Dict[int, Vehicle]
        self.parking_lots = {
        1 : ParkingLot(spots_available=60),
        2 : ParkingLot(spots_available=80),
        3 : ParkingLot(spots_available=60),
        4 : ParkingLot(spots_available=70),
        5 : ParkingLot(spots_available=60),
        6 : ParkingLot(spots_available=60),
        7 : ParkingLot(spots_available=50)
        } # Dict[int, ParkingLot]
        self.cables = {
        1: Cable(max_capacity = 200),
        2: Cable(max_capacity = 200),
        0: Cable(max_capacity = 1000),
        3: Cable(max_capacity = 200),
        4: Cable(max_capacity = 200),
        5: Cable(max_capacity = 200),
        6: Cable(max_capacity = 200),
        7: Cable(max_capacity = 200),
        8: Cable(max_capacity = 200),
        9: Cable(max_capacity = 200)
        }   # Dict[int, Cable]
        self.event_queue = []  # List[Event]
        self.solar_panels = {}  # Dict[int, float]
    
    def update_cable_loads(self):
        self.cables[2].current_load = self.parking_lots[1].current_load
        self.cables[3].current_load = self.parking_lots[2].current_load
        self.cables[4].current_load = self.parking_lots[3].current_load
        self.cables[1].current_load = self.cables[2].current_load + self.cables[3].current_load + self.cables[4].current_load

        self.cables[9].current_load = self.parking_lots[6].current_load
        self.cables[8].current_load = self.parking_lots[5].current_load
        self.cables[7].current_load = self.cables[8].current_load + self.cables[9].current_load
        self.cables[6].current_load = self.parking_lots[7].current_load
        self.cables[5].current_load = self.cables[6].current_load + self.cables[7].current_load

        self.cables[0].current_load = self.cables[1].current_load + self.cables[5].current_load

        for cable in self.cables.values():
            # if cable load >= 110% of max capacity, blackout 
            if cable.current_load >= 1.1 * cable.max_capacity:
                cable.is_blacked_out = True
            else:
                cable.is_blacked_out = False

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
    
    def add_non_served_vehicle(self):
        self.non_served_vehicles += 1