import json
import logging
import os
from avina_event import special

import memory.main
import vars

logger = logging.getLogger(__name__)
msg_queue = vars.msg_handle()


def write_last(values):
    writing = dict(values)
    filepath = os.path.join("avina_event", "last_state.json")
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)


def new_event() -> str:
    f = open("avina_event\\last_state.json")
    last = json.load(f)

    # Special events first.
    if memory.main.name_aeon_ready():
        return "special_name_aeon"

    # Story event check
    if memory.main.get_story_progress() != last["story_progress"]:
        last["story_progress"] = memory.main.get_story_progress()
        write_last(last)
        logger.debug(f"Story event occurring: {last['story_progress']}")
        return "story"

    # Battle check
    if memory.main.battle_active() and last["battle"] == False:
        print(last["battle"])
        last["battle"] = memory.main.battle_active() != 0
        write_last(last)
        logger.debug("Battle is now active")
        return "battle"

    # Map change
    if memory.main.get_map() != last["map"]:
        last["map"] = memory.main.get_map()
        write_last(last)
        logger.debug(f"Map change {last['map']}")
        return "map"

    # Messages for speaking
    if msg_queue.is_msg():
        return "special_message"

    if memory.main.user_control():
        if last["map_last_control"] != memory.main.get_map():
            special.set_recall(first_pos="true")
            last["map_last_control"] = memory.main.get_map()
            write_last(last)
        return "overworld"
    return "wait"
