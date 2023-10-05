# SwapExactAmountInInput.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: SwapExactAmountInInput class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from python.prod.cwpt.exchg.amount import TokenAmount

@dataclass
class SwapExactAmountInInput(object):
    token_in: TokenAmount
    min_token_out: TokenAmount