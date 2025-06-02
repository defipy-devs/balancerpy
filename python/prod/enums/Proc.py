from dataclasses import dataclass

@dataclass(frozen=True)
class Proc:
    SWAPIN: str = "swapin"
    SWAPOUT: str = "swapout"
    ADDTKN: str = "addtkn"
    ADDSHARES: str = "addshares"
    REMOVETKN: str = "removetkn"
    REMOVESHARES: str = "removeshares"