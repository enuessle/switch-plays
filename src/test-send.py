# send_command.py
import socket

HOST = "192.168.1.47"  # your laptop's IP
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello from desktop!")



# Try index 0, 1, 2... until it finds your Elgato device
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open capture device")
    exit()

ret, frame = cap.read()
if ret:
    cv2.imwrite("elgato_capture.png", frame)
else:
    print("Failed to grab frame")