import os
import logging
import json
import memory.main
from avina_event.story import story_trigger
logger = logging.getLogger(__name__)

def write_last(values):
    writing = dict(values)
    filepath = os.path.join("avina_event", "last_state.json")
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)

def new_event() -> str:
    f = open("avina_event\\last_state.json")
    last = json.load(f)
    # Story event check
    if memory.main.get_story_progress() != last["story_progress"]:
        last["story_progress"] = memory.main.get_story_progress()
        write_last(last)
        logger.debug(f"Story event occurring: {last['story_progress']}")
        return "story"
    
    # Battle check
    if memory.main.battle_active() and last["battle"] == "False":
        print(last["battle"])
        last["battle"] = str(memory.main.battle_active() != 0)
        write_last(last)
        logger.debug("Battle is now active")
        return "battle"
    
    # Map change
    if memory.main.get_map() != last["map"]:
        last["map"] = memory.main.get_map()
        write_last(last)
        logger.debug(f"Map change {last['map']}")
        return "map"
    
    return "overworld"