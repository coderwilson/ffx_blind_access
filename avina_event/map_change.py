from avina_speech.tts import say
from memory.main import get_map

def map_description():
    
    if get_map() == 376:
        say("Tidus is crossing a bridge in the sky, wide enough for vehicles.")
        say("He looks up at a digital banner of his father, a hint of disgust crosses his face.")
        say("After a moment, he continues across the bridge.")
    elif get_map() == 371:
        say("Tidus is trying to enter the arena. Many people are getting in his way.")
    elif get_map() == 370:
        say("Tidus wakes up at the front of the arena, where he entered earlier.")
        say("People are running past in a panic.")
        say("Water is falling off of the arena above him.")
        say("Tidus picks himself up.")
    
    else:
        say(f"New Map number: {get_map()}")