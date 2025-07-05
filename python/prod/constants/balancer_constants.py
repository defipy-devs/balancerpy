# ─────────────────────────────────────────────────────────────────────────────
# Apache 2.0 License (DeFiPy)
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# MIT License Attribution (Third-Party Code)
# ─────────────────────────────────────────────────────────────────────────────
# This file contains code adapted from TokenEngineeringCommunity (https://github.com/TokenEngineeringCommunity/BalancerPools_Model)
# Licensed under the MIT License.
# Original copyright (c) 2021 TokenEngineeringCommunity contributors.

from decimal import Decimal

ONE_WEI = Decimal('0.000000000000000001')
BONE = Decimal('1')
MIN_BOUND_TOKENS = 2
MAX_BOUND_TOKENS = 8
MIN_FEE = Decimal('0.000001')
MAX_FEE = Decimal('0.1')
EXIT_FEE = 0
MIN_WEIGHT = BONE
MAX_WEIGHT = BONE * Decimal('50')
MAX_TOTAL_WEIGHT = BONE * Decimal('50')
MIN_BALANCE = Decimal('0.000000000001')
INIT_POOL_SUPPLY = BONE * Decimal('100')
MIN_BPOW_BASE = Decimal('0.000000000000000001')
MAX_BPOW_BASE = (Decimal('2') * BONE) - ONE_WEI
BPOW_PRECISION = BONE / Decimal('10000000000')
MAX_IN_RATIO = BONE / Decimal('2')
MAX_OUT_RATIO = (BONE / Decimal('3')) + ONE_WEI
