from datetime import datetime  # class should start with a capital letter!
from pathlib import WindowsPath
from typing import Sequence, Tuple, Union, TypedDict
from pandas import DataFrame


class BloodPressureDictType(TypedDict):
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

    def blood_pressure_heart_rate(self, records_patterns_and_paths: Tuple[Sequence[WindowsPath], Sequence[int],
                                                                          Sequence[int], Sequence[int]],
                                  as_df: bool = False) -> Union[BloodPressureDictType, DataFrame]:
        """ Returns dataset as a python dict by default
        if as_df is True, than as pandas

        Parameters
        ----------
        records_patterns_and_paths
        as_dict
        as_df

        Returns
        -------

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

    def _time_stamp(self, records_paths: Sequence[WindowsPath]):
        # we need only paths; we don't need recognized audio's texts.
        # records_paths = [x[1] for x in recognized_audio_data_with_paths]
        all_time_stamps = []
        for rec_path in records_paths:
            # stat.ST_CTIME:
            # Unix - is the time of the last metadata change
            # Windows - is the creation time (see platform documentation for details).
            c_timestamp = rec_path.stat().st_ctime
            # convert time stamp to dd-mm-yyyy hh:mm:ss
            c_time = str(datetime.fromtimestamp(c_timestamp))
            # collect all stamps
            all_time_stamps.append(c_time)

        return all_time_stamps
