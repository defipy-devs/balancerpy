# CWPQuote.py
# Author: Ian Moore ( utiliwire@gmail.com )
# Date: Oct 2023

from decimal import Decimal
from ..cwpt.exchg.BalancerMath import BalancerMath 
from ..constants.balancer_constants import EXIT_FEE
from ..constants.balancer_constants import MAX_OUT_RATIO

SWAP_FEE = 0.0025

class CWPQuote():
    
    def get_amount_from_shares(self, lp, tkn, amount_shares_in):
        
        assert lp.tkn_group.get_token(tkn.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'

        if(amount_shares_in > 0):
            total_weight = lp.tkn_group.get_total_denorm_weight()
            tkn_denorm_wts = lp.tkn_group.get_denorm_weights()
            
            exit_swap = BalancerMath.calc_single_out_given_pool_in(
                token_balance_out=Decimal(tkn.token_total),
                token_weight_out=Decimal(tkn_denorm_wts[tkn.token_name]),
                pool_supply=Decimal(lp.pool_shares),
                total_weight=Decimal(total_weight),
                pool_amount_in=Decimal(amount_shares_in),
                swap_fee=Decimal(SWAP_FEE))   
            
            amt_out = float(exit_swap.result)
        else:
            amt_out = 0
            
        return amt_out  
    
    def get_shares_from_amount(self, lp, tkn, amount_in):
        
        assert lp.tkn_group.get_token(tkn.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        if(amount_in > 0):
            total_weight = lp.tkn_group.get_total_denorm_weight()
            tkn_denorm_wts = lp.tkn_group.get_denorm_weights()
            
            exit_swap = BalancerMath.calc_pool_in_given_single_out(
                    token_balance_out=Decimal(tkn.token_total),
                    token_weight_out=Decimal(tkn_denorm_wts[tkn.token_name]),
                    pool_supply=Decimal(lp.pool_shares),
                    total_weight=Decimal(total_weight),
                    token_amount_out=Decimal(amount_in),
                    swap_fee=Decimal(SWAP_FEE))
            
            lp_amt = float(exit_swap.result)
        else:
            lp_amt = 0
        return lp_amt   
             
    
    