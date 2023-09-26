from datetime import datetime  # class should start with a capital letter!
from pathlib import WindowsPath
from typing import Sequence, Tuple, Union, TypedDict
from pandas import DataFrame


class BloodPressureDictType(TypedDict):
    """Complex data type for storing time stamps of audio records, their paths, as well as
    blood pressure and heart rates these records contain"""
    # TODO: should I move all custom datatypes to a separate module??
    time_stamp: Sequence[datetime]
    record_path: Sequence[WindowsPath]
    sys: Sequence[int]
    dia: Sequence[int]
    heart_rate: Sequence[int]


class Patterns2Dataset:
    """"""

    def __init__(self):
        pass

    def blood_pressure_heart_rate(self, records_patterns_and_paths: Sequence[Sequence[WindowsPath], Sequence[int],
                                                                             Sequence[int], Sequence[int]],
                                  as_df: bool = False) -> Union[BloodPressureDictType, DataFrame]:
        """Prepares a dataset in the form of python dict which in turn has BloodPressureDictType structure.

        Parameters
        ----------
        records_patterns_and_paths : Sequence[Sequence[WindowsPath], Sequence[int], Sequence[int], Sequence[int]]
            Four lists with: paths to audio files, systolic, diastolic blood pressure and heart rates of each record.
        as_df : bool
            If switched to True, then the dataset will be returned of the form of pandas.DataFrame.

        Returns
        -------
        dataset : Union[BloodPressureDictType, DataFrame]
            The dataset in the form of BloodPressureDictType, which can be transformed to pandas.DataFrame
            if as_df is True.
        """

        # len(records_patterns_and_paths[0]): [0] could have been [1], [2] or [3] as well
        # we just need the number of records available
        # for record_idx in range(len(records_patterns_and_paths[0])):
        dataset = {'time_stamp': self._time_stamp(records_patterns_and_paths[0]),  # getting time stamps
                   'record_name': records_patterns_and_paths[0],
                   'sys': records_patterns_and_paths[1],
                   'dia': records_patterns_and_paths[2],
                   'heart_rate': records_patterns_and_paths[3]}

        if as_df is True:
            dataset = DataFrame.from_dict(dataset)

        return dataset

    def _time_stamp(self, records_paths: Sequence[WindowsPath]) -> Sequence[str]:
        """Provides a time stamp for each [audio] record.
        On Unix - is the time of the last metadata change.
        On Windows - is the creation time (see platform documentation for details).

        Parameters
        ----------
        records_paths : Sequence[WindowsPath]
            Paths to each .wav audio file.

        Returns
        -------
        all_time_stamps : Sequence[str]
            Time stamps of each provided record in the following format: yyyy-mm-dd hh:mm:ss.
        """
        all_time_stamps = []
        for rec_path in records_paths:
            # stat.ST_CTIME:
            # Unix - is the time of the last metadata change
            # Windows - is the creation time (see platform documentation for details).
            c_timestamp = rec_path.stat().st_ctime
            # convert time stamp to yyyy-mm-dd hh:mm:ss
            c_time = str(datetime.fromtimestamp(c_timestamp))
            # collect all stamps
            all_time_stamps.append(c_time)

        return all_time_stamps
