# Gaze data analyser for OpenFace csv output

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('file', type=str)



args=parser.parse_args()

class icone:
    def __init__(self):
        self.x=[0,0]
        self.y=[0,0]
    
icone_hg=icone()
icone_hd=icone()
icone_bg=icone()
icone_bd=icone()
zone_neutre=icone()

def max_gaze(gaze_data):
    max=-1000
    for x in gaze_data:
        if x>max:
            max=x
    return max
def min_gaze(gaze_data):
    min=1000
    for x in gaze_data:
        if x<min:
            min=x
    return min
# Load the data
data = pd.read_csv("./Data_OpenFace/"+args.file+".csv")

# Get the gaze data
gaze_data = data[['gaze_angle_x', 'gaze_angle_y', 'timestamp']]


# Rolling mean to reduce noise
# calibration_data = gaze_data[gaze_data["timestamp"]<10]
# calibration_data = calibration_data[['gaze_angle_x', 'gaze_angle_y',]]
# calibration_data = calibration_data.mean()

gaze_data = -gaze_data[['gaze_angle_x', 'gaze_angle_y']]
# gaze_data['gaze_angle_x'] = gaze_data['gaze_angle_x'] - np.asarray([calibration_data['gaze_angle_x'] for i in range(gaze_data['gaze_angle_x'].shape[0])])
# gaze_data['gaze_angle_y'] = gaze_data['gaze_angle_y'] - np.asarray([calibration_data['gaze_angle_y'] for i in range(gaze_data['gaze_angle_y'].shape[0])])

gaze_data = gaze_data.rolling(10).mean()

min_x=min_gaze(gaze_data['gaze_angle_x'])
max_x=max_gaze(gaze_data['gaze_angle_x'])
max_y=max_gaze(gaze_data['gaze_angle_y'])
min_y=min_gaze(gaze_data['gaze_angle_y'])
diff_x=max_x-min_x
diff_y=max_y-min_y

icone_hg.x=[min_x-0.2*diff_x, min_x+0.2*diff_x]
icone_hg.y=[max_y-0.2*diff_y, max_y+0.2*diff_y]

icone_hd.x=[max_x-0.2*diff_x, max_x+0.2*diff_x]
icone_hd.y=icone_hg.y

icone_bd.x=icone_hd.x
icone_bd.y=[min_y-0.2*diff_y, min_y+0.2*diff_y]

icone_bg.x=icone_hg.x
icone_bg.y=icone_bd.y



# Plot the gaze data and limits
plt.plot(gaze_data['gaze_angle_x'], gaze_data['gaze_angle_y'])

#plot icone_hg
plt.plot(icone_hg.x, [icone_hg.y[0], icone_hg.y[0]], c='black')
plt.plot(icone_hg.x, [icone_hg.y[1], icone_hg.y[1]], c='black')
plt.plot([icone_hg.x[0], icone_hg.x[0]], icone_hg.y, c='black')
plt.plot([icone_hg.x[1], icone_hg.x[1]], icone_hg.y, c='black')

#plot icone_hd
plt.plot(icone_hd.x, [icone_hd.y[0], icone_hd.y[0]], c='black')
plt.plot(icone_hd.x, [icone_hd.y[1], icone_hd.y[1]], c='black')
plt.plot([icone_hd.x[0], icone_hd.x[0]], icone_hd.y, c='black')
plt.plot([icone_hd.x[1], icone_hd.x[1]], icone_hd.y, c='black')

#plot icone_bg
plt.plot(icone_bg.x, [icone_bg.y[0], icone_bg.y[0]], c='black')
plt.plot(icone_bg.x, [icone_bg.y[1], icone_bg.y[1]], c='black')
plt.plot([icone_bg.x[0], icone_bg.x[0]], icone_bg.y, c='black')
plt.plot([icone_bg.x[1], icone_bg.x[1]], icone_bg.y, c='black')

#plot icone_bd
plt.plot(icone_bd.x, [icone_bd.y[0], icone_bd.y[0]], c='black')
plt.plot(icone_bd.x, [icone_bd.y[1], icone_bd.y[1]], c='black')
plt.plot([icone_bd.x[0], icone_bd.x[0]], icone_bd.y, c='black')
plt.plot([icone_bd.x[1], icone_bd.x[1]], icone_bd.y, c='black')

#

'''
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [-0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
plt.plot([i for i in range(gaze_data['gaze_angle_x'].shape[0])], [0.05 for i in range(gaze_data['gaze_angle_x'].shape[0])], 'r')
'''


plt.show()
