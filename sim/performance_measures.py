class Measures:
    def __init__(self):
        # Elapsed time
        self.elapsed_time = 0
        # Number cars
        self.total_cars = 0
        # Cable load
        self.max_loads ={
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0
        }
        self.blackout_times = {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0
        }
        self.total_loads = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0
        }
        self.total_overload_time = 0 # Float
        self.percentage_blackout_time = 0
        self.percentage_underload_time = 0
        self.load_over_time = 0 #Float

        # Departure dleays
        self.percentage_delayed_vehicles = 0
        self.average_vehicle_delay = 0
        self.max_delay = 0 # In document: 'maximum delays' -> Why plural?

    def update_measures(self, prev_state, current_state): # -> not sure if we actually need before and after? TBD.
        self.elapsed_time = current_state.time
        # Update car counter
        if current_state.event_queue[0].type == 'Vehicle Arrives':
            self.total_cars +=1
        # Update max loads
        for key in current_state.cables.keys():
            # print("Key!: ", key, " and load!: ", after_event.cables[key].current_load)
            if self.max_loads[key] < current_state.cables[key].current_load:
                self.max_loads[key] = current_state.cables[key].current_load
        
        # Update blackout statuses
        for key in current_state.cables.keys():
            # If the cable was blacked out in previous state, then add the time
            # Pretty sure this is true regardless of current state.
            if prev_state.cables[key].is_blacked_out:
                self.blackout_times[key] += current_state.time - prev_state.time
            # load over time
            self.total_loads[key] += current_state.cables[key].current_load * (current_state.time - prev_state.time)
                
        # Update total blackout / non blackout time
        # For each cable: if I was on 'overload' at prev event then add (current_event.time-prev_event.time) to blackout (and vice versa)


        # Calculate load over time (what is load over time, actually?) Assuming load over time is (per cable): sum of loads / time

    

        # After cable load and stuff is handled, can actually update all the measures.


        # This will run all the final calculations ncessessary to close out measures.
    def report_final_measures(self, final_state):
        print ("-------------------------------------------")
        print ("SIMULATION END:")
        print()
        print("Elapsed time: ", self.elapsed_time)
        print("Total cars: ", self.total_cars)
        print("-------------------------------------------")
        print("CABLE LOAD:")
        print()
        print("Max cable loads: ")
        for cable in self.max_loads:
            print("    ", cable,": ", self.max_loads[cable])
        print()
        print("Blackout/non blackout per cable: ")
        for cable in self.blackout_times:
            print("    ", cable,": ", self.blackout_times[cable], " / ", self.elapsed_time-self.blackout_times[cable])

        print("TODO: Load over time (how is this defined?)")
        # print load over time
        print("Load over time, cable 0:", self.total_loads[0])
        print("Load over time, cable 1:", self.total_loads[1])
        print("Load over time, cable 2:", self.total_loads[2])
        print("Load over time, cable 3:", self.total_loads[3])
        print("Load over time, cable 4:", self.total_loads[4])
        print("Load over time, cable 5:", self.total_loads[5])
        print("Load over time, cable 6:", self.total_loads[6])
        print("Load over time, cable 7:", self.total_loads[7])
        print("Load over time, cable 8:", self.total_loads[8])
        print("Load over time, cable 9:", self.total_loads[9])

        print("-------------------------------------------")
        print("DEPARTURE DELAYS: ")
        # As of now: No departure delays. Maybe it's true that this only happens when we change charging strategy? We'll see.
        delays = 0
        total_delay_time = 0
        maximum_delay = 0
        for vehicle_id in final_state.vehicles:
            try:
                if (final_state.vehicles[vehicle_id].charging_end_time > final_state.vehicles[vehicle_id].departure_time):
                    delays += 1
                    total_delay_time += (final_state.vehicles[vehicle_id].charging_end_time - final_state.vehicles[vehicle_id].departure_time)
                    if total_delay_time > maximum_delay:
                        maximum_delay = total_delay_time
            except(TypeError):
                pass
        print("Percentage of vehicles with a delay: ", 100*(delays/self.total_cars))
        print("Average delay over all vehicles: ", total_delay_time/self.total_cars)
        print("Max delay: ", maximum_delay)
            # print(final_state.vehicles[vehicle_id].charging_end_time, " ", final_state.vehicles[vehicle_id].departure_time)
        print("Percentage of non-served vehicles per day: NEED DAY ITERATION SUPPOURT")
        print("Average number of non-served vehicles per day: NEED DAY ITERATION SUPPOURT")      
        print("-------------------------------------------")
        
        
