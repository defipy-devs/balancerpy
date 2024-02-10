from dataclasses import dataclass
from .ExchangeData import ExchangeData
from ...vault import BalancerVault

@dataclass
class BalancerExchangeData(ExchangeData):
    vault: BalancerVault