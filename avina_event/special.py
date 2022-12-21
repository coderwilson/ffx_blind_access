import memory.main
from memory.main import wait_frames
import xbox
import pathing
FFXC = xbox.controller_handle()
import logging
logger = logging.getLogger(__name__)
from avina_speech.tts import speak
import json
import os


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

def set_recall():
    f = open("avina_event\\recall.json")
    lib = json.load(f)
    map_val = str(memory.main.get_map())
    cur_pos = memory.main.get_actor_coords(actor_index=0)
    logger.debug(f"Setting recall point: {map_val}")
    if map_val in lib.keys():
        lib[map_val]["x"] = int(cur_pos[0])
        lib[map_val]["y"] = int(cur_pos[1])
        lib[map_val]["z"] = int(cur_pos[2])
    else:
        new_val = {
            map_val: {
                "x": int(cur_pos[0]),
                "y": int(cur_pos[1]),
                "z": int(cur_pos[2])
            }
        }
        lib.update(new_val)

    filepath = os.path.join("avina_event", "recall.json")
    with open(filepath, "w") as fp:
        json.dump(lib, fp, indent=4)


def return_to_recall():
    f = open("avina_event\\recall.json")
    lib = json.load(f)
    map_val = str(memory.main.get_map())
    index = memory.main.actor_index(actor_num=1)
    if map_val not in lib.keys():
        logger.warning("Attempting to recall, but no recall point set. {map_val}")
    elif int(lib[map_val]["x"]) == 0 and int(lib[map_val]["y"]) == 0:
        logger.warning("Invalid recall point. Please re-set recall spot.")
    else:
        logger.debug(f"Recalling. {memory.main.get_map()}")
        ret_point = [int(lib[map_val]["x"]), int(lib[map_val]["y"]), int(lib[map_val]["z"])]
        logger.debug(f"Index: {index} | {ret_point}")
        memory.main.set_actor_coords(actor_index=index, target_coords=ret_point)
        memory.main.wait_frames(2)
        logger.debug(f"Recall complete. {memory.main.get_actor_coords(actor_index=index)}")
