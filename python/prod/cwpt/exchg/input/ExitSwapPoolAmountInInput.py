# ExitSwapPoolAmountInInput.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: ExitSwapPoolAmountInInput class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from decimal import Decimal

@dataclass
class ExitSwapPoolAmountInInput(object):
    pool_amount_in: Decimal