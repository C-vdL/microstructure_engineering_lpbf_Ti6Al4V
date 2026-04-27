import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# base_path = r"C:\temp\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh"
#
# results = []
# for name in os.listdir(base_path):
#     full_path = os.path.join(base_path, name)
#     if os.path.isdir(full_path):
#         parts = os.path.normpath(full_path).split(os.sep)
#         last_two = os.path.join(parts[-3], parts[-2], parts[-1])
#         results.append(last_two)
#
# # Example output
# for item in results:
#     print(f"'{item}',")


# Load CSV files
recoater_series = pd.read_csv('recoater_event_series_4-5_gh.csv', names=['time', 'x', 'y', 'z', 'state'])
laser_series = pd.read_csv('laser_event_series_4-5_gh.csv', names=['time', 'x', 'y', 'z', 'magnitude'])
timepoint_series = pd.read_csv('timepoints_4-5_gh.csv', names=['time_start', 'time_end', 'step_size'])

# Plot setup
fig, ax = plt.subplots(figsize=(12, 6))

# Plot step_size scatter from timepoints
for _, row in timepoint_series.iterrows():
    timepoint_array = np.linspace(start=row['time_start'], stop=row['time_end'], num=int((row['time_end']-row['time_start'])/row['step_size']))
    ax.scatter(timepoint_array, row['step_size']*np.ones(len(timepoint_array)))
    # time_mid = (row['time_start'] + row['time_end']) / 2
    # ax.scatter(time_mid, row['step_size'], color='blue', s=20)

# Plot shaded regions for recoater state == 1
for i in range(len(recoater_series) - 1):
    if recoater_series.loc[i, 'state'] == 1:
        t_start = recoater_series.loc[i, 'time']
        t_end = recoater_series.loc[i + 1, 'time']
        ax.axvspan(t_start, t_end, color='blue', alpha=0.3, label='Recoater Active' if i == 0 else "")

# Plot shaded regions for laser magnitude != 0
for i in range(len(laser_series) - 1):
    if laser_series.loc[i, 'magnitude'] != 0:
        t_start = laser_series.loc[i, 'time']
        t_end = laser_series.loc[i + 1, 'time']
        ax.axvspan(t_start, t_end, color='red', alpha=1, label='Laser Active' if i == 0 else "")

# Plot formatting
ax.set_xlabel('Time')
ax.set_ylabel('Step Size')
ax.set_title('Step Size with Recoater and Laser Activity')
ax.set_yscale('log')
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()
