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
        last["battle"] = memory.main.battle_active()
        write_last(last)
        logger.debug("Battle is now active")
        return "battle"
    elif not memory.main.battle_active() and last["battle"] == True:
        last["battle"] = memory.main.battle_active()
        write_last(last)
        logger.debug("Battle is no longer active")
        return "wait"
        
    # Battle Summary
    if memory.main.battle_wrap_up_active() and last["summary"] == False:
        last["summary"] = memory.main.battle_wrap_up_active()
        write_last(last)
        logger.debug("Battle summary screen is now active")
        return "summary"
    elif not memory.main.battle_wrap_up_active() and last["summary"] == True:
        last["summary"] = memory.main.battle_wrap_up_active()
        write_last(last)
        logger.debug("Battle summary screen is no longer active")
        return "wait"

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
        return "overworld"
    return "wait"
