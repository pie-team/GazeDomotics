"""
This script uses OpenCV and GazeTracking to control the state of two lamps (dining room and center salon) based on the user's gaze direction. The script captures video from the webcam, analyzes the gaze direction, and toggles the state of the lamps accordingly. The script also displays the video feed with visual feedback for the user's gaze direction.
Global Variables:
- YELLOW_COLOR: RGB value for yellow color.
- GREY_COLOR: RGB value for grey color.
- BLACK_COLOR: RGB value for black color.
- WHITE_COLOR: RGB value for white color.
- GREEN_COLOR: RGB value for green color.
- IMAGE_WIDTH: Width of the captured image.
- IMAGE_HEIGHT: Height of the captured image.
- FPS_STABLE_GAZE: Number of frames to maintain gaze for a stable detection.
- OFF: Constant representing the OFF state.
- ON: Constant representing the ON state.
- REFRESH_PERIOD: Number of frames before checking the state of the lamps.
Lists:
- horizontal_ratio_list: List to record horizontal gaze ratios.
- relative_error_list: List to record relative errors.
- detected_pupils_list: List to record detected pupils.
- closed_eye_list: List to record closed eye states.
Initialization:
- Initializes the webcam with specified width and height.
- Initializes gaze tracking and KNX command objects.
- Sets initial states and colors for the lamps.
Main Loop:
- Captures an image from the webcam.
- Analyzes the gaze direction.
- Updates the state and color of the lamps based on the gaze direction.
- Displays the video feed with visual feedback for the user's gaze direction.
- Exits the loop when the ESC key (27) is pressed.
Constants:
- ESC_KEY: Constant representing the ESC key (27).
"""

import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np
import pyautogui
from Commandes import Commande
import subprocess

# Define global variables
YELLOW_COLOR = [0, 255, 255]
GREY_COLOR = [128, 128, 128]
BLACK_COLOR = [0, 0, 0]
WHITE_COLOR = [255, 255, 255]
GREEN_COLOR = (0, 255, 0)
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
FPS_STABLE_GAZE = 17  # if FPS=25, duration=(1/FPS)*NbIterations=(1/25)*17=0.5 seconds
OFF = 0 
ON = 1
REFRESH_PERIOD = 15 # Number of frames before checking the state of the lamps
ESC_KEY = 27

# Lists to record data
horizontal_ratio_list = []
relative_error_list = []
detected_pupils_list = []
closed_eye_list = []

new_width = IMAGE_WIDTH * 1  # New image width
new_height = IMAGE_HEIGHT * 1  # New image height

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

time.sleep(1)  # Wait

right_gaze_count = 0  # Initialize right gaze
left_gaze_count = 0  # Initialize left gaze
knx_command = Commande()  # Create KNX command object
dining_room_color = BLACK_COLOR
center_salon_color = BLACK_COLOR
dining_room_text_color = GREY_COLOR
center_salon_text_color = GREY_COLOR
dining_room_state = OFF  
center_salon_state = OFF  

num_images = 0  # Number of captured images

gaze = GazeTracking()  # Create gaze tracking object

