# SwapExactAmountOutOutput.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: SwapExactAmountOutOutput class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from python.prod.cwpt.exchg.amount import TokenAmount

@dataclass
class SwapExactAmountOutOutput(object):
    token_in: TokenAmount