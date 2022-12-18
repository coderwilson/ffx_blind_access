from pynput import keyboard
from pynput.keyboard import Key, Controller
import xbox
from memory.main import get_coords
import pathing
FFXC = xbox.controller_handle()
from avina_speech.tts import say
from avina_event.special import closest_actor
import logging
logger = logging.getLogger(__name__)

global up
global down
global left
global right

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
                index, _ = closest_actor()
                logger.debug(f"Approaching actor {index}")
                if index != 99:
                    FFXC.set_neutral()
                    reset_l_stick()
                    #say("Approaching actor") # Line is not working (soft lock)
                    pathing.approach_actor_by_index(actor_index=index)
                #else:
                    #say("Nothing to approach.") # Line is not working (soft lock)
            if key.char == 'o':
                if state == "press":
                    FFXC.set_neutral()
                    reset_l_stick()
                    coords = get_coords()
                    logger.debug(f"Reporting coordinates: {coords}")
                    speak = "x, " + str(int(coords[0])) + ", y, " + str(int(coords[1]))
                    say(speak)
                    logger.debug("Report complete.")
            if key.char == 'r' and state == "press":
                FFXC.set_neutral()
                reset_l_stick()
                say("Not yet implemented.")
            if key.char == 'e' and state == "press":
                FFXC.set_neutral()
                reset_l_stick()
                say("Not yet implemented.")
        except: #non-alpha-numeric value.
            pass


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
