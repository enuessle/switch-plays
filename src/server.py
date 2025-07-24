import socket
import nxbt
import time
import keyboard
import random

from validation import validateActions

HOST = "0.0.0.0"     # Listen on all interfaces
PORT = 5001          # Port to listen on (must match sender)
BUFF_SIZE = 1024

def init_controller():
    nx = nxbt.Nxbt()

    # Create a Pro Controller and wait for it to connect
    print("Trying to connect to Switch")

    controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
    nx.wait_for_connection(controller_index)

    print("Connected to Switch")

    return nx, controller_index

# Stops Current Macro, Starts new one
def newAction(nx:nxbt.Nxbt, controller_index, actions, _down=0.1, _up=0.1):
    nx.clear_all_macros()
    nx.press_buttons(controller_index, actions, down=_down, up=_up, block=False)

def userControl(nx:nxbt.Nxbt, controller_index):
    try:
        while True:
            # Disconnect and Reconnect
            if keyboard.is_pressed('q'):
                print("\n\nDisconnecting controller...")
                nx.remove_controller(controller_index)
                break

            # Controller Inputs
            if keyboard.is_pressed('a'):
                nx.press_buttons(controller_index, [nxbt.Buttons.A], up=0.0)
            if keyboard.is_pressed('s'):
                nx.press_buttons(controller_index, [nxbt.Buttons.B], up=0.0)

            if keyboard.is_pressed('up'):
                nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP], up=0.0)
            if keyboard.is_pressed('down'):
                nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN], up=0.0)
            if keyboard.is_pressed('left'):
                nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_LEFT], up=0.0)
            if keyboard.is_pressed('right'):
                nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_RIGHT], up=0.0)

            if keyboard.is_pressed('p'):
                startServer(nx, controller_index)

            time.sleep(0.01)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\n\nInterrupted. Disconnecting controller...")
        nx.remove_controller(controller_index)


def startServer(nx, controller_index, host = HOST, port=PORT):

    print("\n\nStarting Server Control")

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

                valid_actions = validateActions(actions)

                print(f"Recieved {actions} => {valid_actions}")

                if valid_actions:
                    newAction(nx,controller_index,actions,1000,0.0)



# Connect to Switch
nx, controller_index = init_controller()
userControl(nx,controller_index)