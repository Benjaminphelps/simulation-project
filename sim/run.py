import state
import rng_models
import event_handler

# Initialization of lots and cables according to document.
current_state = state.State(

    parking_lots = {
        1 : state.ParkingLot(spots_available=60),
        2 : state.ParkingLot(spots_available=80),
        3 : state.ParkingLot(spots_available=60),
        4 : state.ParkingLot(spots_available=70),
        5 : state.ParkingLot(spots_available=60),
        6 : state.ParkingLot(spots_available=60),
        7 : state.ParkingLot(spots_available=50)
        },

    cables = {
        0: state.Cable(max_capacity = 1000),
        1: state.Cable(max_capacity = 200),
        2: state.Cable(max_capacity = 200),
        3: state.Cable(max_capacity = 200),
        4: state.Cable(max_capacity = 200),
        5: state.Cable(max_capacity = 200),
        6: state.Cable(max_capacity = 200),
        7: state.Cable(max_capacity = 200),
        8: state.Cable(max_capacity = 200),
        9: state.Cable(max_capacity = 200)
        } 
)

# This is an ever-increasing number just to assign unique vehicle ids. 
vehicle_id= 0

# current_state.time always initializes to 0.0
hour_window = current_state.time

# This loop ensures we generate times every hour
while (hour_window <= 23.0):
    print()
    print ("STARTING NEW HOUR WINDOW: ", hour_window)
    print()
    # For this hour: Generate arrival times and schedule their events.
    arrivals = rng_models.generate_arrivals_per_hour(hour_window)
    for arrival_time in arrivals:
        current_state.schedule_event(state.Event(time=arrival_time, type = 'Vehicle Arrives',vehicle_id = vehicle_id))
        vehicle_id +=1

    while (hour_window <= current_state.time <= hour_window+1.0):
        # Terminate if there are no more events
        if(len(current_state.event_queue) == 0):
            break

        # Get the next event
        next_event = current_state.event_queue[0]

        # Update time to next event
        current_state.time = next_event.time

        # Handle the event (Does this actually want to return state? Because it needs to look at state and also change it)
        current_state = event_handler.handle(next_event, current_state)
        print()

        # Remove the event
        current_state.pop_event()

    hour_window +=1.0
    current_state.time = hour_window

print ("-------------------------------------------")
print ("SIMULATION END:")
print ("Total no. of vehicles: ", vehicle_id)
print ("Parking lot 1 spots available: ", current_state.parking_lots[1].spots_available)
print ("Parking lot 2 spots available: ", current_state.parking_lots[2].spots_available)
print ("Parking lot 3 spots available: ", current_state.parking_lots[3].spots_available)
print ("Parking lot 4 spots available: ", current_state.parking_lots[4].spots_available)
print ("Parking lot 5 spots available: ", current_state.parking_lots[5].spots_available)
print ("Parking lot 6 spots available: ", current_state.parking_lots[6].spots_available)
print ("Parking lot 7 spots available: ", current_state.parking_lots[7].spots_available)

