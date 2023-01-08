import memory.main
import pathing
import xbox
from jsonmerge import merge

FFXC = xbox.controller_handle()
import logging

logger = logging.getLogger(__name__)
import json
import os

import vars
from avina_speech.tts import speak

msg_queue = vars.msg_handle()


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
        # print(f"Testing actor {i}: {prox}")
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
    # print(f"Closest actor is {index} - distance {distance}")
    return (index, distance)


def name_aeon():
    FFXC.set_neutral()
    memory.main.wait_frames(15)
    xbox.tap_b()
    memory.main.wait_frames(2)
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(15)


def set_recall(first_pos:str="false"):
    f = open("avina_event\\recall.json")
    lib = json.load(f)
    map_val = str(memory.main.get_map())
    cur_pos = memory.main.get_actor_coords(actor_index=0, raw=True)
    logger.debug(f"Setting recall point: {map_val}, first position: {first_pos}")
    if map_val in lib.keys():
        if first_pos in lib[map_val].keys():
            print("=====A=====")
            lib[map_val][first_pos]["x"] = cur_pos[0]
            lib[map_val][first_pos]["y"] = cur_pos[1]
            lib[map_val][first_pos]["z"] = cur_pos[2]
        else:
            print("=====B=====")
            new_val = {map_val: { first_pos: {"x": cur_pos[0], "y": cur_pos[1], "z": cur_pos[2]}}}
            lib = merge(lib, new_val)
    else:
        print("=====C=====")
        new_val = {map_val: { first_pos: {"x": cur_pos[0], "y": cur_pos[1], "z": cur_pos[2]}}}
        lib = merge(lib, new_val)

    filepath = os.path.join("avina_event", "recall.json")
    with open(filepath, "w") as fp:
        json.dump(lib, fp, indent=4)
    msg_queue.add_msg("set")


def return_to_recall(first_pos:str="false"):
    f = open("avina_event\\recall.json")
    lib = json.load(f)
    map_val = str(memory.main.get_map())
    index = memory.main.actor_index(actor_num=1)
    if map_val not in lib.keys():
        logger.warning("Attempting to recall, but no recall point set. {map_val}")
    elif int(lib[map_val][first_pos]["x"]) == 0 and int(lib[map_val][first_pos]["y"]) == 0:
        logger.warning("Invalid recall point. Please re-set recall spot.")
    else:
        logger.debug(f"Recalling. {memory.main.get_map()}")
        ret_point = [lib[map_val][first_pos]["x"], lib[map_val][first_pos]["y"], lib[map_val][first_pos]["z"]]
        logger.debug(f"Index: {index} | {ret_point}")
        # ret_point[0] = struct.unpack("!I", struct.pack("!f", ret_point[0]))[0]
        # ret_point[1] = struct.unpack("!I", struct.pack("!f", ret_point[1]))[0]
        # ret_point[2] = struct.unpack("!I", struct.pack("!f", ret_point[2]))[0]
        logger.debug(f"Packed: {index} | {ret_point}")
        memory.main.set_actor_coords(actor_index=index, target_coords=ret_point)
        memory.main.wait_frames(2)
        logger.debug(
            f"Recall complete. {memory.main.get_actor_coords(actor_index=index)}"
        )
    msg_queue.add_msg("return")
