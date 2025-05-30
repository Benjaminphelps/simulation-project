import state as s
import rng_models
import math

PRICE_BLOCKS = [
    (0, 8, 16),
    (8, 16, 18),
    (16, 20, 22),
    (20, 24, 20),
]

FCFS_QUEUE = [] 

def get_price(hour):
    hour %= 24
    for start, end, price in PRICE_BLOCKS:
        if start <= hour < end:
            return price
    return 0  # should not happen

def get_price_blocks_in_window(start_time, end_time):
    """Returns all distinct hourly block boundaries within [start_time, end_time]"""
    blocks = []
    for day in range(int(start_time // 24), int(end_time // 24) + 1):
        for (start_h, end_h, _) in PRICE_BLOCKS:
            block_start = day * 24 + start_h
            if block_start >= end_time:
                break
            if block_start >= start_time:
                blocks.append(block_start)
    return sorted(set(blocks + [start_time]))  # include exact start time


def estimate_charging_cost(start_time, duration):
    cost = 0.0
    t = start_time
    remaining = duration
    while remaining > 0:
        current_hour = t % 24
        end_of_hour = int(t) + 1
        time_in_current_hour = min(end_of_hour - t, remaining)
        cost += get_price(current_hour) * 6 * time_in_current_hour
        t += time_in_current_hour
        remaining -= time_in_current_hour
    return cost


# "Vehicle Arrives", "Charging Starts", "Charging Ends", "Vehicle Departs"
def handle (event, state):
    match event.type:
        case "Vehicle Arrives":
            # print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_arrival(event, state)

        case "Charging Starts":
            # print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_charging_start(event, state)

        case "Charging Ends":
            # print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_charging_end(event, state)
        
        case "Vehicle Departs":
            # print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_vehicle_departure(event, state)

        case _:
            print("Unrecognized event: ", event.type)

def handle_arrival (event, state):
    # Handling arrival likely varies the most w/ respect to strategies
    # first implement price levels
    # Instantiate a vehicle
    # print("Handling arrival")
    vehicle = s.Vehicle(id=event.vehicle_id,
                            arrival_time=event.time,
                            charging_volume=0,  # to be set later
                            connection_time=0, # to be set later
                            adapted_departure_time=0, # to be set later
                            charging_status='waiting', 
                            assigned_parking=None,  # not sure yet
                            )
    state.vehicles[event.vehicle_id] = vehicle
    # Pick a parking lot
    lot_choices = [int(x) for x in rng_models.generate_lot_choices()]
    # print ("My lot preference list is:, ", lot_choices)
    lot_found = False
    for lot in lot_choices:
        # Need to change this for FCFS ... ? 
        
        if (state.parking_lots[lot].spots_available > 0):         
            # Vehicle now knows its lot, so it can be set
            vehicle.assigned_parking = lot
            # Also put the Vehicle in the lot
            state.parking_lots[lot].add_vehicle(vehicle)

            # When a car is in a lot, it's connection time starts right away.
            vehicle.connection_start_time = event.time

            # Calculate your charging duration and adapted desired departure time immediately
            vehicle.charging_duration = rng_models.generate_charging_duration()

            vehicle.adapted_departure_time = rng_models.generate_departure_time(vehicle.connection_start_time, vehicle.charging_duration)

            # print("Charging duration: ", vehicle.charging_duration, "Adapted departure time:", vehicle.adapted_departure_time)

            # Assumption for baseline strategy vehicle begins charging right away
            # This line will become something more dynamic in the future.
            if (state.charging_strategy == 1):
                vehicle.charging_start_time = event.time
                # schedule a start for charging
                state.schedule_event(s.Event(time=vehicle.charging_start_time, type='Charging Starts', vehicle_id=vehicle.id))
                state.parking_lots[lot].remove_spot()

                lot_found = True
            
            # Price-driven
            elif (state.charging_strategy == 2):
                t_min = state.time
                t_max = (vehicle.adapted_departure_time)-(vehicle.charging_duration)

                candidate_times = get_price_blocks_in_window(t_min, t_max)
                candidate_times.append(t_max)  # add the latest possible start time
                candidate_times = sorted(set(candidate_times))  # deduplicate

                best_time = t_min
                best_cost = float('inf')
            
                for t in candidate_times:
                    if t + vehicle.charging_duration > vehicle.adapted_departure_time:
                        continue
                    cost = estimate_charging_cost(t, vehicle.charging_duration)
                    if cost < best_cost:
                        best_cost = cost
                        best_time = t

                vehicle.charging_start_time = best_time

                # schedule a start for charging
                state.schedule_event(s.Event(time=vehicle.charging_start_time, type='Charging Starts', vehicle_id=vehicle.id))
                state.parking_lots[lot].remove_spot()

                lot_found = True

            # FCFS
            # Overloads should now be impossible (and by this measure, also blackouts).
            elif (state.charging_strategy == 3):
                # If adding a vehicle would overload cable, then add it to the FCFS queue (pretty sure the max capacity is being handled incorrectly)
                if state.parking_lots[lot].current_load + 6.0 > state.cables[lot].max_capacity:
                    FCFS_QUEUE.append(vehicle)
                else:
                    # Otherwise, vehicle can start charging right away
                    if len(FCFS_QUEUE) == 0:
                        vehicle.charging_start_time = event.time
                    else:
                        FCFS_QUEUE.append(vehicle)
                        vehicle = FCFS_QUEUE.pop(0)  # Get the first vehicle in the queue
                        vehicle.charging_start_time = event.time
                
                    # schedule a start for charging
                    state.schedule_event(s.Event(time=vehicle.charging_start_time, type='Charging Starts', vehicle_id=vehicle.id))
                    state.parking_lots[lot].remove_spot()

                    lot_found = True
                        

            # ELFS
            elif (state.charging_strategy == 4):
                pass

            else:
                print("Charging strategy not suppourted!")
                exit(1)
            break
    if not lot_found:
        state.add_non_served_vehicle()

    # If we get here, it means that there was no available lot.

    return state


def handle_charging_start(event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]

    # Update the vehicle's status
    vehicle.charging_status = 'charging'

    vehicle.charging_end_time = state.time + vehicle.charging_duration

    state.parking_lots[vehicle.assigned_parking].add_vehicle_load()

    # Update cable loads
    state.update_cable_loads()  # Assuming 6 kW charging rate

    state.schedule_event(s.Event(time=vehicle.charging_end_time, type='Charging Ends', vehicle_id=event.vehicle_id) )

    return state


def handle_charging_end(event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]

    # Unplug
    state.parking_lots[vehicle.assigned_parking].remove_vehicle_load()

    # Change status
    vehicle.charging_status = 'finished'
    vehicle.charging_end_time = state.time

    # Set departure time according to adapted departure time
    dep = vehicle.adapted_departure_time

    # Update cable loads
    state.update_cable_loads()

    # Just making this field for debugging reasons.
    vehicle.departure_time = dep

    state.schedule_event(s.Event(time=dep, type='Vehicle Departs', vehicle_id=event.vehicle_id) )

    # If FCFS queue is not empty, we can start charging the next vehicle
    # if state.charging_strategy == 3 and len(FCFS_QUEUE) > 0:
    #     next_vehicle = FCFS_QUEUE.pop(0)
    #     next_vehicle.charging_start_time = state.time
    #     next_vehicle.charging_status = 'charging'
    #     state.schedule_event(s.Event(time=next_vehicle.charging_start_time, type='Charging Starts', vehicle_id=next_vehicle.id))
    #     state.parking_lots[next_vehicle.assigned_parking].remove_spot()

    return state


def handle_vehicle_departure (event, state):
    # print("Handling departure")
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]

    # Free up the parking spot
    state.parking_lots[vehicle.assigned_parking].add_spot()

    # Also remove car from lot
    state.parking_lots[vehicle.assigned_parking].remove_vehicle(vehicle)


    # Remove the vehicle from the system
    del state.vehicles[event.vehicle_id]

    return state