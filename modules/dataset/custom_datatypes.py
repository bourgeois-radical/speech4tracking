from typing import TypedDict, Sequence
from pathlib import WindowsPath
from datetime import datetime


class BloodPressureDictType(TypedDict):
    """Complex data type for storing time stamps of audio records, their paths, as well as
    blood pressure and heart rates these records contain"""
    time_stamp: Sequence[datetime]
    record_path: Sequence[WindowsPath]
    sys: Sequence[int]
    dia: Sequence[int]
    heart_rate: Sequence[int]
