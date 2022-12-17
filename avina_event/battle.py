import memory.main
from avina_event.trigger import new_event

def battle_complete():
    if memory.main.battle_complete():
        return True
    if new_event() == "story":
        return True
    return False