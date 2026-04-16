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
    return lp, eth, dai


class TestJoin(unittest.TestCase):

    def setUp(self):
        self.lp, self.eth, self.dai = setup_balancer_lp()
        Join().apply(self.lp, USER, 100)

    def test_join_sets_pool_shares(self):
        self.assertEqual(self.lp.pool_shares, 100)

    def test_join_sets_eth_reserve(self):
        self.assertEqual(self.lp.get_reserve(self.eth), 10)

    def test_join_sets_dai_reserve(self):
        self.assertEqual(self.lp.get_reserve(self.dai), 10000)

    def test_join_provider_credited(self):
        self.assertGreater(self.lp.pool_providers[USER], 0)

    def test_join_already_joined_raises(self):
        with self.assertRaises(AssertionError):
            Join().apply(self.lp, USER, 100)


if __name__ == '__main__':
    unittest.main()
