# %%
import numpy as np
import pandas as pd

# Generate arrivals for a given hour
# Assumed to be correct - averaging around 750 which is perfect.
def generate_arrivals_per_hour(actual_hour):
    modified_hour = actual_hour % 24
    arrivals_dataset = pd.read_csv('../data/arrival_hours.csv', delimiter=';')
    arrivals_dataset['Share_of_charging_transactions'] = arrivals_dataset['Share_of_charging_transactions'].str.replace(',','.').astype(float)

    mu = arrivals_dataset['Share_of_charging_transactions'][modified_hour] * 750
    times = np.sort(np.random.uniform(actual_hour,actual_hour+1,np.random.poisson(mu))).tolist()
    return times


def generate_lot_choices():
    lot_options = np.array([1, 2, 3, 4, 5, 6, 7])
    probabilities = np.array([15, 15, 15, 20, 15, 10, 10]) / 100  # Convert percentages to proportions

    # Draw 3 unique samples according to the distribution
    return np.random.choice(lot_options, size=3, replace=False, p=probabilities)

def generate_charging_duration():
    charging_volume_dataset = pd.read_csv('../data/charging_volume.csv', delimiter=';')
    charging_volume_dataset['Share_of_charging_transactions'] = charging_volume_dataset['Share_of_charging_transactions'].str.replace(',', '.').astype(float)
    volume_probs = charging_volume_dataset['Share_of_charging_transactions'].values
    volume_bins = charging_volume_dataset['Charging_volume_[kWh]'].values  # Assume these are integers: 0 = [0,1), 1 = [1,2), etc.

    # Sample charging volume bin and get actual volume
    volume_bin = np.random.choice(volume_bins, p=volume_probs)
    charging_volume = np.random.uniform(volume_bin, volume_bin + 1)
    charging_time = charging_volume / 6  # charging rate is 6 kW
    # print("Charging time (hours): ", charging_time)

    return charging_time

def generate_departure_time(current_time, total_charging_time):
    # Load and prepare connection time distribution
    connection_time_dataset = pd.read_csv('../data/connection_time.csv', delimiter=';')
    connection_time_dataset['Share_of_charging_transactions'] = connection_time_dataset['Share_of_charging_transactions'].str.replace(',', '.').astype(float)
    conn_probs = connection_time_dataset['Share_of_charging_transactions'].values
    conn_bins = connection_time_dataset['Connection_time_to_charging_station_[h]'].values  # 0 = [0,1), etc.


    # Sample connection time bin and get actual time
    conn_bin = np.random.choice(conn_bins, p=conn_probs)
    sampled_conn_time = np.random.uniform(conn_bin, conn_bin + 1)
    

    # Enforce minimum connection time
    min_required_conn_time = 1.4 * total_charging_time
    connection_time = max(sampled_conn_time, min_required_conn_time)

    # Compute departure time
    departure_time = current_time + connection_time
    return departure_time
    


