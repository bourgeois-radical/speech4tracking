import re
import torch
import scipy
import string
from pathlib import Path
from transformers import VitsModel, AutoTokenizer
# import local modules
from texts_for_tts import texts

output_dir = Path.cwd() / 'generated_utterances' / 'fb_mms_tts'

if output_dir.exists():
    pass
else:
    Path.mkdir(Path.cwd() / 'generated_utterances' / 'fb_mms_tts')


model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

for text in texts:
    input_utterance = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        output = model(**input_utterance).waveform

    utterance_name = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    utterance_name = utterance_name[:round(len(text)*(2/3))]
    utterance_name = re.sub('\s', '_', utterance_name)
    utterance_name = Path(utterance_name.rstrip('_'))
    utterance_path = output_dir / utterance_name.with_suffix('.wav')

    scipy.io.wavfile.write(utterance_path, rate=model.config.sampling_rate, data=output.numpy().T)


print('All utterances have been successfully created!')