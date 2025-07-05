# Copyright 2023–2025 Ian Moore
# Email: defipy.devs@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

# This file contains code adapted from web3-ethereum-defi (https://github.com/TokenEngineeringCommunity/BalancerPools_Model)
# Licensed under the MIT License.
# Original copyright (c) 2021 TokenEngineeringCommunity contributors.

from attr import dataclass
from decimal import Decimal

@dataclass
class BalancerMathResult:
    # The relevant result of the operation
    result: Decimal
    # Amount of tokens the pool keeps in the token going into the pool (for join and joinswaps) or out the pool (exits)
    fee: Decimal