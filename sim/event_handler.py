import state
import rng_models

# "Vehicle Arrives", "Charging Starts", "Charging Ends", "Vehicle Departs"
def handle (event, state):
    match event.type:

        case "Vehicle Arrives":
            print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_arrival(event, state)

        case "Charging Starts":
            print("No suppourt for this event yet!")

        case "Charging Departs":
            print("No suppourt for this event yet!")

        case "Vehicle Departs":
            print("Handling event with time: ", event.time, " and type: ", event.type)
            return handle_vehicle_departure(event, state)

        case _:
            print("Unrecognized event!")
    

def handle_arrival (event, state):
    # Pick a parking lot
    lot_choices = [int(x) for x in rng_models.generate_lot_choices()]
    print ("My lot preference list is:, ", lot_choices)
    lot_found = False
    for lot in lot_choices:
        if (state.parking_lots[lot].spots_available > 0):
            print("Found a spot in lot: ",  lot, " which has capacity: ", state.parking_lots[lot].spots_available)

            # Generate a departure
            dep = rng_models.generate_departure_time(state.time)
            print("Departure time was determined to be: ", dep)

            # TODO: Schedule departure event, but i'm really confused about connection times?
            exit(0)

            state.parking_lots[lot].remove_spot()
            lot_found = True
            break
    if not lot_found:
        print("Didn't find a lot! What to do?")

    # If we get here, it means that there was no available lot.

    return state


def handle_vehicle_departure (event, state):
    # Get the vehicle
    vehicle = state.vehicles[event.vehicle_id]
    print("Handling departure for vehicle: ", event.vehicle_id)
    print("Vehicle was in lot: ", vehicle.assigned_parking)
    print("Vehicle is leaving at time: ", event.time)

    # Free up the parking spot
    state.parking_lots[vehicle.assigned_parking].add_spot()

    # Remove the vehicle from the system
    del state.vehicles[event.vehicle_id]

    return state