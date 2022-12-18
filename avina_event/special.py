import memory.main
from memory.main import wait_frames
import xbox
import pathing
FFXC = xbox.controller_handle()

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