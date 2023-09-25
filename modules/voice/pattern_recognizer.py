import re
from pathlib import WindowsPath
from typing import Sequence, Tuple

class PatternRecognizer:
    """

    """

    @staticmethod
    def blood_pressure_heart_rate(recognized_audio_data_with_paths: Sequence[Tuple[str, WindowsPath]]) -> \
            Sequence[Sequence[str]]:

        all_sys = []
        all_dia = []
        all_heart = []
        all_paths = []
        for record_with_path in recognized_audio_data_with_paths:
            # Regular expressions to extract numbers
            systolic_pattern = r'systolic (\d+)'
            diastolic_pattern = r'diastolic (\d+)'
            heart_rate_pattern = r'heart rate (\d+)'

            # Extract numbers using regular expressions
            systolic_match = re.search(systolic_pattern, record_with_path[0])
            # record_with_path[0] because we have tuples like:
            # ('systolic 117 diastolic 64 heart rate 73', './path_to_the_auido/recorded_audio_0.wav')
            # we need only 'systolic 117 diastolic 64 heart rate 73', not the path to the source audio
            diastolic_match = re.search(diastolic_pattern, record_with_path[0])
            heart_rate_match = re.search(heart_rate_pattern, record_with_path[0])

            # Store the extracted numbers in variables
            systolic = int(systolic_match.group(1)) if systolic_match else None
            diastolic = int(diastolic_match.group(1)) if diastolic_match else None
            heart_rate = int(heart_rate_match.group(1)) if heart_rate_match else None

            # keep the file's path for every recording
            all_paths.append(record_with_path[1])
            all_sys.append(systolic)
            all_dia.append(diastolic)
            all_heart.append(heart_rate)

        return all_paths, all_sys, all_dia, all_heart
