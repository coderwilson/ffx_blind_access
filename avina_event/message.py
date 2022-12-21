from memory.main import get_coords
from avina_speech.tts import speak
import vars
from avina_event.special import approach_nearest_actor
from avina_event.special import set_recall
from avina_event.special import return_to_recall

import logging
logger = logging.getLogger(__name__)

def handle_message():
    msg_queue = vars.msg_handle()
    value = msg_queue.get_msg()
    logger.debug(value)
    if value == "coords":
        coords = get_coords()
        phrase = "x " + str(int(coords[0])) + ", y " + str(int(coords[1]))
        speak(phrase)
    elif value == "approach":
        approach_nearest_actor()
    elif value == "set_recall":
        set_recall()
    elif value == "return_recall":
        return_to_recall()
    else:
        speak(value)