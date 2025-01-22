# Gaze data analyser for OpenFace csv output

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("./Data_OpenFace/Test.csv")

# Get the gaze data
gaze_data = data[['gaze_angle_x', 'gaze_angle_y', 'timestamp']]

# Rolling mean to reduce noise
calibration_data = gaze_data[gaze_data["timestamp"]<10]
calibration_data = calibration_data[['gaze_angle_x', 'gaze_angle_y',]]
calibration_data = calibration_data.mean()

gaze_data = gaze_data[['gaze_angle_x', 'gaze_angle_y']]
gaze_data['gaze_angle_x'] = gaze_data['gaze_angle_x'] - np.asarray([calibration_data['gaze_angle_x'] for i in range(gaze_data['gaze_angle_x'].shape[0])])
gaze_data['gaze_angle_y'] = gaze_data['gaze_angle_y'] - np.asarray([calibration_data['gaze_angle_y'] for i in range(gaze_data['gaze_angle_y'].shape[0])])

gaze_data = gaze_data.rolling(10).mean()

# Plot the gaze data and limits
plt.plot(gaze_data)
plt.legend(['gaze_angle_x', 'gaze_angle_y'])
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [-0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
plt.show()