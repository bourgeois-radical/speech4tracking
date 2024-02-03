# TODO: allow user to specify data stemp manually

# TODO: automatic report for doctor (in PDF or whatever)

# TODO: Try another language. Try input in German!

# TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”) add more patterns

# TODO: speech interaction only (app pronounces T2S)

# TODO: F0, shimmer and jitter and ... A person provides his or her age and it automatically adjusts these parameters
#  of the ASR system

# TODO: a person provides a few supervised inputs (speech2text and text target) so that every
#  user can fine-tune the model

# TODO: add more regular expressions patterns

# TODO: add a time frame for measurements / an accepted time gap:
#  if u take 'pure' measurements at 12, u are allowed to take affected measurements
#  in the time frame from 11 to 13, like 2 hours range is allowed. if this condition
#  is not satisfied, the app should warn that results of the t-test may be not so clear


# fixme: measurement #1: systolic 120 diastolic 60: if there is no heart rate or dia or sys, then None will be returned
#  and the .mean cannot be calculated with None
#  was the measurement recognized correctly? [Y/n] Y
#  [[120], [60], [None]]
#  check pattern_recognizer.py

#  TODO: in contrast to speech2text functionality which varies from input to input
#   in the case of text2speech we just need to generate audio version of our standard questions
#   we normally ask a user and then reuse the generated files

# TODO: ask a user whether he wants fully speech2text based interaction

# TODO: update requirements
#   install python 3.12

# TODO: unittests for each module!!!

# TODO: generate utterances for menu (speech-based interface)