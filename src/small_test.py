import nxbt
import keyboard
import time
import random

# Possible Controller Inputs
buttons = [
    'B',
    'A',
    'R',
    'ZR'
]

stick_directions = [
    (100,0),
    (-100,0),
    (0,0)
]


# Start the NXBT service
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
print("Trying to connect to Switch")

controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
nx.wait_for_connection(controller_index)


# Loop
print("Connected! Press 'q' to disconnect and quit.")

try:
    while True:
        # Disconnect and Reconnect
        if keyboard.is_pressed('q'):
            print("\n\nDisconnecting controller...")
            nx.remove_controller(controller_index)
            break
        if keyboard.is_pressed('r'):
            controller_index = nx.create_controller(nxbt.PRO_CONTROLLER,
                                                    reconnect_address=nx.get_switch_addresses())

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

        time.sleep(0.01)  # Reduce CPU usage

except KeyboardInterrupt:
    print("\n\nInterrupted. Disconnecting controller...")
    nx.remove_controller(controller_index)