############## DISPLAY ####################
screen_width, screen_height = pyautogui.size()  # Get screen dimensions
window_height = IMAGE_HEIGHT  # Define window height
# ~ cv2.namedWindow("Chez Gérard", cv2.WND_PROP_FULLSCREEN)  # Create a fullscreen window
cv2.namedWindow("Chez Gerard", cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.setWindowProperty("Chez Gerard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Set to fullscreen
cv2.resizeWindow("Chez Gerard", screen_width, window_height)  # Resize the window
############## DISPLAY ####################

while True:
    # Capture an image
    ret, frame = cap.read()
    if not ret:
        break

    # Analyze the image
    gaze.refresh(frame)

    # Place cross on pupils
    frame = gaze.annotated_frame()

    # Flip image vertically for user feedback
    frame = cv2.flip(frame, 1)

    # Periodic state check and GUI update
    num_images += 1  # Increment captured images count
    if num_images >= REFRESH_PERIOD:  # If delay reached
        # Check installation state
        # dining_room_state = OFF
        # center_salon_state = ON 
        num_images = 0  # Reset captured images count
        if dining_room_state == OFF:
            dining_room_color = BLACK_COLOR
            dining_room_text_color = GREY_COLOR
        else:
            dining_room_color = YELLOW_COLOR
            dining_room_text_color = GREY_COLOR
        if center_salon_state == OFF:
            center_salon_color = BLACK_COLOR
            center_salon_text_color = GREY_COLOR
        else:
            center_salon_color = YELLOW_COLOR
            center_salon_text_color = GREY_COLOR

    # Gaze processing
    if gaze.is_blinking():  # If blinking
        # Handle blinking
        pass
    elif gaze.is_left():
        right_gaze_count = 0  # Reset right gaze
        left_gaze_count += 1  # Increment left gaze count
        # Handle dining room lamp command in toggle switch mode
        if left_gaze_count >= FPS_STABLE_GAZE:  # Maintain gaze for at least 17 iterations
            if dining_room_state == OFF:
                dining_room_state = ON
                # knx_command.turn_on_dining_room()  # Turn on
            else:
                dining_room_state = OFF  # Otherwise
                # knx_command.turn_off_dining_room()  # Turn off
            left_gaze_count = 0  # Reset left gaze count

    elif gaze.is_right():  # If gaze is right
        left_gaze_count = 0  # Reset left gaze
        right_gaze_count += 1  # Increment right gaze count

        # Handle center salon lamp command in toggle switch mode
        if right_gaze_count >= FPS_STABLE_GAZE:  # Maintain gaze for at least 17 iterations
            if center_salon_state == OFF:  # If lamp is off
                center_salon_state = ON
                # knx_command.turn_on_center_salon()  # Turn on
            else:
                center_salon_state = OFF  # Otherwise
                # knx_command.turn_off_center_salon()  # Turn off
            right_gaze_count = 0  # Reset right gaze count

    elif gaze.is_center():  # If gaze is center
        right_gaze_count = 0  # Reset right gaze
        left_gaze_count = 0  # Reset left gaze

    #<<<<<<<<<<<<<<<<<<< DISPLAY <<<<<<<<<<<<<<<<<<<
    resized_frame = cv2.resize(frame, (new_width, new_height))
    height, width, _ = resized_frame.shape  # Get dimensions of the resized webcam image

    # Define available space for the color bands
    available_width = screen_width - width
    band_width = int(available_width / 2)

    # Create an image with color bands on the sides
    bordered_frame = np.zeros((height, screen_width, 3), dtype=np.uint8)

    # Add color for the left command
    bordered_frame[:, :band_width] = dining_room_color  # Color for dining room

    # Add the name of the room
    text = "Item suivant"
    position = (160, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    text_color = dining_room_text_color
    text_thickness = 2
    cv2.putText(bordered_frame, text, position, font, font_size, text_color, text_thickness)

    # Add color for the right command
    bordered_frame[:, -band_width:] = center_salon_color  # Color for center salon

    # Add the name of the room
    text = "Salon"
    position = (screen_width - 300, 100)  # Adjusted position to ensure visibility
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    text_color = center_salon_text_color
    text_thickness = 2
    cv2.putText(bordered_frame, text, position, font, font_size, text_color, text_thickness)

    # Add the name of the room dynamically
    rooms = ["Salon", "Bedroom", "Kitchen"]
    current_room = rooms[num_images % len(rooms)]  # Cycle through the rooms
    text = current_room
    position = (screen_width - 300, 100)  # Adjusted position to ensure visibility
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    text_color = center_salon_text_color
    text_thickness = 2
    cv2.putText(bordered_frame, text, position, font, font_size, text_color, text_thickness)

    # Add ratio text
    text = "Ratio: " + str(int(100 * gaze.horizontal_ratio()))
    text_position = (int(screen_width / 2) - 100, 50)  # Centered horizontally
    cv2.putText(bordered_frame, text, position, font, font_size, WHITE_COLOR, text_thickness)

    # Copy the video stream to the center of the image
    bordered_frame[:, band_width:band_width + width] = frame

    #<<<<<<<<<<<<  CREATION OF MARKERS FOR GAZE POSITION FEEDBACK  <<<<<<<<<<<<
    horizontal_ratio = (gaze.normalize_horizontal_ratio()) 			# record ratio(... + measured_mean - desired_mean) * std_dev_
    relative_error = gaze.coefficient_de_variation()		# record relative error
    
    marker_position_x = -5485 * horizontal_ratio + 3840	# calculate circle ordinate
    # print("ratio:", horizontal_ratio, "marker position:", marker_position_x)
    marker_diameter = relative_error * 100 				# calculate circle diameter
    thickness = 6
    cv2.circle(bordered_frame, (int(marker_position_x), int(IMAGE_HEIGHT / 2)),
                int(marker_diameter), GREEN_COLOR, thickness)
    #>>>>>>>>>>>>>>>>>>  CREATION OF MARKERS  >>>>>>>>>>>>>>>>>>

    # Display the image
    cv2.imshow("Chez Gerard", bordered_frame)
    #>>>>>>>>>>>>>>>>>> DISPLAY >>>>>>>>>>>>>>>>>>

    # Exit
    if cv2.waitKey(1) == ESC_KEY:
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Free memory