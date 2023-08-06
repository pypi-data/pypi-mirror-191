from dataclasses import dataclass
from enum import StrEnum


class OkxInfoType(StrEnum):
    BALANCE = 'balance'
    TICKERS = 'tickers'


@dataclass
class OkxTickerInfo:
    askPrice: float
    askSize: float
    bidPrice: float
    bidSize: float
