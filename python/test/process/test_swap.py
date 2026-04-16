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
from python.prod.process.swap import Swap
from python.prod.enums import Proc

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


class TestSwap(unittest.TestCase):

    def setUp(self):
        self.lp, self.eth, self.dai = setup_balancer_lp()

    def test_swap_exact_in_eth_for_dai(self):
        out = Swap().apply(self.lp, self.eth, self.dai, USER, 1)
        self.assertIsInstance(out, dict)
        self.assertGreater(out['tkn_out_amt'], 0)

    def test_swap_exact_in_eth_reserve_increases(self):
        eth_before = self.lp.get_reserve(self.eth)
        Swap().apply(self.lp, self.eth, self.dai, USER, 1)
        self.assertGreater(self.lp.get_reserve(self.eth), eth_before)

    def test_swap_exact_in_dai_reserve_decreases(self):
        dai_before = self.lp.get_reserve(self.dai)
        Swap().apply(self.lp, self.eth, self.dai, USER, 1)
        self.assertLess(self.lp.get_reserve(self.dai), dai_before)

    def test_swap_exact_in_fee_positive(self):
        out = Swap().apply(self.lp, self.eth, self.dai, USER, 1)
        self.assertGreater(out['tkn_in_fee'], 0)

    def test_swap_exact_out_dai_for_eth(self):
        out = Swap(kind=Proc.SWAPIN).apply(self.lp, self.dai, self.eth, USER, 0.5)
        self.assertIsInstance(out, dict)
        self.assertGreater(out['tkn_in_amt'], 0)

    def test_swap_price_impact(self):
        out_small = Swap().apply(self.lp, self.eth, self.dai, USER, 0.1)
        ratio_small = out_small['tkn_out_amt'] / 0.1

        lp2, eth2, dai2 = setup_balancer_lp()
        out_large = Swap().apply(lp2, eth2, dai2, USER, 5)
        ratio_large = out_large['tkn_out_amt'] / 5

        self.assertGreater(ratio_small, ratio_large)

    def test_get_price(self):
        price = self.lp.get_price(self.eth, self.dai)
        self.assertGreater(price, 0)


if __name__ == '__main__':
    unittest.main()
