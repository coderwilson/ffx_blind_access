from pynput import keyboard
from pynput.keyboard import Key, Controller
import xbox
from memory.main import get_coords
import pathing
FFXC = xbox.controller_handle()
import logging
logger = logging.getLogger(__name__)
import vars
msg_queue = vars.msg_handle()


global up
global down
global left
global right
global pass_message

def start():
    global listener
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    global up
    global down
    global left
    global right
    up = False
    down = False
    left = False
    right = False
    
    
def stop():
    FFXC.set_neutral()
    global listener
    listener.stop()

global last_state
last_state = None
global last_key
last_key = None

def reset_l_stick():
    global up
    global down
    global left
    global right
    up = False
    down = False
    left = False
    right = False

def update_xbox(key, state:str="press"):
    global last_key
    global last_state
    global up
    global down
    global left
    global right
    if key == last_key and state == last_state:
        return
    else:
        last_key = key
        last_state = state
    if key in [Key.up, Key.down, Key.left, Key.right]:
        #print(f"Movement Key: {key}")
        l_stick = [0,0]
        if up:
            l_stick[1] += 40
        elif down:
            l_stick[1] -= 40
        if right:
            l_stick[0] += 40
        elif left:
            l_stick[0] -= 40
        if l_stick != [0,0]:
            pathing.set_movement([get_coords()[0] + l_stick[0], get_coords()[1] + l_stick[1]])
        else:
            FFXC.set_neutral()
    else:
        try:
            if key.char == 'c' or key == Key.enter:
                if state == "press":
                    FFXC.set_value("btn_b", 1)
                else:
                    FFXC.set_value("btn_b", 0)
            if key.char == 'x' or key == Key.backspace:
                if state == "press":
                    FFXC.set_value("btn_a", 1)
                else:
                    FFXC.set_value("btn_a", 0)
            if key.char == 'v':
                if state == "press":
                    FFXC.set_value("btn_x", 1)
                else:
                    FFXC.set_value("btn_x", 0)
            if key.char == 'z':
                if state == "press":
                    FFXC.set_value("btn_y", 1)
                else:
                    FFXC.set_value("btn_y", 0)
            if key.char == 'a' and state == "press":
                if state == "press":
                    logger.debug("Adding message to queue")
                    msg_queue.add_msg("approach")
            if key.char == 'o':
                if state == "press":
                    msg_queue.add_msg("coords")
            if key.char == 'r' and state == "press":
                FFXC.set_neutral()
                reset_l_stick()
                msg_queue.add_msg("Not yet implemented")
            if key.char == 'e' and state == "press":
                FFXC.set_neutral()
                reset_l_stick()
                msg_queue.add_msg("Not yet implemented")
        except: #non-alpha-numeric value.
            pass
    pass_message = "none"


def on_press(key):
    print(key)
    try:
        global up
        global down
        global left
        global right
        if key == Key.up:
            up = True
        if key == Key.down:
            down = True
        if key == Key.left:
            left = True
        if key == Key.right:
            right = True
        print(f"Updating key {key}")
        update_xbox(key)
        
        
    except AttributeError:
        logger.warning("Failure in controls")
        FFXC.set_neutral()

def on_release(key):
    global up
    global down
    global left
    global right
    if key == Key.up:
        up = False
    if key == Key.down:
        down = False
    if key == Key.left:
        left = False
    if key == Key.right:
        right = False
    update_xbox(key, state="release")
    #if key == keyboard.Key.esc:
    #    # Stop listener
    #    return False
