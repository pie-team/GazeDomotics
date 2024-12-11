# Toggle switch mode
# Right: center salon lamp
# Left: dining room lamp

import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np
import pyautogui
from Commandes import Commande
import subprocess

image_width = 640  # Image width
image_height = 480  # Image height
relative_error = 100  # Initial relative error
screen_width = 1920  # Screen width
width = image_width
height = image_height
defined_ratios = 0  # Defined ratios for left and right boundaries: 0: none, 1: left, 2: right, 3: both
fps_for_stable_gaze = 30  # Number of iterations to consider gaze stable (if FPS=25, duration=(1/FPS)*NbIterations=(1/25)*30=1.2 seconds)
horizontal_ratio_list = []  # List to record horizontal ratio
relative_error_list = []  # List to record relative error
detected_pupils_list = []  # List to record detected pupils
closed_eye_list = []  # List to record closed eyes

new_width = image_width * 1  # New image width
new_height = image_height * 1  # New image height
horizontal_ratio = 0.0
relative_error = 0.0

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)

time.sleep(1)  # Wait

right_gaze = 0  # Initialize right gaze
left_gaze = 0  # Initialize left gaze
knx_command = Commande()  # Create KNX command object
dining_room_color = [0, 0, 0]  # Initialize black color for dining room
center_salon_color = [0, 0, 0]  # Initialize black color for center salon
dining_room_text_color = [0, 255, 255]  # Initialize yellow text color for dining room
center_salon_text_color = [0, 255, 255]  # Initialize yellow text color for center salon
dining_room_state = 0  # Initialize state return for dining room
center_salon_state = 0  # Initialize state return for center salon

num_images = 0  # Number of captured images
refresh_period = 15  # Refresh period for the interface (1/FPS). If FPS=30, refresh every 500ms

gaze = GazeTracking()  # Create gaze tracking object

############## DISPLAY ####################
screen_width, screen_height = pyautogui.size()  # Get screen dimensions
window_height = image_height  # Define window height
# ~ cv2.namedWindow("Chez Gérard", cv2.WND_PROP_FULLSCREEN)  # Create a fullscreen window
cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Set to fullscreen
cv2.resizeWindow("Chez Gérard", screen_width, window_height)  # Resize the window
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
    if num_images >= refresh_period:  # If delay reached
        # Check installation state
        # dining_room_state = 0  # int(subprocess.getoutput('knxtool read ip: 6/0/209'))  # Check dining room lamp state
        # center_salon_state = 1  # int(subprocess.getoutput('knxtool read ip: 6/0/208'))  # Check center salon lamp state
        # num_images = 0  # Reset captured images count
        # Update dining room lamp state
        if dining_room_state == 0:  # If off
            dining_room_color = [0, 0, 0]  # Black background
            dining_room_text_color = [128, 128, 128]  # Medium gray text
        else:  # Otherwise
            dining_room_color = [0, 255, 255]  # Yellow background
            dining_room_text_color = [128, 128, 128]  # Medium gray text
        # Update center salon lamp state
        if center_salon_state == 0:  # If off
            center_salon_color = [0, 0, 0]  # Black background
            center_salon_text_color = [128, 128, 128]  # Medium gray text
        else:  # Otherwise
            center_salon_color = [0, 255, 255]  # Yellow background
            center_salon_text_color = [128, 128, 128]  # Medium gray text
            # (0,0,0) black / (50,50,50) dark gray / (128,128,128) medium gray / (200,200,200) light gray / (255,255,255) white

    # Gaze processing
    if gaze.is_blinking():  # If blinking
        # Handle blinking
        pass
    elif gaze.is_left():  # If gaze is left
        right_gaze = 0  # Reset right gaze
        left_gaze += 1  # Increment left gaze count
        # ~ print("Number of iterations looking left:", left_gaze)  # Print info in terminal

        # Handle dining room lamp command in toggle switch mode
        if left_gaze >= 17:  # Maintain gaze for at least 17 iterations
            if dining_room_state == 0:  # If lamp is off
                dining_room_state = 1
                # knx_command.turn_on_dining_room()  # Turn on
            else:
                dining_room_state = 0  # Otherwise
                # knx_command.turn_off_dining_room()  # Turn off
            left_gaze = 0  # Reset left gaze count

    elif gaze.is_right():  # If gaze is right
        left_gaze = 0  # Reset left gaze
        right_gaze += 1  # Increment right gaze count
        # ~ print("Number of iterations looking right:", right_gaze)  # Print info in terminal

        # Handle center salon lamp command in toggle switch mode
        if right_gaze >= 17:  # Maintain gaze for at least 17 iterations
            if center_salon_state == 0:  # If lamp is off
                center_salon_state = 1
                # knx_command.turn_on_center_salon()  # Turn on
            else:
                center_salon_state = 0  # Otherwise
                # knx_command.turn_off_center_salon()  # Turn off
            right_gaze = 0  # Reset right gaze count

    elif gaze.is_center():  # If gaze is center
        # ~ print("Looking at center")
        right_gaze = 0  # Reset right gaze
        left_gaze = 0  # Reset left gaze

    ############## DISPLAY ####################
    resized_frame = cv2.resize(frame, (new_width, new_height))
    height, width, _ = resized_frame.shape  # Get dimensions of the resized webcam image

    # Define available space for the color bands
    available_width = screen_width - width
    band_width = int(available_width / 2)

    # Create an image with color bands on the sides
    bordered_frame = np.zeros((height, screen_width, 3), dtype=np.uint8)
    # height: height of the resized webcam image
    # width: screen width

    # Add color for the left command
    bordered_frame[:, :band_width] = dining_room_color  # Color for dining room
    # [height, width]
    # : all rows
    # :band_width: columns from the beginning (:) to band_width

    # Add the name of the room
    text = "Dining Room"
    position = (160, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    text_color = dining_room_text_color
    text_thickness = 2
    cv2.putText(bordered_frame, text, position, font, font_size, text_color, text_thickness)

    # Add color for the right command
    bordered_frame[:, -band_width:] = center_salon_color  # Color for center salon
    # [height, width]
    # : all rows
    # -band_width:: columns from the end (:) going back by band_width

    # Add the name of the room
    text = "Center Salon"
    position = (screen_width - 300, 100)  # Adjusted position to ensure visibility
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    text_color = center_salon_text_color
    text_thickness = 2
    cv2.putText(bordered_frame, text, position, font, font_size, text_color, text_thickness)

    # Add ratio text
    text = "Ratio: " + str(int(100 * gaze.horizontal_ratio()))
    text_position = (int(screen_width / 2) - 100, 50)  # Centered horizontally
    cv2.putText(bordered_frame, text, position, font, font_size, (255, 255, 255), text_thickness)  # White color for better visibility

    # Copy the video stream to the center of the image
    bordered_frame[:, band_width:band_width + width] = frame
    # [height, width]
    # : all rows
    # band_width: starting column
    # :band_width + width: ending column

    # Display the image
    cv2.imshow("Chez Gerard", bordered_frame)
    ############## DISPLAY ####################

    # Exit
    if cv2.waitKey(1) == 27:
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Free memory