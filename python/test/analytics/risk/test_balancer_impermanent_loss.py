# ─────────────────────────────────────────────────────────────────────────────
# Apache 2.0 License (DeFiPy)
# ─────────────────────────────────────────────────────────────────────────────
# Copyright 2023–2026 Ian Moore
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

import sys, os, math, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).split('/python/')[0])

from python.prod.erc import ERC20
from python.prod.vault import BalancerVault
from python.prod.cwpt.factory import BalancerFactory
from python.prod.utils.data import BalancerExchangeData
from python.prod.process.join import Join
from python.prod.process.swap import Swap
from python.prod.analytics.risk import BalancerImpLoss

USER = 'user0'


def _build_lp(base_weight = 0.5, eth_amt = 10.0, dai_amt = 10000.0,
              suffix = 'a1'):
    """Deploy a fresh Balancer ETH/DAI pool at the given base weight.

    Weights are normalized. Returns (lp, eth, dai, lp_init_amt) where
    lp_init_amt is the pool_shares USER holds after joining.
    """
    eth = ERC20("ETH", "0x01")
    eth.deposit(USER, eth_amt)
    dai = ERC20("DAI", "0x02")
    dai.deposit(USER, dai_amt)

    vault = BalancerVault()
    vault.add_token(eth, base_weight)
    vault.add_token(dai, 1.0 - base_weight)

    factory = BalancerFactory(
        "Balancer factory {}".format(suffix),
        "0x{}".format(suffix),
    )
    exch_data = BalancerExchangeData(
        vault = vault, symbol = "BPT{}".format(suffix),
        address = "0x0{}".format(suffix),
    )
    lp = factory.deploy(exch_data)
    Join().apply(lp, USER, 100)
    return lp, eth, dai, lp.pool_providers[USER]


# ═══════════════════════════════════════════════════════════════════════════
# Construction & shape
# ═══════════════════════════════════════════════════════════════════════════

class TestBalancerImpLossShape(unittest.TestCase):

    def test_constructor_captures_base_weight(self):
        lp, _, _, amt = _build_lp(base_weight = 0.8, suffix = 's1')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.base_weight, 0.8, places = 10)

    def test_constructor_captures_per_token_amounts(self):
        # USER holds 100% of pool → full reserves as init amounts.
        lp, _, _, amt = _build_lp(suffix = 's2')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.base_tkn_init, 10.0, places = 6)
        self.assertAlmostEqual(il.opp_tkn_init, 10000.0, places = 6)

    def test_token_names_captured(self):
        lp, _, _, amt = _build_lp(suffix = 's3')
        il = BalancerImpLoss(lp, amt)
        self.assertEqual(il.base_tkn_name, "ETH")
        self.assertEqual(il.opp_tkn_name, "DAI")

    def test_apply_returns_float(self):
        lp, _, _, amt = _build_lp(suffix = 's4')
        il = BalancerImpLoss(lp, amt)
        self.assertIsInstance(il.apply(), float)


# ═══════════════════════════════════════════════════════════════════════════
# calc_iloss — sanity anchors on known values
# ═══════════════════════════════════════════════════════════════════════════

class TestBalancerImpLossCalcCorrectness(unittest.TestCase):

    def test_alpha_one_gives_zero_il(self):
        lp, _, _, amt = _build_lp(suffix = 'c1')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.calc_iloss(1.0), 0.0, places = 10)

    def test_weight_50_50_matches_v2_formula(self):
        # Classic V2: IL = 2·sqrt(alpha)/(1+alpha) - 1
        lp, _, _, amt = _build_lp(base_weight = 0.5, suffix = 'c2')
        il = BalancerImpLoss(lp, amt)
        for alpha in [0.5, 0.8, 1.25, 2.0, 4.0]:
            expected = 2.0 * math.sqrt(alpha) / (1.0 + alpha) - 1.0
            self.assertAlmostEqual(
                il.calc_iloss(alpha), expected, places = 8,
                msg = "alpha = {}".format(alpha),
            )

    def test_80_20_less_il_than_50_50(self):
        # More concentrated weight on the volatile asset → less IL at
        # the same alpha (bounded-IL property of weighted pools).
        lp_50, _, _, amt_50 = _build_lp(base_weight = 0.5, suffix = 'c3')
        lp_80, _, _, amt_80 = _build_lp(base_weight = 0.8, suffix = 'c4')
        il_50 = BalancerImpLoss(lp_50, amt_50)
        il_80 = BalancerImpLoss(lp_80, amt_80)
        # At alpha = 2, both lose value, but 80/20 loses less in magnitude.
        loss_50 = il_50.calc_iloss(2.0)
        loss_80 = il_80.calc_iloss(2.0)
        self.assertGreater(loss_80, loss_50)   # less negative = smaller loss
        self.assertLess(loss_50, 0.0)          # both are losses

    def test_il_negative_for_alpha_not_one(self):
        lp, _, _, amt = _build_lp(base_weight = 0.3, suffix = 'c5')
        il = BalancerImpLoss(lp, amt)
        for alpha in [0.5, 0.75, 1.5, 3.0]:
            self.assertLess(
                il.calc_iloss(alpha), 0.0,
                msg = "alpha = {}".format(alpha),
            )

    def test_weight_override(self):
        # Construction weight can be overridden per-call.
        lp, _, _, amt = _build_lp(base_weight = 0.5, suffix = 'c6')
        il = BalancerImpLoss(lp, amt)
        # Call with the default (0.5) and with an override (0.8); they
        # should give different numbers.
        default = il.calc_iloss(2.0)
        overridden = il.calc_iloss(2.0, weight = 0.8)
        self.assertNotAlmostEqual(default, overridden, places = 4)

    def test_symmetry_identity(self):
        # IL(alpha, w) == IL(1/alpha, 1-w) — the "mirror" property of
        # weighted IL: inverting alpha and flipping weight gives the
        # same loss.
        lp, _, _, amt = _build_lp(base_weight = 0.7, suffix = 'c7')
        il = BalancerImpLoss(lp, amt)
        alpha = 1.8
        w = 0.7
        lhs = il.calc_iloss(alpha, w)
        rhs = il.calc_iloss(1.0 / alpha, 1.0 - w)
        self.assertAlmostEqual(lhs, rhs, places = 8)


