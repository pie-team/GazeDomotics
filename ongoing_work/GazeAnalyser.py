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
    calibration_data = gaze_data
    calibration_data = calibration_data[['gaze_angle_x', 'gaze_angle_y',]]
    calibration_data = calibration_data.mean()
    gaze_data['gaze_angle_x'] = gaze_data['gaze_angle_x'] - np.asarray([calibration_data['gaze_angle_x'] for i in range(gaze_data['gaze_angle_x'].shape[0])])
    gaze_data['gaze_angle_y'] = gaze_data['gaze_angle_y'] - np.asarray([calibration_data['gaze_angle_y'] for i in range(gaze_data['gaze_angle_y'].shape[0])])
else:
    gaze_data = gaze_data[['gaze_angle_x', 'gaze_angle_y']]


gaze_data = gaze_data.rolling(10).mean()

times = np.array(gaze_data_timed['timestamp'].values[:])
i = 0
for time in times:
    times[i] = "{:.2f}".format(time)
    i += 1


# Plot the gaze data and limits
fig, ax = plt.subplots()
plt.plot(gaze_data)
ax.set_xticks(gaze_data_timed['frame'].values[:])
ax.set_xticklabels(times, rotation=45)
plt.legend(['gaze_angle_x', 'gaze_angle_y'])
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [-0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
if mode == "LandR":
    plt.vlines()
plt.show()