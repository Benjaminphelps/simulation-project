class Measures:
    def __init__(self, max_loads, percentage_blackout_time, percentage_underload_time, load_over_time,
                 percentage_delayed_vehicles, average_vehicle_delay, max_delay):

        # Cable load
        self.max_loads = {max_loads} # Dict[int (lot id), int (max load)]
        self.percentage_blackout_time = percentage_blackout_time # Float
        self.percentage_underload_time = percentage_underload_time # Float
        self.load_over_time = load_over_time #Float

        # Departure dleays
        self.percentage_delayed_vehicles = percentage_delayed_vehicles
        self.average_vehicle_delay = average_vehicle_delay
        self.max_delay = max_delay # In document: 'maximum delays' -> Why plural?

    def update_measures(self, before_event, after_event): # -> not sure if we actually need before and after? TBD.
        pass