# ═══════════════════════════════════════════════════════════════════════════
# apply — current pool state path
# ═══════════════════════════════════════════════════════════════════════════

class TestBalancerImpLossApply(unittest.TestCase):

    def test_fresh_pool_zero_il(self):
        # Just joined → alpha = 1 → IL = 0.
        lp, _, _, amt = _build_lp(suffix = 'a1')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.apply(), 0.0, places = 6)

    def test_swap_moves_alpha_creates_il(self):
        # Construct IL tracker BEFORE swapping. Then swap. Then .apply()
        # should see a nonzero (negative) IL because alpha has moved.
        lp, eth, dai, amt = _build_lp(suffix = 'a2')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.apply(), 0.0, places = 6)

        # Drive a price move via a swap.
        Swap().apply(lp, eth, dai, USER, 2.0)

        il_after = il.apply()
        self.assertLess(il_after, 0.0)

    def test_apply_matches_calc_iloss_on_live_alpha(self):
        # Reading .apply() should equal calc_iloss at the live alpha.
        lp, eth, dai, amt = _build_lp(suffix = 'a3')
        il = BalancerImpLoss(lp, amt)
        Swap().apply(lp, eth, dai, USER, 1.0)

        # Compute live alpha using fee-free weight-adjusted spot price,
        # matching the convention .apply() uses internally.
        b_base = lp.tkn_reserves[il.base_tkn_name]
        b_opp = lp.tkn_reserves[il.opp_tkn_name]
        w_base = lp.tkn_weights[il.base_tkn_name]
        w_opp = lp.tkn_weights[il.opp_tkn_name]
        current_price = (b_opp / w_opp) / (b_base / w_base)
        entry_price = il.opp_tkn_init / il.base_tkn_init
        alpha = current_price / entry_price

        self.assertAlmostEqual(
            il.apply(), il.calc_iloss(alpha), places = 10,
        )


# ═══════════════════════════════════════════════════════════════════════════
# hold_value sanity
# ═══════════════════════════════════════════════════════════════════════════

class TestBalancerImpLossHoldValue(unittest.TestCase):

    def test_fresh_pool_hold_equals_tvl(self):
        # At entry, hold value = opp-denominated sum of reserves.
        # 10 ETH * (10000/10) + 10000 DAI = 20000 DAI.
        lp, _, _, amt = _build_lp(suffix = 'h1')
        il = BalancerImpLoss(lp, amt)
        self.assertAlmostEqual(il.hold_value(), 20000.0, places = 4)

    def test_hold_value_scales_with_price(self):
        # After a swap that raises ETH price, hold_value (which revalues
        # the held tokens at the new price) should grow.
        lp, eth, dai, amt = _build_lp(suffix = 'h2')
        il = BalancerImpLoss(lp, amt)
        before = il.hold_value()
        # Buy ETH — removes ETH from pool, drives price up.
        Swap().apply(lp, dai, eth, USER, 1000.0)
        after = il.hold_value()
        self.assertGreater(after, before)


# ═══════════════════════════════════════════════════════════════════════════
# Validation
# ═══════════════════════════════════════════════════════════════════════════

class TestBalancerImpLossValidation(unittest.TestCase):

    def test_unjoined_pool_raises(self):
        # Pool with no shares → ValueError.
        eth = ERC20("ETH", "0x01")
        dai = ERC20("DAI", "0x02")
        vault = BalancerVault()
        vault.add_token(eth, 0.5)
        vault.add_token(dai, 0.5)
        factory = BalancerFactory("unjoined factory", "0xuj")
        exch_data = BalancerExchangeData(
            vault = vault, symbol = "BPTuj", address = "0x0uj",
        )
        lp = factory.deploy(exch_data)
        with self.assertRaises(ValueError) as ctx:
            BalancerImpLoss(lp, 100.0)
        self.assertIn("pool_shares", str(ctx.exception))

    def test_zero_lp_init_amt_raises(self):
        lp, _, _, _ = _build_lp(suffix = 'v1')
        with self.assertRaises(ValueError) as ctx:
            BalancerImpLoss(lp, 0.0)
        self.assertIn("lp_init_amt", str(ctx.exception))

    def test_negative_lp_init_amt_raises(self):
        lp, _, _, _ = _build_lp(suffix = 'v2')
        with self.assertRaises(ValueError):
            BalancerImpLoss(lp, -5.0)

    def test_calc_iloss_rejects_nonpositive_alpha(self):
        lp, _, _, amt = _build_lp(suffix = 'v3')
        il = BalancerImpLoss(lp, amt)
        with self.assertRaises(ValueError):
            il.calc_iloss(0.0)
        with self.assertRaises(ValueError):
            il.calc_iloss(-1.0)

    def test_calc_iloss_rejects_weight_out_of_range(self):
        lp, _, _, amt = _build_lp(suffix = 'v4')
        il = BalancerImpLoss(lp, amt)
        with self.assertRaises(ValueError):
            il.calc_iloss(2.0, weight = 0.0)
        with self.assertRaises(ValueError):
            il.calc_iloss(2.0, weight = 1.0)
        with self.assertRaises(ValueError):
            il.calc_iloss(2.0, weight = 1.5)


if __name__ == '__main__':
    unittest.main()
