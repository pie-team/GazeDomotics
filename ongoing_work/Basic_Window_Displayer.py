import cv2
import numpy as np


def Basic_Window_Displayer(height, width, title, text, text_color=(128,128,128), wait_time=0, mode="center", location=(0,0)):

    # Create a black image
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Define the text and its properties
    text = text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    text_color = text_color
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
    if mode == "center":
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2
    elif mode == "location":
        text_x = (location[0] - text_size[0]//2)
        text_y = (location[1] + text_size[1]//2)

    # Put the text on the image
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness)

    # Create a window and display the image
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
    cv2.imshow(title, frame)

    cv2.waitKey(wait_time)