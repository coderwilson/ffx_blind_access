from pynput import keyboard
from pynput.keyboard import Key
from players import (
    Auron,
    Bahamut,
    CurrentPlayer,
    Kimahri,
    Lulu,
    Rikku,
    Tidus,
    Valefor,
    Wakka,
    Yuna,
)
from memory.main import (
    get_current_turn,
    turn_ready,
    get_overdrive_battle
)

import xbox
from avina_speech.tts import speak


def start():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()


def stop():
    global listener
    listener.stop()


global last_state
last_state = None
global last_key
last_key = None


def update_xbox(key, state: str = "press"):
    global last_key
    global last_state
    if key == last_key and state == last_state:
        return
    else:
        last_key = key
        last_state = state
    FFXC = xbox.controller_handle()
    if key in [Key.up, Key.down, Key.left, Key.right]:
        # print(f"Movement Key: {key}")
        l_stick = [0, 0]
        if key == Key.up:
            if state == "press":
                FFXC.set_value("d_pad", 1)
            else:
                FFXC.set_value("d_pad", 0)
        if key == Key.down:
            if state == "press":
                FFXC.set_value("d_pad", 2)
            else:
                FFXC.set_value("d_pad", 0)
        if key == Key.left:
            if state == "press":
                FFXC.set_value("d_pad", 4)
            else:
                FFXC.set_value("d_pad", 0)
        if key == Key.right:
            if state == "press":
                FFXC.set_value("d_pad", 8)
            else:
                FFXC.set_value("d_pad", 0)
    else:
        print(key)
        if key == "c" or key == Key.enter:
            if state == "press":
                FFXC.set_value("btn_b", 1)
            else:
                FFXC.set_value("btn_b", 0)
        if key in ["x", "X"] or key == Key.backspace:
            if state == "press":
                FFXC.set_value("btn_a", 1)
            else:
                FFXC.set_value("btn_a", 0)
        if key in ["o", "O"]:
            if state == "press":
                actor = get_current_turn()
                if actor < 7:
                    if get_overdrive_battle(actor) == 100:
                        if actor == 0:
                            Tidus.overdrive()
                        elif actor == 2:
                            Auron.overdrive()
                        elif actor == 4:
                            Wakka.overdrive()
                        elif actor == 5:
                            speak("Lulu's overdrive not yet programmed.")
                        else:
                            speak("Current character's overdrive can be done by hand.")
                elif get_overdrive_battle(actor) == 20:
                    pass


def on_press(key):
    try:
        # print('alphanumeric key {0} pressed'.format(
        #    key.char))
        update_xbox(key)

    except AttributeError:
        # print('special key {0} pressed'.format(
        #    key))
        update_xbox(key)


def on_release(key):
    # print('{0} released'.format(
    #    key))
    update_xbox(key, state="release")
    # if key == keyboard.Key.esc:
    #    # Stop listener
    #    return False
