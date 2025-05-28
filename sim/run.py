import state
import rng_models
import event_handler
import performance_measures
import copy

# Init state
current_state = state.State()

# Init performance measures
stats = performance_measures.Measures()

# This is an ever-increasing number just to assign unique vehicle ids. 
vehicle_id= 0

# current_state.time always initializes to 0.0
hour_window = current_state.time

# This loop ensures we generate times every hour
print ("-------------------------------------------")
print("SIMULATION START")
while (hour_window <= 23.0):
    # print()
    print ("Hour: ", hour_window)
    # print()
    # For this hour: Generate arrival times and schedule their events.
    arrivals = rng_models.generate_arrivals_per_hour(hour_window)
    for arrival_time in arrivals:
        current_state.schedule_event(state.Event(time=arrival_time, type = 'Vehicle Arrives',vehicle_id = vehicle_id))
        vehicle_id +=1

    while (hour_window <= current_state.time < hour_window+1.0):
        # Terminate if there are no more events
        if(len(current_state.event_queue) == 0):
            break
        
        # Adds a bit of overhead but simplifies pretty well.
        prev_state = copy.copy(current_state)
        # Get the next event
        next_event = current_state.event_queue[0]

        # Update time to next event
        current_state.time = next_event.time
        # print(current_state.time)

        # Save previous state so we can use it in performance measures

        # Handle the event (Does this actually want to return state? Because it needs to look at state and also change it)
        current_state = event_handler.handle(next_event, current_state)

        # Update performance measures based on state before event and state after event
        stats.update_measures(prev_state,current_state)

        # Remove the event
        current_state.pop_event()

    hour_window +=1.0
    current_state.time = hour_window

stats.report_final_measures(current_state)
