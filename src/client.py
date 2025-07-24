# send_command.py
import socket
import base64
from openai import OpenAI
import cv2
# Get Private Keys
import keys
import prompts

HOST = "192.168.1.47"  # your laptop's IP
PORT = 5001
FILENAME = "elgato_capture.png"

# Get frame from elgato
def getImage(cap, filename = FILENAME):
    if not cap.isOpened():
        print("Cannot open capture device")
        exit()

    ret, frame = cap.read()

    if ret:
        # Downscale the frame before saving
        downscaled = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
        cv2.imwrite(filename, downscaled)
    else:
        print("Failed to grab frame")
        return None

    return filename

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def getChatGPT(client, prompt, image_path):
    # Getting the Base64 string
    base64_image = encode_image(image_path)

    completion = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": f"{prompt}" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        },
                    },
                ],
            }
        ],
    )

    command = completion.choices[0].message.content
    return command


def openClient(host = HOST, port=PORT):
    # Connect to Laptop / Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {host}:{port}...")
        s.connect((host, port))

        cap = cv2.VideoCapture(0)
        client = OpenAI(api_key = keys.GPT_KEY)

        # Loop
        for i in range (1):
            print("Getting Action")
            # Get Image
            image_path = getImage(cap, FILENAME)
            if image_path is None:
                cap.release()
                return
            
            # Get GPT Response
            command = getChatGPT(client, prompts.MK_PROMPT, image_path)

            # Send to Server
            s.sendall(command.encode())
            print(command)
            print("Sent Action")

        # Close Stuff
        cap.release()


openClient()