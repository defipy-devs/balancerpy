# JoinSwapPoolAmountOutInput.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: JoinSwapPoolAmountOutInput class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from decimal import Decimal
from python.prod.cwpt.exchg.amount import TokenAmount

@dataclass
class JoinSwapPoolAmountOutInput(object):
    pool_amount_out: Decimal
    max_token_in: TokenAmount