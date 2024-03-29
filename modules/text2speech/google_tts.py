import re
import string
from gtts import gTTS
from pathlib import Path
# local modules
from texts_for_tts import texts, texts_2

output_dir = Path.cwd() / 'generated_utterances' / 'google_tts'

if output_dir.exists():
    pass
else:
    Path.mkdir(Path.cwd() / 'generated_utterances' / 'google_tts')

# TODO: generate in mp.3 and wav in subfolders inside google_tts
for text in texts_2:
    utterance = gTTS(text, lang='en', tld='com.au')
    utterance_name = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    # TODO: add if a file's name after mult by 2/3 is longer than 20, than restrict to 20
    utterance_name = utterance_name[:round(len(text)*(2/3))]
    utterance_name = re.sub('\s', '_', utterance_name)
    utterance_name = Path(utterance_name.rstrip('_'))
    utterance.save(output_dir / utterance_name.with_suffix('.mp3'))

print('All utterances have been successfully created!')
