# BalancerMathResult.py
# Author: Ian Moore ( utiliwire@gmail.com )
# Original: BalancerMathResult class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from attr import dataclass
from decimal import Decimal

@dataclass
class BalancerMathResult:
    # The relevant result of the operation
    result: Decimal
    # Amount of tokens the pool keeps in the token going into the pool (for join and joinswaps) or out the pool (exits)
    fee: Decimal