from enum import IntEnum
from typing import TypedDict

class CandleIndex(IntEnum):
    TIME = 0
    OPEN = 1
    CLOSE = 2
    HIGH = 3
    LOW = 4


class Candle(TypedDict):
    open: float
    close: float
    high: float
    low: float
    time: int