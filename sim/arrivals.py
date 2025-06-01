import rng_models
import numpy as np

# Run arrivals 10000 times for paper.
number_of_days = 10000
daily_arrivals = []

for day in range(number_of_days):
    day_total = 0
    for hour in range(24):
        hour_window = day * 24 + hour
        day_total += len(rng_models.generate_arrivals_per_hour(hour_window))
    daily_arrivals.append(day_total)

# Convert to numpy array for easier stats
daily_arrivals = np.array(daily_arrivals)
mean = np.mean(daily_arrivals)
std = np.std(daily_arrivals)

print(f"Average daily arrivals over {number_of_days} days: {mean:.2f}")
print(f"Standard deviation: {std:.2f}")
