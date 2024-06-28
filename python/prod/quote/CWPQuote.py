# Copyright [2023] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from decimal import Decimal
from ..cwpt.exchg.BalancerMath import BalancerMath 
from ..constants.balancer_constants import EXIT_FEE
from ..constants.balancer_constants import MAX_OUT_RATIO

SWAP_FEE = 0.0025

class CWPQuote():
    
    """ 
        Constant weighted product liquidity pool token quotes (ie, price, reserve and liquidity)
    """        
    
    def get_amount_from_shares(self, lp, tkn, amount_shares_in):
        
        """ get_amount_from_shares

            Get amount of token reserve, given an amount of input liquidity pool shares
                
            Parameters
            -----------------
            lp : UniswapExchange
                Uniswap LP    
            tkn: ERC20
                Token asset from CWPT set     
            amount_shares_in: float
                Amount of input shares             

            Returns
            -----------------
            amt_out: float
                Amount of token reserve
        """            
        
        assert lp.vault.get_token(tkn.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'

        if(amount_shares_in > 0):
            total_weight = lp.vault.get_total_denorm_weight()
            tkn_denorm_wts = lp.vault.get_denorm_weights()
            
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
        
        """ get_shares_from_amount

            Get amount of liquidity pool shares, given an amount of input token
                
            Parameters
            -----------------
            lp : UniswapExchange
                Uniswap LP    
            tkn: ERC20
                Token asset from CWPT set  
            amount_in: float
                Amount of input token             

            Returns
            -----------------
            lp_amt: float
                Amount of liquidity pool shares
        """          
        
        assert lp.vault.get_token(tkn.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        if(amount_in > 0):
            total_weight = lp.vault.get_total_denorm_weight()
            tkn_denorm_wts = lp.vault.get_denorm_weights()
            
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
             
    
    