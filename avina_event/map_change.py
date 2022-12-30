import time

from avina_speech.tts import speak
from memory.main import get_map


def map_description():

    if get_map() == 132:
        speak("Opening scene. A sword, staff, and ball are stacked on a pile of dirt.")
        speak("It's late in the day, around dusk.")
        speak("In the background, you see the remains of a destroyed city.")
        speak(
            "Whisp-like creatures seem to float and flow through the sky, almost as if dancing."
        )
        speak("A party sits around a campfire, each appearing lost in thought.")
        time.sleep(13)
        speak("One of the party stands up. A teenage-looking boy.")
        time.sleep(8)
        speak(
            "He walks over to another, a teenage girl, and touches her on the shoulder."
        )
        time.sleep(20)
        speak(
            "After looking at each other for a few moments, the teenager climbs a small hill and looks out into the distance."
        )
    elif get_map() == 368:
        speak("We now fade in to a city, alive and well, built on the ocean.")
        speak("A small crowd seems to be waiting for something.")
        time.sleep(5)
        speak("A man runs up and gestures wildly for a few moments.")
        speak("The crowd runs off as a group.")
        time.sleep(5)
        speak(
            "A few moments later, a child appears in the same place, fading in and out of view."
        )
        speak("The child follows the group.")
        time.sleep(5)
        speak(
            "The same teenager from the previous scene exits his home, a boat house connected to the pier by a small bridge."
        )
        speak(
            "The crowd is waiting to meet him. It looks like he'll need to talk to a few people before proceeding."
        )
    elif get_map() == 376:
        speak("Tidus is crossing a bridge in the sky, wide enough for vehicles.")
        speak(
            "He looks up at a digital banner of his father, a hint of disgust crosses his face."
        )
        speak("After a moment, he continues across the bridge.")
    elif get_map() == 371:
        speak("Tidus is trying to enter the arena. Many people are getting in his way.")
    elif get_map() == 370:
        speak("Tidus wakes up at the front of the arena, where he entered earlier.")
        speak("People are running past in a panic.")
        speak("Water is falling off of the arena above him.")
        speak("Tidus picks himself up.")

    else:
        speak(f"New Map number: {get_map()}")
