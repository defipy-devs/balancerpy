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

from python.prod.erc import ERC20
from python.prod.vault import BalancerVault
from python.prod.cwpt.factory import BalancerFactory
from python.prod.utils.data import BalancerExchangeData
from python.prod.process.join import Join
from python.prod.quote import CWPQuote

USER = 'user0'


def setup_balancer_lp():
    eth = ERC20("ETH", "0x01")
    eth.deposit(USER, 10)
    dai = ERC20("DAI", "0x02")
    dai.deposit(USER, 10000)

    vault = BalancerVault()
    vault.add_token(eth, 0.5)
    vault.add_token(dai, 0.5)

    factory = BalancerFactory("Balancer factory", "0x3")
    exch_data = BalancerExchangeData(vault=vault, symbol="BPT", address="0x011")
    lp = factory.deploy(exch_data)
    Join().apply(lp, USER, 100)
    return lp, eth, dai


class TestCWPQuote(unittest.TestCase):

    def setUp(self):
        self.lp, self.eth, self.dai = setup_balancer_lp()
        self.quote = CWPQuote()

    def test_get_amount_from_shares_positive(self):
        amt = self.quote.get_amount_from_shares(self.lp, self.eth, 10)
        self.assertGreater(amt, 0)

    def test_get_shares_from_amount_positive(self):
        shares = self.quote.get_shares_from_amount(self.lp, self.eth, 1)
        self.assertGreater(shares, 0)

    def test_round_trip_shares_to_amount_to_shares(self):
        initial_shares = 10
        amt = self.quote.get_amount_from_shares(self.lp, self.eth, initial_shares)
        recovered_shares = self.quote.get_shares_from_amount(self.lp, self.eth, amt)
        self.assertAlmostEqual(recovered_shares, initial_shares, delta=initial_shares * 0.001)

    def test_zero_shares_returns_zero(self):
        amt = self.quote.get_amount_from_shares(self.lp, self.eth, 0)
        self.assertEqual(amt, 0)

    def test_zero_amount_returns_zero(self):
        shares = self.quote.get_shares_from_amount(self.lp, self.eth, 0)
        self.assertEqual(shares, 0)


if __name__ == '__main__':
    unittest.main()
