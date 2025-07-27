# send_command.py
import socket
import base64
from openai import OpenAI
import cv2
# Get Private Keys
import keys
import prompts
import time
import numpy as np
import math

HOST = "192.168.1.47"  # your laptop's IP
PORT = 5001
FILENAME = "elgato_capture.png"

commands = {
    'LEFT': 'L_STICK@-100+000',
    'RIGHT': 'L_STICK@+100+000',
    'STRAIGHT': '',          
}

# Get frame from elgato
def getImage(cap, filename = FILENAME):
    if not cap.isOpened():
        print("Cannot open capture device")
        exit()

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(filename, frame)
    else:
        print("Failed to grab frame")
        return None

    return filename

def get_roi_band(image, top_frac=0.4, bottom_frac=0.7):
    height = image.shape[0]
    return image[int(height * top_frac):int(height * bottom_frac), :]

def modifyImage(filename=FILENAME):
    # Load image
    image = cv2.imread(filename)
    if image is None:
        print("Failed to load image")
        return {"error": "Failed to load image"}

    # Step 1: Crop Region of Interest (ROI)
    roi = get_roi_band(image, 0.4, 0.55)
    cv2.imwrite("step1_roi.jpg", roi)

    # Step 2: Grayscale & blur
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite("step2_blur.jpg", blur)

    # Step 3: Edge detection
    edges = cv2.Canny(blur, 50, 150)
    cv2.imwrite("step3_edges.jpg", edges)

    # Step 4: Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=40, maxLineGap=100)
    lines_img = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)

    left_angles = []
    right_angles = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(lines_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            if angle < -20:
                left_angles.append(angle)
            elif angle > 20:
                right_angles.append(angle)

    cv2.imwrite("step4_lines.jpg", lines_img)

    # Step 5: Decision logic
    avg_left = sum(left_angles) / len(left_angles) if left_angles else 0
    avg_right = sum(right_angles) / len(right_angles) if right_angles else 0

    if len(left_angles) > len(right_angles):
        direction = "RIGHT"
    elif len(right_angles) > len(left_angles):
        direction = "LEFT"
    else:
        direction = "STRAIGHT"

    return {
        "direction": direction,
        "left_lines": len(left_angles),
        "right_lines": len(right_angles),
        "avg_left_angle": round(avg_left, 2),
        "avg_right_angle": round(avg_right, 2),
        "command": commands[direction]
    }


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



def openClient(host = HOST, port=PORT):
    # Connect to Laptop / Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {host}:{port}...")
        s.connect((host, port))

        cap = cv2.VideoCapture(0)

        # Loop
        while True:
            print("Getting Action")
            # Get Image
            image_path = getImage(cap, FILENAME)
            if image_path is None:
                cap.release()
                return
            
            data = modifyImage(image_path)
            
            # Get GPT Response
            command = "A, " + data[command]

            # Send to Server
            s.sendall(command.encode())
            print(command)
            print("Sent Action")

        # Close Stuff
        cap.release()


cap = cv2.VideoCapture(0)
openClient()