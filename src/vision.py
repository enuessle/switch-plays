import cv2

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

cap.release()