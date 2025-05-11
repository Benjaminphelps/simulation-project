import state
import rng_models

# Initialization
current_state = state.State(
    parking_lots = {
        1 : state.ParkingLot(num_stations=60)

        },
    cables = {
        1: state.Cable(max_capacity = 1000)
        }
)

# Initialize parking lots
# lot = state.ParkingLot(id=1, num_stations=60)

totalArrs = 0
# Change later to 23.o
while (current_state.time <= 1.0):
    # Next: get a bunch of interarrival times for the hour. CURRENTLY ONLY OPERATIVE FOR THE ONE HOUR!
    arrivals = rng_models.generate_arrivals_per_hour(current_state.time)
    print(arrivals)
    current_state.time+=1000

print (totalArrs)

