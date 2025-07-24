import socket
from validation import validateActions

HOST = "0.0.0.0"     # Listen on all interfaces
PORT = 5001          # Port to listen on (must match sender)
BUFF_SIZE = 1024

def openServer(host = HOST, port=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(BUFF_SIZE)
                if not data:
                    break

                client_string = data.decode()
                actions = [item.strip() for item in client_string.split(",")]

                print(f"Recieved {actions} => {validateActions(actions)}")


openServer()