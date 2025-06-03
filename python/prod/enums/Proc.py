# Copyright [2025] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from dataclasses import dataclass

@dataclass(frozen=True)
class Proc:
    SWAPIN: str = "swapin"
    SWAPOUT: str = "swapout"
    ADDTKN: str = "addtkn"
    ADDSHARES: str = "addshares"
    REMOVETKN: str = "removetkn"
    REMOVESHARES: str = "removeshares"