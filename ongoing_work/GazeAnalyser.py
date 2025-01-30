# Gaze data analyser for OpenFace csv output

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

IsCalibrated = sys.argv[1]
mode = sys.argv[2]

# Load the data
data = pd.read_csv("./Data_OpenFace/Test.csv")

# Get the gaze data
gaze_data_timed = data[['gaze_angle_x', 'gaze_angle_y', "timestamp", "frame"]]
gaze_data = data[['gaze_angle_x', 'gaze_angle_y']]

# Rolling mean to reduce noise
if IsCalibrated == "True":
    calibration_data = (gaze_data_timed[gaze_data_timed['timestamp']<10])[['gaze_angle_x', 'gaze_angle_y']]
    calibration_values = calibration_data.mean()
    gaze_data_calibrated = gaze_data - calibration_values
else:
    gaze_data_calibrated = gaze_data[['gaze_angle_x', 'gaze_angle_y']]


gaze_data_calibrated.loc[:,:] = gaze_data_calibrated.rolling(10).mean()

epochs_indexes = []
times = np.array(gaze_data_timed['timestamp'].values[:])
i = 0
t = 0
for time in times:
    if float(time) >= t :
        epochs_indexes.append(i)
        t += 3
    times[i] = "{:.2f}".format(time)
    i += 1

# Plot the gaze data and limits
fig, ax = plt.subplots()
plt.plot(gaze_data_calibrated)
ax.set_xticks([i for i in range(0, len(times), 25)])
ax.set_xticklabels(times[::25], rotation=45)
plt.legend(['gaze_angle_x', 'gaze_angle_y'])
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [-0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
if mode == "LandR":
    plt.vlines(epochs_indexes,-0.2,0.2)
plt.show()