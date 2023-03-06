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
        speak("They look sad, like there are a thousand words to be said, yet held back in this moment of sorrow.")
        time.sleep(4)
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
            "A few moments later, a child with a purple hood appears in the same place, fading in and out of view."
        )
        speak("The child follows the group.")
        time.sleep(3)
        speak(
            "The same teenager from the previous scene exits his home, a boat house connected to the pier by a small bridge."
        )
        speak(
            "The crowd is waiting to meet him. It looks like he'll need to talk to a few people before proceeding."
        )
    elif get_map() == 366:
        pass
    elif get_map() == 376:
        speak("Tidus is crossing a bridge in the sky, wide enough for vehicles.")
        speak(
            "He looks up at a digital banner of his father, a hint of disgust crosses his face."
        )
        speak("After a moment, he continues across the bridge.")
    elif get_map() == 371:
        speak("Tidus is trying to enter the arena. Many people are getting in his way.")
        speak("The arena is a few paces to the south.")
    elif get_map() == 370:
        speak("Tidus wakes up at the front of the arena, where he entered earlier.")
        speak("People are running past in a panic.")
        speak("Water is falling off of the arena above him.")
        speak("Tidus picks himself up. It looks like he should run north.")
    elif get_map() == 389:
        speak("Tidus runs after Auron.")
        time.sleep(6)
        speak("Auron directs Tidus's attention to the sky.")
        speak("Tidus looks up, his mouth agape in surprise.")
        time.sleep(3)
        speak("A giant ball of water floats above, bigger than the buildings below.")
        time.sleep(11)
        speak("A monster is ejected and lands with great impact into a nearby building.")
        time.sleep(7)
        speak("Smaller creatures fly off of it. Small, pointy creatures, almost looking like pods.")
        time.sleep(3)
        speak("As the creatures hit the road in front of Tidus and Auron, some of them start to open.")
        speak("They form into bug-like creatures, ready to take down the two heroes.")
        speak("Tidus tries to keep them at bay, flailing his arms pathetically.")
        time.sleep(4)
        speak("Auron holds out a sword to Tidus. The blade is red and shaped like a hook.")
        speak("Tidus takes the sword, nearly falling over under the surprising weight of the weapon.")
        time.sleep(13)
        speak("Gathering himself, Tidus holds the sword behind himself, ready to attack.")

    else:
        speak(f"New Map number: {get_map()}")