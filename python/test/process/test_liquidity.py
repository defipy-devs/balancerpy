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
from python.prod.process.liquidity import AddLiquidity, RemoveLiquidity
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


class TestLiquidity(unittest.TestCase):

    def setUp(self):
        self.lp, self.eth, self.dai = setup_balancer_lp()

    def test_add_liquidity_by_token_increases_shares(self):
        shares_before = self.lp.pool_shares
        AddLiquidity().apply(self.lp, self.eth, USER, 1)
        self.assertGreater(self.lp.pool_shares, shares_before)

    def test_add_liquidity_eth_reserve_increases(self):
        reserve_before = self.lp.get_reserve(self.eth)
        AddLiquidity().apply(self.lp, self.eth, USER, 1)
        self.assertGreater(self.lp.get_reserve(self.eth), reserve_before)

    def test_add_liquidity_returns_fee(self):
        out = AddLiquidity().apply(self.lp, self.eth, USER, 1)
        self.assertIsInstance(out, dict)
        self.assertGreater(out['tkn_in_fee'], 0)

    def test_add_liquidity_by_shares(self):
        reserve_before = self.lp.get_reserve(self.eth)
        AddLiquidity(kind=Proc.ADDSHARES).apply(self.lp, self.eth, USER, 5)
        self.assertGreater(self.lp.get_reserve(self.eth), reserve_before)

    def test_remove_liquidity_by_token(self):
        reserve_before = self.lp.get_reserve(self.eth)
        RemoveLiquidity().apply(self.lp, self.eth, USER, 1)
        self.assertLess(self.lp.get_reserve(self.eth), reserve_before)

    def test_remove_liquidity_by_shares(self):
        reserve_before = self.lp.get_reserve(self.eth)
        RemoveLiquidity(kind=Proc.REMOVESHARES).apply(self.lp, self.eth, USER, 5)
        self.assertLess(self.lp.get_reserve(self.eth), reserve_before)

    def test_exit_pool_all_assets(self):
        out = self.lp.exit_pool(50, USER)
        self.assertIsInstance(out, dict)
        self.assertIn('ETH', out)
        self.assertIn('DAI', out)
        self.assertGreater(out['ETH'], 0)
        self.assertGreater(out['DAI'], 0)


if __name__ == '__main__':
    unittest.main()
