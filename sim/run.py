import numpy as np
from scipy import stats
import state
import rng_models
import event_handler
import performance_measures
import copy

# Confidence intervals -> Change to reasonable amount of runs and days if you want intervals
# To show instructors: 1 run, 10 days, no CIs
NUM_RUNS = 1
number_of_days = 10
show_intervals = False

# Scenarios for confidence intervals
# To show instructors,
scenarios = [
    ('FCFS - Solar 1,2,6,7 Summer', state.State(charging_strategy=3, season='Summer', solar_scenario='1_2_6_7'))
    # ('ELFS - 1,2,6,7 Summer', state.State(charging_strategy=4, season='Summer', solar_scenario='1_2_6_7'))
]

results = {}

def run_scenario(label, base_state):
    print(f"\nRunning simulations for: {label}")

    cable_1_overload = []
    cable_5_overload = []
    cable_1_blackout = []
    cable_5_blackout = []

    percentage_delayed = []
    average_delay = []
    percentage_not_served = []

    for run in range(NUM_RUNS):
        current_state = copy.deepcopy(base_state)
        stats = performance_measures.Measures()
        vehicle_id = 0
        hour_window = current_state.time

        while hour_window <= (24 * number_of_days - 1):
            print("HOUR: ", hour_window)

            arrivals = rng_models.generate_arrivals_per_hour(hour_window)
            for arrival_time in arrivals:
                current_state.schedule_event(state.Event(time=arrival_time, type='Vehicle Arrives', vehicle_id=vehicle_id))
                vehicle_id += 1

            current_state.schedule_event(state.Event(time=hour_window, type='Solar update', vehicle_id=None))

            while hour_window <= current_state.time < hour_window + 1.0:
                if len(current_state.event_queue) == 0:
                    break
                prev_state = copy.copy(current_state)
                next_event = current_state.event_queue[0]
                current_state.time = next_event.time
                try:
                    vehicle = current_state.vehicles[next_event.vehicle_id]
                except KeyError:
                    pass
                current_state = event_handler.handle(next_event, current_state)
                stats.update_measures(prev_state, current_state)
                current_state.pop_event()

            hour_window += 1.0
            current_state.time = hour_window

        
        analysis = stats.report_final_measures(current_state, vehicle_id + 1, number_of_days)

        cable_1_overload.append(analysis['Cable_1_overload'])
        cable_5_overload.append(analysis['Cable_5_overload'])

        cable_1_blackout.append(analysis['Cable_1_blackout'])
        cable_5_blackout.append(analysis['Cable_5_blackout'])
        
        percentage_delayed.append(analysis['Percentage_delayed'])
        average_delay.append(analysis['Average_delay'])
        percentage_not_served.append(analysis['Percentage_not_served'])

    results[label] = {
        'cable_1_overload': cable_1_overload,
        'cable_5_overload': cable_5_overload,

        'cable_1_blackout': cable_1_blackout,
        'cable_5_blackout': cable_5_blackout,

        'percentage_delayed': percentage_delayed,
        'average_delay': average_delay,
        'percentage_not_served': percentage_not_served
    }

def ci_string(data):
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = stats.t.interval(0.95, len(data) - 1, loc=mean, scale=std_err)
    return f"{mean:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]"

# --- Run all scenarios ---
for label, base_state in scenarios:
    run_scenario(label, base_state)

if show_intervals: 
    # --- Report all CIs ---
    print("\nCONFIDENCE INTERVALS:\n")
    for label in results:
        print(f"Scenario: {label}")
        print("  Cable 1 overload:", ci_string(results[label]['cable_1_overload']))
        print("  Cable 5 overload:", ci_string(results[label]['cable_5_overload']))

        print("  Cable 1 blackout:", ci_string(results[label]['cable_1_blackout']))
        print("  Cable 5 blackout:", ci_string(results[label]['cable_5_blackout']))

        print("  Percentage delayed:", ci_string(results[label]['percentage_delayed']))
        print("  Average delay:", ci_string(results[label]['average_delay']))
        print("  Percentage not served:", ci_string(results[label]['percentage_not_served']))

        print()
