# Copyright [2023] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

# Original: BalancerMathResult class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model

from attr import dataclass
from decimal import Decimal

@dataclass
class BalancerMathResult:
    # The relevant result of the operation
    result: Decimal
    # Amount of tokens the pool keeps in the token going into the pool (for join and joinswaps) or out the pool (exits)
    fee: Decimal