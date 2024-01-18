import re
import string
from gtts import gTTS
from pathlib import Path
# local modules

# TODO: rename the module to 'tts_current_voice_input'


def save_current_voice_input_as_mp3(input_measurement):
    output_dir = Path.cwd() / 'generated_utterances'

    if output_dir.exists():
        pass
    else:
        Path.mkdir(Path.cwd() / 'generated_utterances')

    # TODO: generate in mp.3 and wav in subfolders inside google_tts
    utterance = gTTS(input_measurement, lang='en', tld='com.au')
    # utterance_name = input_measurement.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    # TODO: add if a file's name after mult by 2/3 is longer than 20, than restrict to 20
    utterance.save('modules/text2speech/generated_utterances/current_measurement.mp3')

    return 'successfully generated and saved'

# save_current_voice_input_as_mp3('systolic 120 diastolic 60 heart rate 65')