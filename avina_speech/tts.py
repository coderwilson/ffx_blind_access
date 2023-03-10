import pyttsx3

engine = pyttsx3.init()
import logging

logger = logging.getLogger(__name__)


def speak(value: str):
    message(value=value)


def message(value: str, *, gender: str = "f"):
    voices = engine.getProperty("voices")
    if gender.lower() == "f":
        engine.setProperty("voice", voices[1].id)
    else:
        engine.setProperty("voice", voices[0].id)
    logger.debug(value)
    engine.say(value)
    engine.runAndWait()
    # if engine.isBusy():
    #    engine.stop()
