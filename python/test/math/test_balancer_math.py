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

import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).split('/python/')[0])
from decimal import Decimal

from python.prod.cwpt.exchg import BalancerMath

BAL_IN = Decimal('1000')
W_IN = Decimal('0.5')
BAL_OUT = Decimal('1000')
W_OUT = Decimal('0.5')
SWAP_FEE = Decimal('0.003')
AMT_IN = Decimal('10')
AMT_OUT = Decimal('10')
POOL_SUPPLY = Decimal('100')
TOTAL_WEIGHT = Decimal('1')


class TestBalancerMath(unittest.TestCase):

    def test_calc_out_given_in_positive(self):
        result = BalancerMath.calc_out_given_in(
            token_amount_in=AMT_IN,
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)

    def test_calc_out_given_in_fee_positive(self):
        result = BalancerMath.calc_out_given_in(
            token_amount_in=AMT_IN,
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.fee, 0)

    def test_calc_in_given_out_positive(self):
        result = BalancerMath.calc_in_given_out(
            token_amount_out=AMT_OUT,
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)

    def test_calc_spot_price(self):
        price = BalancerMath.calc_spot_price(
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            swap_fee=SWAP_FEE,
        )
        expected = (BAL_IN / W_IN) / (BAL_OUT / W_OUT) * (1 / (1 - SWAP_FEE))
        self.assertAlmostEqual(float(price), float(expected), places=10)

    def test_pool_out_given_single_in_positive(self):
        result = BalancerMath.calc_pool_out_given_single_in(
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            pool_supply=POOL_SUPPLY,
            total_weight=TOTAL_WEIGHT,
            token_amount_in=AMT_IN,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)

    def test_single_in_given_pool_out_positive(self):
        result = BalancerMath.calc_single_in_given_pool_out(
            token_balance_in=BAL_IN,
            token_weight_in=W_IN,
            pool_supply=POOL_SUPPLY,
            total_weight=TOTAL_WEIGHT,
            pool_amount_out=AMT_IN,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)

    def test_single_out_given_pool_in_positive(self):
        result = BalancerMath.calc_single_out_given_pool_in(
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            pool_supply=POOL_SUPPLY,
            total_weight=TOTAL_WEIGHT,
            pool_amount_in=AMT_IN,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)

    def test_pool_in_given_single_out_positive(self):
        result = BalancerMath.calc_pool_in_given_single_out(
            token_balance_out=BAL_OUT,
            token_weight_out=W_OUT,
            pool_supply=POOL_SUPPLY,
            total_weight=TOTAL_WEIGHT,
            token_amount_out=AMT_OUT,
            swap_fee=SWAP_FEE,
        )
        self.assertGreater(result.result, 0)


if __name__ == '__main__':
    unittest.main()
