import state as s
import rng_models

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
    # Instantiate a vehicle
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
        if (state.parking_lots[lot].spots_available > 0):
            # print("Found a spot in lot: ",  lot, " which has capacity: ", state.parking_lots[lot].spots_available)            
            # Vehicle now knows its lot, so it can be set
            vehicle.assigned_parking = lot
            # Also put the Vehicle in the lot
            state.parking_lots[lot].add_vehicle(vehicle)

            # Assumption #1: When a car is in a lot, it's connection time starts right away.
            vehicle.connection_start_time = event.time
            # Assumption for baseline strategy vehicle begins charging right away
            # This line will become something more dynamic in the future.
            vehicle.charging_start_time = event.time

            # schedule a start for charging
            state.schedule_event(s.Event(time=vehicle.charging_start_time, type='Charging Starts', vehicle_id=vehicle.id))
            state.parking_lots[lot].remove_spot()

            lot_found = True
            break
    if not lot_found:
        print("Didn't find a lot! What to do?")

    # If we get here, it means that there was no available lot.

    return state


def handle_charging_start(event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]
    # print("Handling charging start for vehicle: ", event.vehicle_id)
    # print("Vehicle is in lot: ", vehicle.assigned_parking)
    # print("Vehicle is starting to charge at time: ", event.time)

    # Update the vehicle's status
    vehicle.charging_status = 'charging'
    vehicle.charging_start_time = event.time
    vehicle.charging_end_time = event.time + rng_models.generate_charging_time(event.time)

    state.schedule_event(s.Event(time=vehicle.charging_end_time, type='Charging Ends', vehicle_id=event.vehicle_id) )

    return state


def handle_charging_end(event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]
    # print("Handling charging end for vehicle: ", event.vehicle_id)
    # print("Vehicle was in lot: ", vehicle.assigned_parking)
    # print("Vehicle started charging at: ", vehicle.charging_start_time)
    # print("Vehicle has finished charging at time: ", event.time)
    total_charging_time = event.time - vehicle.charging_start_time
    elapsed_connection_time = event.time - vehicle.connection_start_time

    vehicle.charging_status = 'finished'
    vehicle.charging_end_time = 'time'

    # Yes, this seems correct.
    dep = rng_models.generate_departure_time(event.time, total_charging_time, elapsed_connection_time)


    # Just making this field for debugging reasons.
    vehicle.departure_time = dep

    state.schedule_event(s.Event(time=dep, type='Vehicle Departs', vehicle_id=event.vehicle_id) )

    return state


def handle_vehicle_departure (event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]
    # print("Handling departure for vehicle: ", event.vehicle_id)
    # print("Vehicle was in lot: ", vehicle.assigned_parking)
    # print("Vehicle entered lot at time", vehicle.connection_start_time)
    # print("Vehicle is now leaving at time: ", event.time)

    # Free up the parking spot
    state.parking_lots[vehicle.assigned_parking].add_spot()

    # Also remove car from lot
    state.parking_lots[vehicle.assigned_parking].remove_vehicle(vehicle)


    # Remove the vehicle from the system
    del state.vehicles[event.vehicle_id]

    return state