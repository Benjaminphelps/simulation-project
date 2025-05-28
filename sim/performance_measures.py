class Measures:
    def __init__(self, max_loads, total_overload_time, total_underload_time, load_over_time,
                 percentage_delayed_vehicles, average_vehicle_delay, max_delay):

        # Cable load
        self.max_loads = max_loads # Dict[int (lot id), int (max load)]
        self.total_overload_time = total_overload_time # Float
        self.percentage_blackout_time = 0
        self.percentage_underload_time = 0
        self.load_over_time = load_over_time #Float

        # Departure dleays
        self.percentage_delayed_vehicles = percentage_delayed_vehicles
        self.average_vehicle_delay = average_vehicle_delay
        self.max_delay = max_delay # In document: 'maximum delays' -> Why plural?

    def update_measures(self, prev_event, current_event): # -> not sure if we actually need before and after? TBD.

        # Update max loads
        for key in current_event.cables.keys():
            # print("Key!: ", key, " and load!: ", after_event.cables[key].current_load)
            if self.max_loads[key] < current_event.cables[key].current_load:
                self.max_loads[key] = current_event.cables[key].current_load
        
        # Update total blackout / non blackout time
        # For each cable: if I was on 'overload' at prev event then add (current_event.time-prev_event.time) to blackout (and vice versa)


        # Calculate load over time (what is load over time, actually?)

    

        # After cable load and stuff is handled, can actually update all the measures.
        print("!!UPDATING MEASURES!!!")


# This will run all the final calculations ncessessary to close out measures.
def report_final_measures(self):
    pass