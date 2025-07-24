import re

valid_actions = {
    'Y',
    'X',
    'B',
    'A',
    'JCL_SR',
    'JCL_SL',
    'R',
    'ZR',
    'MINUS',
    'PLUS',
    'R_STICK_PRESS',
    'L_STICK_PRESS',
    'HOME',
    'CAPTURE',
    'DPAD_DOWN',
    'DPAD_UP',
    'DPAD_RIGHT',
    'DPAD_LEFT',
    'JCR_SR',
    'JCR_SL',
    'L',
    'ZL'
}

# Regex to match L_STICK@+xxx+yyy or R_STICK@-xxx-yyy etc.
stick_pattern = re.compile(r'^(L_STICK|R_STICK)@([+-]\d{3})([+-]\d{3})$')


def validateActions(actions):
    for action in actions:
        # Check if button input
        if action in valid_actions:
            continue
        
        #Regex Match Check for correct stick input
        match = stick_pattern.match(action)
        if not match:
            return False

        x_str = match.group(2)
        y_str = match.group(3)

        # Strip + or - and check if number is in 0–100
        try:
            x_val = int(x_str)
            y_val = int(y_str)
            if not (-100 <= x_val <= 100 and -100 <= y_val <= 100):
                return False
        except ValueError:
            return False
        
    return True

# Test

test_inputs = [
    ['A', 'B', 'X'],                     # all valid simple actions
    ['L_STICK@+050-100', 'ZR'],          # valid stick + normal action
    ['R_STICK@-000+099', 'HOME'],        # valid stick + normal action
    ['L_STICK@+101+000'],                 # invalid stick (101 out of range)
    ['L_STICK@+10+0'],                 # invalid stick (not three digit)
    ['INVALID', 'ANOTHER'],               # all invalid
    ['L_STICK@+050-100', 'INVALID'],     # mixed valid + invalid
    []                                  # empty list, edge case
]

if __name__ == "__main__":
    for i, actions in enumerate(test_inputs, 1):
        print(f"Test #{i}: {actions} => {validateActions(actions)}")