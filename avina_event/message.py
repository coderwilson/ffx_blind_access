from memory.main import get_coords
from avina_speech.tts import speak
import vars
from avina_event.special import approach_nearest_actor

def handle_message():
    msg_queue = vars.msg_handle()
    value = msg_queue.get_msg()
    if value == "coords":
        coords = get_coords()
        phrase = "x " + str(int(coords[0])) + ", y " + str(int(coords[1]))
        speak(phrase)
    elif value == "approach":
        approach_nearest_actor()
    else:
        speak(value)