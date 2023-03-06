from memory.main import get_story_progress
from avina_speech.tts import speak
import time

def story_trigger():
    progress = get_story_progress()
    if progress == 6:
        speak("You see Tidus resting in preparation for the Blitzball game.")
    if progress == 9:
        speak("Tidus and Auron find themselves back on the bridge from earlier.")
        time.sleep(3)
        speak("People continue to run in panic.")
        speak("As Tidus looks around, suddenly time seems to freeze around him.")
        time.sleep(5)
        speak("The boy with the purple hood stands before Tidus.")
        time.sleep(18)
        speak("Time returns to normal.")
    if progress == 14:
        speak("Tidus and Auron run forward along the bridge, still covered in pod monsters.")
        speak("As they come over a crest in the bridge, they see a large monster.")
        speak("It looks almost like a tree, with tentacle-like branches waving in the sky.")
        speak("Many of the little guys are also ready to fight.")
        speak("This is a good time to learn about overdrives.")
        speak("Let's use Auron's overdrive to clear all the little guys.")
        speak("When Auron's turn starts, press 'O' and I will make Auron use his overdrive.")
    else:
        pass
    return