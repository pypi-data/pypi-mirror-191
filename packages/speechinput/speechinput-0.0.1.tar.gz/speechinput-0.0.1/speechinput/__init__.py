import speech_recognition as sr
import io
import sys

recognizer = sr.Recognizer()
key: str = ""
lang = "en-US"


def sinput(prefix: str = "") -> str:
    global recognizer
    global key
    global lang
    if not prefix == "silent":
        print(prefix, end=" ")
    # silence command-line output temporarily
    text_trap = io.StringIO()
    old_out = sys.stdout
    sys.stdout = text_trap

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)
            if not key == "":
                msg = recognizer.recognize_google(audio, key=key, language=lang)
            else:
                msg = recognizer.recognize_google(audio, language=lang)
    except sr.RequestError or sr.UnknownValueError:
        recognizer = sr.Recognizer()
        return "-1"

    # unsilence command-line output
    sys.stdout = old_out
    if not prefix == "silent":
        print(msg)
    return msg


def set_lang(language: str):
    global lang
    lang = language


def set_key(api_key: str) -> None:
    global key
    key = api_key
