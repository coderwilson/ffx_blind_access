import memory.main
from memory.main import wait_frames
import xbox
import pathing
FFXC = xbox.controller_handle()
import logging
logger = logging.getLogger(__name__)
from avina_speech.tts import speak


def approach_nearest_actor():
    index, _ = closest_actor()
    logger.debug(f"Approaching actor {index}")
    if index == 99:
        speak("No characters nearby.")
    else:
        if not pathing.approach_actor_by_index(actor_index=index):
            speak("That character has nothing to say.")

def closest_actor():
    # Returns the index of the closest actor. Excludes controlled player.
    distance = 99
    index = 99
    
    for i in range(memory.main.get_actor_array_size()):
        prox = pathing.distance(i)
        #print(f"Testing actor {i}: {prox}")
        if prox == 0 or prox > 90:
            pass
        elif index == 99:
            index = i
            distance = prox
        elif prox < distance:
            index = i
            distance = prox
        else:
            pass
    #print(f"Closest actor is {index} - distance {distance}")
    return (index, distance)

def name_aeon():
    FFXC.set_neutral()
    memory.main.wait_frames(15)
    xbox.tap_b()
    memory.main.wait_frames(2)
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(15)