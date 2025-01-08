
import cv2
import time
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ffmpeg -re -i ../test1.mp4 -map 0:v -vf format=yuv420p -f v4l2 /dev/video0
# ffmpeg -stream_loop 1 -re -i ../pie/test1.mp4 -map 0:v -vf format=yuv420p -f v4l2 /dev/video0

square_size = 300  # Side length of the square
center_x = square_size // 2
center_y = square_size // 2
max_gaze_angle = 1

def draw_gaze_square(frame, gaze_angle_x, gaze_angle_y):
    """
    Draw a square with a dot corresponding to gaze_angle_x and gaze_angle_y.
    The gaze direction is normalized to the size of the square.
    """
    # Normalize gaze angles to be within the square's dimensions
    dot_x = int(center_x + (gaze_angle_x / max_gaze_angle) * 2*(square_size))
    dot_y = int(center_y - (gaze_angle_y / max_gaze_angle) * 2*(square_size))  # Invert y-axis for screen coordinates
    
    # Draw the square (centered in the frame)
    cv2.rectangle(frame, (center_x - square_size // 2, center_y - square_size // 2),
                  (center_x + square_size // 2, center_y + square_size // 2),
                  (255, 255, 255), 2)  # White square outline
    
    # Draw the gaze direction as a red dot inside the square
    cv2.circle(frame, (dot_x, dot_y), 8, (0, 0, 255), -1)  # Red dot for gaze direction
    
    return frame

frame_path = "./data/frame.jpg"
output_path = "./output/output.csv"

# docker_command = [
#     "docker", "run", "--rm",
#     "-v", f"{frame_path}:/input/frame.jpg",  # Map the frame into the container
#     "-v", f"{output_path}:/output/output.csv",  # Map the output file from the container
#     "openface-image",  # Name of the OpenFace Docker image
#     "./FeatureExtraction",  # Command to execute inside the container
#     "-f", "/input/frame.jpg",  # Input frame path inside the container
#     "-of", "/output/output.csv"  # Output file path inside the container
# ]

W=160
H=120
cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('U','H','C','V'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.resize(frame, (640, 480))
    
    cv2.imwrite(frame_path, frame)
    docker_command = [
        "docker", "exec", "-itd", "2b",
        "/home/openface-build/build/bin/FaceLandmarkImg", "-gaze",
        "-f", "/home/openface-build/data/frame.jpg",
        "-of", "/home/openface-build/output/output.csv"
    ]
    subprocess.run(docker_command, check=True)
    # print(f"Output saved to {output_path}")
    
    data = pd.read_csv("./output/output.csv")
    thetax = data.iloc[0,8]
    thetay = data.iloc[0,9]
    
    frame = draw_gaze_square(frame, thetax, thetay)
    
    cv2.imshow('usb cam test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
