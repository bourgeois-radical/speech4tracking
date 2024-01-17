from pathlib import Path, WindowsPath
from typing import Tuple, Optional, Sequence
from speech_recognition import Microphone, Recognizer, AudioFile, AudioData


class SpeechRecognizer:

    def __init__(self):
        pass

    def voice2text(self):
        recognizer = Recognizer()
        mic = Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        # recognizing the voice_input using google API
        recognized_text = recognizer.recognize_google(audio)

        return recognized_text


