from pathlib import Path, WindowsPath
from typing import Tuple, Optional, Sequence
from speech_recognition import Recognizer, AudioFile, AudioData


class VoiceRecordsRecognizer:
    """This class is an adapter for speech_recognition package."""

    def __init__(self):
        pass

    def speech2text(self, src_dir: str, voice_records_names: Optional[Sequence[str]] = None) -> \
            Sequence[Tuple[str, WindowsPath]]:
        """Transforms .wav audio file(-s) into plain text.

        Parameters
        ----------
        src_dir : str
            Source directory of .wav audio file(-s)

        voice_records_names : Optional[Sequence[str]]
            Optional. if this parameter is not specified,
            then all .wav files inside the provided src_dir will be uploaded and recognized.

        Returns
        -------
        recognized_audio_data_with_paths : Sequence[Tuple[str, WindowsPath]]
            Returns a list of tuple(-s), containing the text of the recognized .wav audio file
            and the path to every
            file.
        """

        # from _upload method we get voice_records_paths which is a concatenation
        # of two arguments: src_dir and voice_records_names.
        # We need these paths for time stamping in Patterns2Dataset class inside patterns2dataset.py module

        # FIXME: self._upload fails if voice_records_names is provided as a tuple and not as a list
        audio_data, voice_records_paths = self._upload(src_dir, voice_records_names)
        recognized_audio_data_with_paths = []
        for audio, record_path in zip(audio_data, voice_records_paths):
            text = Recognizer().recognize_google(audio)
            # each recognized text is provided with relative path to the source audio
            recognized_audio_data_with_paths.append((text, record_path))

        return recognized_audio_data_with_paths

    def _upload(self, src_dir: str, voice_records_names: Optional[Sequence[str]] = None) -> \
            Tuple[Sequence[AudioData], Sequence[WindowsPath]]:
        """Uploads .wav file(-s) and transforms them to speech_recognition.AudioData format,
        which is necessary for further speech recognition.

        Parameters
        ----------
        src_dir : str
            Source directory of .wav audio file(-s).

        voice_records_names : Optional[Sequence[str]]
            Optional. if this parameter is not specified,
            then all .wav files inside the provided src_dir will be uploaded and recognized.

        Returns
        -------
        audio_data : Sequence[AudioData]
            Voice records, converted into AudioData format, which is necessary for speech_recognition package.
        voice_records_paths : Sequence[WindowsPath]
            Paths to recognized .wav audio files.
        """

        # transform src path to a Path object
        src_dir = Path(src_dir)
        # TODO  (if) check whether the folder and the file exist
        # upload all files's names from the provided directory
        if voice_records_names is None:
            # find all files of .wav format in the dir
            pointer_files = src_dir.glob('*.wav')
            # collect all files' names in the dir
            voice_records_names = [x.name for x in pointer_files if x.is_file()]

        # upload all the files (or) only concrete files provided by user
        audio_data = []
        voice_records_paths = []
        for rec_idx, rec_name in enumerate(voice_records_names):
            # getting the full path to the file
            rec_path = src_dir / rec_name
            # collect all paths
            voice_records_paths.append(rec_path)

            with open(rec_path, 'rb') as record:
                # transform the record to AudioFile object
                audio_file = AudioFile(record)
                # open context manager for record() method
                with audio_file as voice:
                    # recognize audio record
                    audio = Recognizer().record(voice)
                    # collect all records record
                    audio_data.append(audio)

        return audio_data, voice_records_paths




