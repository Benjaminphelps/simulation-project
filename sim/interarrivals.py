# %%
import numpy as np
import pandas as pd


# Open csv file
# %%
arrivals_dataset = pd.read_csv('../data/arrival_hours.csv', delimiter=';')
arrivals_dataset['Share_of_charging_transactions'] = arrivals_dataset['Share_of_charging_transactions'].str.replace(',','.').astype(float)
arrivals_dataset.head()
# %%

# %%
# I'm changing this so you pass it a single hour, as per reccomendation on may 6 meeting.
def generate_arrivals_per_hour(hour):
    mu = arrivals_dataset['Share_of_charging_transactions'][hour] * 750
    print ("mu: ", mu)
    times = np.sort(np.random.uniform(0,60,np.random.poisson(mu))).tolist()
    # print(arrivals_ph)
    # print(sum(arrivals_ph))
    return times

# Generate arrivals for some hour 0-24, will fluctuate based on the current time in simulation
hourly_arrivals = generate_arrivals_per_hour(0)

print ("Amount of arrivals generated: ", len(hourly_arrivals))
print ("Times, sorted: ", hourly_arrivals)


#%%