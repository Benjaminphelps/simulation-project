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

        self.overload_times = {
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
                # print("new max")
                self.max_loads[key] = current_state.cables[key].current_load
        
        # Update blackout statuses
        for key in current_state.cables.keys():
            # If the cable was blacked out in previous state, then add the time
            # Pretty sure this is true regardless of current state.
            if prev_state.cables[key].is_blacked_out:
                self.blackout_times[key] += current_state.time - prev_state.time
            # load over time
            self.total_loads[key] += current_state.cables[key].current_load * (current_state.time - prev_state.time)

        for key in current_state.cables.keys():
            # If the cable was blacked out in previous state, then add the time
            # Pretty sure this is true regardless of current state.
            if prev_state.cables[key].is_overload:
                self.overload_times[key] += current_state.time - prev_state.time
            # load over time
            # self.total_loads[key] += current_state.cables[key].current_load * (current_state.time - prev_state.time)


        # This will run all the final calculations ncessessary to close out measures.
    def report_final_measures(self, final_state, total_num_vehicles, days):
        print("-------------------------------------------")
        print("SIMULATION END:")
        print()
        print("Elapsed time: ", round(self.elapsed_time, 2))
        print("Total cars per day: ", round(self.total_cars / days, 2))
        print("-------------------------------------------")
        print("CABLE LOAD:")
        print()
        print("Max cable loads: ")
        for cable in self.max_loads:
            print("    ", cable, ": ", round(self.max_loads[cable], 2))
        print()
        print("Blackout/non blackout per cable:")
        header = f"{'Cable':<6}{'Blackout':>12}{'Non-Blackout':>16}{'=':>4}{'Blackout %':>12}{'/':>4}{'Non-Blackout %':>16}"
        print(header)
        print("-" * len(header))
        for cable in self.blackout_times:
            blackout = self.blackout_times[cable]
            non_blackout = self.elapsed_time - blackout
            blackout_pct = (blackout / self.elapsed_time * 100) if self.elapsed_time > 0 else 0
            non_blackout_pct = 100 - blackout_pct
            print(f"{str(cable):<6}{round(blackout, 2):>12.2f}{round(non_blackout, 2):>16.2f}"
                f"{'=':>4}{round(blackout_pct, 2):>12.2f}%{'/':>4}{round(non_blackout_pct, 2):>16.2f}%")
        
        print("Overload/non overload per cable:")
        header = f"{'Cable':<6}{'Overload':>12}{'Non-Overload':>16}{'=':>4}{'Overload %':>12}{'/':>4}{'Non-Overload %':>16}"
        print(header)
        print("-" * len(header))
        for cable in self.overload_times:
            overload = self.overload_times[cable]
            non_overload = self.elapsed_time - overload
            overload_pct = (overload / self.elapsed_time * 100) if self.elapsed_time > 0 else 0
            non_overload_pct = 100 - overload_pct
            print(f"{str(cable):<6}{round(overload, 2):>12.2f}{round(non_overload, 2):>16.2f}"
                f"{'=':>4}{round(overload_pct, 2):>12.2f}%{'/':>4}{round(non_overload_pct, 2):>16.2f}%")
            
                # Summarized overload and blackout % for cable 1 and 5
        def pct(value):
            return round(value / self.elapsed_time * 100, 2) if self.elapsed_time > 0 else 0.0

        o1 = pct(self.overload_times.get(1, 0))
        b1 = pct(self.blackout_times.get(1, 0))
        o5 = pct(self.overload_times.get(5, 0))
        b5 = pct(self.blackout_times.get(5, 0))

        print(f"latex copy and paste: & {o1:.2f} & {b1:.2f} & {o5:.2f} & {b5:.2f}")


        # print load over time
        for i in range(10):
            print(f"Load over time, cable {i}:", round(self.total_loads[i], 2))

        print("-------------------------------------------")
        print("DEPARTURE DELAYS: ")
        delays = 0
        total_delay_time = 0
        maximum_delay = 0
        for vehicle_id in final_state.vehicles:
            try:
                vehicle = final_state.vehicles[vehicle_id]
                if vehicle.charging_end_time > vehicle.departure_time:
                    delays += 1
                    delay = vehicle.charging_end_time - vehicle.departure_time
                    total_delay_time += delay
                    if delay > maximum_delay:
                        maximum_delay = delay
            except TypeError:
                pass

        delay_percentage = 100 * (delays / self.total_cars) if self.total_cars > 0 else 0
        avg_delay = total_delay_time / self.total_cars if self.total_cars > 0 else 0

        print("Percentage of vehicles with a delay: ", round(delay_percentage, 2))
        print("Average delay over all vehicles: ", round(avg_delay, 2))
        print("Max delay: ", round(maximum_delay, 2))
        print("Number of delays: ", delays)
        print("Number of non-served (declined) vehicles: ", final_state.non_served_vehicles)

        percentage_non_served = (
            100* (final_state.non_served_vehicles / total_num_vehicles) if total_num_vehicles > 0 else 0
        )
        avg_non_served_per_day = (
            final_state.non_served_vehicles / days if days > 0 else 0
        )

        print("Percentage of non-served vehicles per day:",  round(percentage_non_served, 2))
        print("Average number of non-served vehicles per day:", round(avg_non_served_per_day, 2))
        def fmt(val):
            rounded = round(val, 2)
            return f"{int(rounded)}" if rounded == int(rounded) else f"{rounded:.2f}"

        latex_delay_pct = fmt(delay_percentage)
        latex_avg_delay = fmt(avg_delay)
        latex_non_served_pct = fmt(percentage_non_served)

        print(f"latex copy and paste: & {latex_delay_pct} & {latex_avg_delay} & {latex_non_served_pct}")

        print("-------------------------------------------")
        print("QUEUE SIZE: ", len(final_state.vehicle_queue))


            
            
