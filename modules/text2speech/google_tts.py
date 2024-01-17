import re
import string
from gtts import gTTS
from pathlib import Path
# local modules
from texts_for_tts import texts

output_dir = Path.cwd() / 'generated_utterances' / 'google_tts'

if output_dir.exists():
    pass
else:
    Path.mkdir(Path.cwd() / 'generated_utterances' / 'google_tts')


for text in texts:
    utterance = gTTS(text, lang='en', tld='com.au')
    utterance_name = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    utterance_name = utterance_name[:round(len(text)*(2/3))]
    utterance_name = re.sub('\s', '_', utterance_name)
    utterance_name = Path(utterance_name.rstrip('_'))
    utterance.save(output_dir / utterance_name.with_suffix('.mp3'))

print('All utterances have been successfully created!')
