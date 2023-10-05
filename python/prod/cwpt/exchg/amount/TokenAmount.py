# TokenAmount.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: TokenAmount class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from decimal import Decimal

@dataclass
class TokenAmount:
    symbol: str
    amount: Decimal

    @staticmethod
    def ta_with_dict(token_dict):
        return TokenAmount(symbol=token_dict['symbol'], amount=Decimal(token_dict['amount']))