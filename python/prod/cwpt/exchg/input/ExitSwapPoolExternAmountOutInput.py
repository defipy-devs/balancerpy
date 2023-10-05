# ExitSwapPoolExternAmountOutInput.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: ExitSwapPoolExternAmountOutInput class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from decimal import Decimal
from python.prod.cwpt.exchg.amount import TokenAmount


@dataclass
class ExitSwapPoolExternAmountOutInput(object):
    token_out: TokenAmount
    max_pool_in: Decimal