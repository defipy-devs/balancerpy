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

from decimal import Decimal, getcontext
getcontext().prec = 50


class BalancerImpLoss:

    """ Impermanent loss for a 2-asset Balancer weighted pool.

        Mirrors the shape of uniswappy.analytics.risk.UniswapImpLoss so
        callers can compose across the DeFiPy ecosystem with a single
        mental model: construct, then .apply() with the observed price
        ratio. The closed-form used here reduces to the classic
        Uniswap V2 IL formula when the weights are 50/50.

        Math
        ----
        For a 2-asset weighted pool with normalized weights (w, 1-w)
        on (base, opp), and alpha = P'/P the ratio of current-to-entry
        price of the base token measured in opp units:

            V_LP / V_hold = alpha^w / (w·alpha + (1 - w))
            IL(alpha, w)   = V_LP / V_hold - 1

        Sanity anchors:
          alpha = 1                   → IL = 0  (no divergence, no loss)
          w = 0.5                     → IL = 2·sqrt(alpha)/(1 + alpha) - 1,
                                          matches V2's constant-product IL
          w = 1                       → IL = 0  (pool holds base only)
          w = 0                       → IL = 0  (pool holds opp only)
          0 < w < 1, alpha != 1       → IL < 0  (geometric < arithmetic mean)

        The formula is symmetric in a specific sense: IL(alpha, w) ==
        IL(1/alpha, 1-w). That is, halving the price of the base asset
        in a 80/20 base/opp pool gives the same IL as doubling the
        price of the base asset in a 20/80 base/opp pool. Tests cover
        this identity.

        API contract
        ------------
        Construct with the lp and the amount of pool shares the
        caller holds. The constructor captures the per-token share
        of reserves entitled to that position size at the current
        pool state — these serve as the "entry" amounts in the
        hold-value counterfactual, matching UniswapImpLoss's
        convention.

        calc_iloss(alpha, weight=None) is a pure function of alpha
        and the base-token weight; call it directly for what-if
        scenarios without re-reading pool state. weight defaults to
        the base token's weight at construction time.

        apply(base_tkn, opp_tkn) reads the current pool state to
        compute alpha from reserves, then returns IL via calc_iloss.
        Useful for "what's my IL right now" at call time.

        Scope limits
        ------------
        - 2-asset pools only. Balancer supports N-asset weighted
          pools, and the generalized IL formula exists, but the 2-asset
          case is the one that composes cleanly with cross-protocol
          comparison (where the other side is typically a 2-asset
          Uniswap or stableswap pool). N-asset extension is a natural
          next iteration.
        - Fee exclusion. The formula computes IL from price divergence
          alone — it does not fold in accumulated fees. Callers wanting
          net position value should compose with separate fee accounting
          (matches UniswapImpLoss's fees=False path).
    """

    def __init__(self, lp, lp_init_amt):

        """ __init__

            Parameters
            ----------
            lp : BalancerExchange
                The pool. Must have been joined (non-zero pool_shares).
                Must have exactly 2 tokens; N > 2 raises ValueError.
            lp_init_amt : float
                Pool shares held by this position. Used to derive the
                per-token entry amounts via pro-rata share of reserves.

            Raises
            ------
            ValueError
                If the pool has != 2 tokens, or if lp_init_amt is <= 0,
                or if the pool hasn't been joined yet (pool_shares == 0).
        """

        if lp_init_amt <= 0:
            raise ValueError(
                "BalancerImpLoss: lp_init_amt must be > 0; "
                "got {}".format(lp_init_amt)
            )

        if lp.pool_shares <= 0:
            raise ValueError(
                "BalancerImpLoss: pool has no shares (not joined?); "
                "got pool_shares = {}".format(lp.pool_shares)
            )

        token_names = list(lp.tkn_reserves.keys())
        if len(token_names) != 2:
            raise ValueError(
                "BalancerImpLoss: only 2-asset pools supported in v1; "
                "got {} tokens ({}). N>2 extension is a future "
                "iteration.".format(len(token_names), token_names)
            )

        self.lp = lp
        self.lp_init = lp_init_amt

        # Per-token amounts the caller is entitled to via pro-rata
        # share. Captured at construction like UniswapImpLoss's
        # x_tkn_init / y_tkn_init — these are the "hold" amounts
        # in the counterfactual.
        share = Decimal(str(lp_init_amt)) / Decimal(str(lp.pool_shares))
        self.token_names = token_names
        self.base_tkn_name = token_names[0]
        self.opp_tkn_name = token_names[1]
        self.base_tkn_init = float(
            share * Decimal(str(lp.tkn_reserves[self.base_tkn_name]))
        )
        self.opp_tkn_init = float(
            share * Decimal(str(lp.tkn_reserves[self.opp_tkn_name]))
        )

        # Base token weight at construction. Stored so calc_iloss
        # can default to "this pool's weight" when no override is
        # supplied.
        self.base_weight = float(lp.tkn_weights[self.base_tkn_name])

    def calc_iloss(self, alpha, weight = None):

        """ calc_iloss

            Pure function: closed-form IL at a given price ratio
            and base-token weight. Does not read pool state.

            Parameters
            ----------
            alpha : float
                P' / P — ratio of current-to-entry price of the base
                token in units of the opp token. Must be > 0.
            weight : float, optional
                Normalized weight of the base token, in (0, 1). When
                None, defaults to the weight captured at construction.

            Returns
            -------
            float
                IL as a fraction: 0.0 means no loss; -0.05 means 5%
                below the hold counterfactual. Always <= 0 for
                alpha > 0, 0 < w < 1.

            Raises
            ------
            ValueError
                If alpha <= 0, or weight outside (0, 1) when supplied.
        """

        if alpha <= 0:
            raise ValueError(
                "BalancerImpLoss.calc_iloss: alpha must be > 0; "
                "got {}".format(alpha)
            )

        w = self.base_weight if weight is None else weight
        if not (0 < w < 1):
            raise ValueError(
                "BalancerImpLoss.calc_iloss: weight must be in (0, 1); "
                "got {}".format(w)
            )

        # Decimal for consistency with UniswapImpLoss.
        d_alpha = Decimal(str(alpha))
        d_w = Decimal(str(w))
        d_one = Decimal("1")

        # V_LP / V_hold = alpha^w / (w·alpha + (1 - w))
        # Decimal doesn't support non-integer exponentiation directly;
        # use the ln/exp bridge: x^w = exp(w · ln(x)).
        numerator = (d_w * d_alpha.ln()).exp()
        denominator = d_w * d_alpha + (d_one - d_w)
        il = numerator / denominator - d_one
        return float(il)

    def apply(self, base_tkn = None, opp_tkn = None):

        """ apply

            Compute current IL using the pool's live state.

            Reads the current spot price of base in opp units, divides
            by the entry price implicit in the captured reserves at
            construction, and returns IL at the resulting alpha.

            Parameters
            ----------
            base_tkn : ERC20, optional
                Base token override. Defaults to the first token in
                the pool (tkn_reserves insertion order). Provide
                explicitly when the default ordering doesn't match
                the caller's mental model.
            opp_tkn : ERC20, optional
                Opp token override. Defaults to the second token.

            Returns
            -------
            float
                IL at the current pool state, fractional.
        """

        tokens = self.lp.vault.get_balances()
        if base_tkn is not None and opp_tkn is not None:
            base_nm = base_tkn.token_name
            opp_nm = opp_tkn.token_name
            # Ensure we captured these at construction; otherwise
            # the "init" amounts don't correspond.
            if base_nm != self.base_tkn_name or opp_nm != self.opp_tkn_name:
                raise ValueError(
                    "BalancerImpLoss.apply: supplied (base, opp) "
                    "tokens ({}, {}) don't match construction-time "
                    "ordering ({}, {}). Reconstruct with the desired "
                    "ordering or omit the overrides.".format(
                        base_nm, opp_nm,
                        self.base_tkn_name, self.opp_tkn_name,
                    )
                )

        # Entry price: captured reserves' ratio at construction.
        # Denominated as opp-per-base (units of opp per unit of base).
        if self.base_tkn_init == 0:
            return 0.0
        entry_price = self.opp_tkn_init / self.base_tkn_init

        # Current spot price, fee-free and weight-adjusted.
        # sP_opp_per_base = (B_opp / w_opp) / (B_base / w_base)
        #
        # We compute this directly from reserves/weights rather than
        # calling lp.get_price(), because lp.get_price() bakes in a
        # (1 - swap_fee) denominator scale factor from calc_spot_price.
        # That scaling is appropriate for "quote this trade" use cases,
        # but for IL decomposition we want the marginal (fee-free)
        # spot price — otherwise a fresh pool with alpha=1 would
        # register a residual IL from fee scaling alone.
        b_base = self.lp.tkn_reserves[self.base_tkn_name]
        b_opp = self.lp.tkn_reserves[self.opp_tkn_name]
        w_base = self.lp.tkn_weights[self.base_tkn_name]
        w_opp = self.lp.tkn_weights[self.opp_tkn_name]
        if b_base <= 0 or b_opp <= 0 or w_base <= 0 or w_opp <= 0:
            return 0.0
        current_price = (b_opp / w_opp) / (b_base / w_base)

        if entry_price <= 0 or current_price <= 0:
            return 0.0

        alpha = current_price / entry_price
        return self.calc_iloss(alpha)

    def hold_value(self, base_tkn = None, opp_tkn = None):

        """ hold_value

            Counterfactual value if the caller had held their entry
            tokens instead of LPing, denominated in opp units.

            Parameters
            ----------
            base_tkn, opp_tkn : ERC20, optional
                Override token choice, same semantics as .apply().

            Returns
            -------
            float
                Hold value in opp-token units.
        """

        if base_tkn is not None and opp_tkn is not None:
            if (base_tkn.token_name != self.base_tkn_name
                    or opp_tkn.token_name != self.opp_tkn_name):
                raise ValueError(
                    "BalancerImpLoss.hold_value: supplied tokens "
                    "don't match construction-time ordering."
                )

        # Fee-free spot price, opp-per-base, computed directly from
        # reserves and weights (see .apply() for why we bypass
        # lp.get_price here).
        b_base = self.lp.tkn_reserves[self.base_tkn_name]
        b_opp = self.lp.tkn_reserves[self.opp_tkn_name]
        w_base = self.lp.tkn_weights[self.base_tkn_name]
        w_opp = self.lp.tkn_weights[self.opp_tkn_name]
        if b_base <= 0 or b_opp <= 0 or w_base <= 0 or w_opp <= 0:
            return 0.0
        current_price = (b_opp / w_opp) / (b_base / w_base)
        return (self.base_tkn_init * current_price) + self.opp_tkn_init
