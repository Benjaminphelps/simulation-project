# %%
import numpy as np
import pandas as pd

# Generate arrivals for a given hour
def generate_arrivals_per_hour(hour):
    arrivals_dataset = pd.read_csv('../data/arrival_hours.csv', delimiter=';')
    arrivals_dataset['Share_of_charging_transactions'] = arrivals_dataset['Share_of_charging_transactions'].str.replace(',','.').astype(float)
    arrivals_dataset.head()

    mu = arrivals_dataset['Share_of_charging_transactions'][hour] * 750
    times = np.sort(np.random.uniform(hour,hour+1,np.random.poisson(mu))).tolist()
    return times



