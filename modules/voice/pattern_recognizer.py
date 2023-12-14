import re
from pathlib import Path
from typing import Sequence, Tuple


class PatternRecognizer:
    """This class helps to find patterns of our interest in texts of recognized audio files."""

    def __init__(self):
        # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
        self.systolic_pattern = r'systolic (\d+)'
        self.diastolic_pattern = r'diastolic (\d+)'
        self.heart_rate_pattern = r'heart rate (\d+)'

    def blood_pressure_heart_rate_from_voice(self, recognized_voice_inputs: list):
        """Finds systolic and diastolic blood pressure as well as heart rate
        in recognized voice inputs.

        Parameters
        ----------
        recognized_voice_inputs

        Returns
        -------

        """

        all_sys = []
        all_dia = []
        all_heart = []

        for record in recognized_voice_inputs:
            # all recognized rates
            all_sys = self._recognize_pattern(self.systolic_pattern, record, all_sys)
            all_dia = self._recognize_pattern(self.diastolic_pattern, record, all_dia)
            all_heart = self._recognize_pattern(self.heart_rate_pattern, record, all_heart)

        return [all_sys, all_dia, all_heart]

    def blood_pressure_heart_rate_from_wav(self, recognized_audio_data_with_paths: Sequence[Tuple[str, Path]]) -> \
            Tuple[Sequence[Path], Sequence[int], Sequence[int], Sequence[int]]:
        """Recognizes systolic and diastolic blood pressure as well as heart rate
        in texts of recognized audio files.

         Parameters
         ----------
         recognized_audio_data_with_paths : Sequence[Tuple[str, WindowsPath]]
            A list of tuple(-s), containing the text of the recognized .wav audio file
            and the path to this file.

         Returns
         -------
         all_paths : Sequence[WindowsPath]
            Paths of audio files in the form of WindowsPath objects.
         all_sys : Sequence[int]
            Recognized systolic blood pressure from all the records.
         all_dia : Sequence[int]
            Recognized diastolic blood pressure from all the records.
         all_heart : Sequence[int]
            Recognized heart rates from all the records.
         """

        # # Regular expressions to extract numbers
        # systolic_pattern = r'systolic (\d+)'
        # diastolic_pattern = r'diastolic (\d+)'
        # heart_rate_pattern = r'heart rate (\d+)'

        # TODO: initialize them inside __init__?
        all_paths = []
        all_sys = []
        all_dia = []
        all_heart = []

        # gather all recognized rates
        for record_with_path in recognized_audio_data_with_paths:
            # src[0] because we have tuples like:
            # ('systolic 117 diastolic 64 heart rate 73', './path_to_the_auido/recorded_audio_0.wav')
            # we need only 'systolic 117 diastolic 64 heart rate 73', not the path to the source audio
            all_sys = self._recognize_pattern(self.systolic_pattern, record_with_path[0], all_sys)
            all_dia = self._recognize_pattern(self.diastolic_pattern, record_with_path[0], all_dia)
            all_heart = self._recognize_pattern(self.heart_rate_pattern, record_with_path[0], all_heart)
            # # Store the extracted numbers in variables
            # systolic = int(systolic_match.group(1)) if systolic_match else None
            # diastolic = int(diastolic_match.group(1)) if diastolic_match else None
            # heart_rate = int(heart_rate_match.group(1)) if heart_rate_match else No
            # # keep the file's path for every recording
            all_paths.append(record_with_path[1])

        return [all_paths, all_sys, all_dia, all_heart]

    def _recognize_pattern(self, pattern: str, src: Sequence, dest: list):
        """

        Parameters
        ----------
        pattern
        src
        dest

        Returns
        -------

        """

        match = re.search(pattern, src)
        extracted_value = int(match.group(1)) if match else None
        dest.append(extracted_value)

        return dest
