# BalancerExchange.py
# Author: Ian Moore ( utiliwire@gmail.com )
# Date: Oct 2023

from decimal import Decimal
from ...erc import ERC20
from ...vault import BalancerVault
from ..factory import BalancerFactory
from .BalancerMath import BalancerMath 
from .balancer_constants import EXIT_FEE
from .balancer_constants import MAX_OUT_RATIO
import math

SWAP_FEE = 0.0025
MINIMUM_SHARES = 1e-15

class BalancerExchange():
    
    """ 
        How Balancer calls liquidity pools and uses the constant weighted product automated market maker

        Parameters
        ----------
        self.factory : Factory
            Token name 
        self.tkn_group : BalancerERC20Group
            ERC20 token group 
        self.name : str
            Exchange name  
        self.symbol : str
            Exchange symbol
        self.pool_shares : float
            Total shares in exchange             
        self.tkn_reserves : dictionary
            Token reserves  
        self.tkn_weights : dictionary
            Token weights   
        self.collected_fees : dictionary
            Collected token fees            
        self.pool_providers : dictionary
            Pool providers shares 
        self.last_pool_deposit : float
            Last pool deposit    
        self.joined : boolean
            Boolean indicator of whether pool has been initialized               

        References
        ----------   
        - https://medium.com/balancer-simulations/introducing-balancer-simulations-c0e2807709b8
        - https://token-engineering-balancer.gitbook.io/balancer-simulations/additional-code-and-instructions/balancer-the-python-edition/pool_state_updates.py
    """     
    
    def __init__(self, creator: BalancerFactory, tkn_group : BalancerVault, symbol: str, addr : str) -> None: 
        self.factory = creator
        self.tkn_group = tkn_group
        self.name = tkn_group.get_name()
        self.symbol = symbol 
        self.pool_shares = 0
        self.addr = addr   
        self.tkn_reserves = {}
        self.tkn_weights = {}
        self.tkn_fees = {}
        self.collected_fees = {}
        self.pool_providers = {} 
        self.last_pool_deposit = 0
        self.joined = False 
        
    def info(self):
        if(self.pool_shares == 0):
            reserve_str = " | ".join([f'{tkn_nm} = {0}' for tkn_nm in self.tkn_reserves]) 
            print(f"Balancer Exchange: {self.name} ({self.symbol})")
            print(f"Coins: {self.tkn_group.get_coins_str()}")
            print(f"Reserves: {reserve_str}")
            print(f"Pool Shares: {self.pool_shares} \n")             
        else:
            reserve_str = " | ".join([f'{tkn_nm} = {self.tkn_reserves[tkn_nm]}' for tkn_nm in self.tkn_reserves]) 
            weights_str = " | ".join([f'{tkn_nm} = {self.tkn_weights[tkn_nm]}' for tkn_nm in self.tkn_weights]) 
            print(f"Balancer Exchange: {self.name} ({self.symbol})")
            print(f"Coins: {self.tkn_group.get_coins_str()}")
            print(f"Reserves: {reserve_str}")
            print(f"Weights: {weights_str}")
            print(f"Pool Shares: {self.pool_shares} \n") 

            
    def join_pool(self, tkn_group : BalancerVault, amt_shares_in: float, to: str):
        
        """ join_pool

            Initialize a Balancer pool, and add liquidity for all asset deposit
                
            Parameters
            -------
            tkn_group : BalancerERC20Group
                Group of ERC20 objects     
            amt_shares_in : float
                Amount of pool shares in      
            to : str
                User name/address                 
        """          
        
        if(not self.joined):
            self.tkn_group = tkn_group
            self.tkn_reserves = tkn_group.get_balances().copy()
            self.tkn_weights = tkn_group.get_norm_weights().copy()
            self._mint(to, amt_shares_in)
            self.joined = True
        else:
            assert not self.joined, 'Balancer V1: POOL ALREADY JOINED' 
    
    def join_swap_extern_amount_in(self, amt_tkn_in, tkn_in, to): 
        
        """ join_swap_extern_amount_in

            Add liquidity via depositing token amount for single asset deposit
                
            Parameters
            -------
            amt_tkn_in : float
                Amount of token coming in     
            tkn_in : ERC20
                Input token     
            to : str
                User name/address                 
        """           
        
        assert self.tkn_group.get_token(tkn_in.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        total_weight = self.tkn_group.get_total_denorm_weight()
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        join_swap = BalancerMath.calc_pool_out_given_single_in(
            token_balance_in=Decimal(tkn_in.token_total),
            token_weight_in=Decimal(tkn_denorm_wts[tkn_in.token_name]),
            pool_supply=Decimal(self.pool_shares),
            total_weight=Decimal(total_weight),
            token_amount_in=Decimal(amt_tkn_in),
            swap_fee=Decimal(SWAP_FEE)
            )
        
        ## *** need to error check for pool_amount_out_expected ***
        
        self.tkn_group.get_token(tkn_in.token_name).deposit(to, amt_tkn_in)        
        self.mint(float(join_swap.result), amt_tkn_in, tkn_in, to)
        self._tally_fees(tkn_in, float(join_swap.fee))
        
        return {'shares_in_amt': float(join_swap.result), 'tkn_in_nm': tkn_in.token_name, 'tkn_in_fee':float(join_swap.fee)}
        
    def join_swap_pool_amount_out(self, amt_shares_in, tkn_in, to):  
        
        """ join_swap_pool_amount_out

            Add liquidity via depositing shares amount for single asset deposit
                
            Parameters
            -------
            amt_shares_in : float
                Amount of pool shares coming in     
            tkn_in : ERC20
                Input token     
            to : str
                User name/address                 
        """            
        
        assert self.tkn_group.get_token(tkn_in.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        total_weight = self.tkn_group.get_total_denorm_weight()
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        join_swap = BalancerMath.calc_single_in_given_pool_out(
            token_balance_in=Decimal(tkn_in.token_total),
            token_weight_in=Decimal(Decimal(tkn_denorm_wts[tkn_in.token_name])),
            pool_supply=Decimal(self.pool_shares),
            total_weight=Decimal(total_weight),
            pool_amount_out=Decimal(amt_shares_in),
            swap_fee=Decimal(SWAP_FEE)
            )
        
        ## *** need to error check for pool_amount_out_expected ***
        tkn_amt_in = float(join_swap.result)
        tkn_fee_in = float(join_swap.fee)
        
        self.tkn_group.get_token(tkn_in.token_name).deposit(to, tkn_amt_in)        
        self.mint(amt_shares_in, tkn_amt_in, tkn_in, to)
        self._tally_fees(tkn_in, tkn_fee_in)
        
        return {'tkn_in_amt': tkn_amt_in, 'tkn_in_nm': tkn_in.token_name, 'tkn_in_fee':tkn_fee_in}   
   
    
    def exit_swap_extern_amount_out(self, amt_tkn_out, tkn_out, to):  
          
        """ exit_swap_extern_amount_out

            Remove liquidity via withdrawing shares amount for a single asset 
                
            Parameters
            -------
            amt_tkn_out : float
                Amount of token requested for withdrawal    
            tkn_out : ERC20
                Output token     
            to : str
                User name/address                 
        """          
        
        assert self.tkn_group.get_token(tkn_out.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        assert amt_tkn_out < self.tkn_reserves[tkn_out.token_name]*float(MAX_OUT_RATIO), 'Balancer: MAX OUT RATIO'
        
        total_weight = self.tkn_group.get_total_denorm_weight()
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        exit_swap = BalancerMath.calc_pool_in_given_single_out(
                token_balance_out=Decimal(tkn_out.token_total),
                token_weight_out=Decimal(tkn_denorm_wts[tkn_out.token_name]),
                pool_supply=Decimal(self.pool_shares),
                total_weight=Decimal(total_weight),
                token_amount_out=Decimal(amt_tkn_out),
                swap_fee=Decimal(SWAP_FEE)
            )
        
        assert float(exit_swap.result) != 0, 'Balancer V1: MATH EXIT ERROR'
        
        ## *** need to error check enough supply to perform removal ***
        
        self.burn(float(exit_swap.result), amt_tkn_out, tkn_out, to)
        self._tally_fees(tkn_out, float(exit_swap.fee)) 
        
        return {'shares_out_amt': float(exit_swap.result), 'tkn_out_nm': tkn_out.token_name, 'tkn_out_fee':float(exit_swap.fee)} 
    
    def exit_swap_pool_amount_in(self, amt_shares_out, tkn_out, to):   
        
        """ exit_swap_pool_amount_in

            Remove liquidity via withdrawing shares amount for a single asset 
                
            Parameters
            -------
            amt_shares_out : float
                Amount of pool shares requested for withdrawal    
            tkn_out : ERC20
                Output token     
            to : str
                User name/address                 
        """          
        
        assert self.tkn_group.get_token(tkn_out.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        assert amt_shares_out < self.pool_shares*float(MAX_OUT_RATIO), 'Balancer: MAX OUT RATIO'
        
        total_weight = self.tkn_group.get_total_denorm_weight()
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        exit_swap = BalancerMath.calc_single_out_given_pool_in(
                token_balance_out=Decimal(tkn_out.token_total),
                token_weight_out=Decimal(tkn_denorm_wts[tkn_out.token_name]),
                pool_supply=Decimal(self.pool_shares),
                total_weight=Decimal(total_weight),
                pool_amount_in=Decimal(amt_shares_out),
                swap_fee=Decimal(SWAP_FEE)
            )        
        
        assert float(exit_swap.result) != 0, 'Balancer V1: MATH EXIT ERROR'
        
        ## *** need to error check enough supply to perform removal ***
        
        self.burn(amt_shares_out, float(exit_swap.result), tkn_out, to)
        self._tally_fees(tkn_out, float(exit_swap.fee)) 
        
        return {'tkn_out_amt': float(exit_swap.result), 'tkn_out_nm': tkn_out.token_name, 'tkn_out_fee':float(exit_swap.fee)}     
        
    def burn(self, shares, amt_tkn_out, tkn_out, _from):
        
        """ burn

            Burn liquidity from token based on number of pool shares and amount of token
                
            Parameters
            -------
            amt_tkn_out : float
                Amount of token requested for burn    
            tkn_out : ERC20
                Output token     
            _from : str
                User name/address                 
        """          
        
        assert self.tkn_group.get_token(tkn_out.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        self._burn(_from, shares)
        self.tkn_group.get_token(tkn_out.token_name).transfer(_from, amt_tkn_out)
        new_balance = self.tkn_group.get_token(tkn_out.token_name).token_total
        self._update(new_balance, tkn_out.token_name) 
        
    def _burn(self, _from, shares_out):
        
        """ burn

            Burn liquidity from token based on number of pool shares
                
            Parameters
            -------
            shares_out : float
                Amount of pool shares requested for burn        
            _from : str
                User name/address                 
        """         
        
        exit_fee = shares_out * EXIT_FEE
        available_shares = self.pool_providers.get(_from)
        self.pool_providers[_from] = available_shares - shares_out - exit_fee
        self.pool_shares -= shares_out - exit_fee       
    
    # remove liquidity: all asset withdrawal
    def exit_pool(self, amt_shares_out, _from):  
        
        """ exit_pool

            Remove liquidity via withdrawing shares amount for all assets within pool 
                
            Parameters
            -------
            amt_shares_out : float
                Amount of pool shares requested for exit        
            _from : str
                User name/address                 
        """          
        
        assert amt_shares_out <= self.pool_shares, 'Balancer V1: INSUFFICIENT AMOUNT SHARES IN POOL' 
        assert amt_shares_out <= self.pool_providers[_from], 'Balancer V1: INSUFFICIENT AMOUNT IN PROVIDER ACCOUNT' 
        
        ratio_out = amt_shares_out / self.pool_shares 
        self._burn(_from, amt_shares_out)
        
        tkn_amts_out = {}
        for tkn_nm in self.tkn_reserves:
            amt_tkn_out = ratio_out * self.tkn_reserves[tkn_nm]            
            assert amt_tkn_out != 0, 'Balancer: MATH EXIT ERROR'  
            self.tkn_group.get_token(tkn_nm).transfer(_from, amt_tkn_out)
            new_balance = self.tkn_group.get_token(tkn_nm).token_total
            self._update(new_balance, tkn_nm)  
            tkn_amts_out[tkn_nm] = amt_tkn_out
            
        self.joined = False if self.pool_shares == 0 else self.joined   
            
        return tkn_amts_out   
      
    def swap_exact_amount_in(self, amt_tkn_in, tkn_in, tkn_out, to):
        
        """ swap_exact_amount_in

            Swap output token given input token 
                
            Parameters
            -------
            amt_tkn_in : float
                Amount of input token requested for swaping   
            tkn_in : ERC20
                Input token           
            tkn_out : ERC20
                Output token                    
            to : str
                User name/address                 
        """          
        
        assert self.tkn_group.get_token(tkn_in.token_name) and self.tkn_group.get_token(tkn_out.token_name), "Balancer: TOKEN NOT PART OF GROUP"
        
        amount_out_expected = self.get_amount_out(amt_tkn_in, tkn_in, tkn_out)
        assert amount_out_expected['tkn_out_amt'] <= tkn_out.token_total, 'Balancer V1: INSUFFICIENT_OUTPUT_AMOUNT'   
        self.tkn_group.get_token(tkn_in.token_name).deposit(to, amt_tkn_in)
        self.swap(amount_out_expected['tkn_out_amt'], amount_out_expected['tkn_in_fee'], tkn_out, tkn_in, to)
        return amount_out_expected
    
    def swap_exact_amount_out(self, amt_tkn_out, tkn_out, tkn_in, to):
        
        """ swap_exact_amount_out

            Swap input token given output token 
                
            Parameters
            -------
            amt_tkn_in : float
                Amount of input token requested for swaping   
            tkn_in : ERC20
                Input token           
            tkn_out : ERC20
                Output token                    
            to : str
                User name/address                 
        """          
        
        assert self.tkn_group.get_token(tkn_in.token_name) and self.tkn_group.get_token(tkn_out.token_name), "Balancer: TOKEN NOT PART OF GROUP"
        
        amount_in_expected = self.get_amount_in(amt_tkn_out, tkn_out, tkn_in)
        assert amount_in_expected['tkn_in_amt'] <= tkn_in.token_total, 'Balancer V1: INSUFFICIENT_OUTPUT_AMOUNT'   
        self.tkn_group.get_token(tkn_out.token_name).deposit(to, amt_tkn_out)
        self.swap(amount_in_expected['tkn_in_amt'], amount_in_expected['tkn_out_fee'], tkn_in, tkn_out, to)
        return amount_in_expected    
    
    
    def swap(self, amt_swap, amt_fee, tkn_out, tkn_in, to): 
        
        """ swap

            Swap output token given input token 
                
            Parameters
            -------
            amt_out : float
                Amount of input token requested for swaping   
            tkn_in : ERC20
                Input token           
            tkn_out : ERC20
                Output token                    
            to : str
                User name/address                 
        """         
        
        self.tkn_group.get_token(tkn_out.token_name).transfer(to, amt_swap)
        new_tkn_balances = self.tkn_group.get_balances()
        
        res_balance_in = self.tkn_reserves[tkn_in.token_name]
        res_balance_out = self.tkn_reserves[tkn_out.token_name]
        
        new_balance_in = new_tkn_balances[tkn_in.token_name]
        new_balance_out = new_tkn_balances[tkn_out.token_name]
        
        if new_balance_in > res_balance_in - amt_swap:
            amount_in = new_balance_in - res_balance_in
        else:
            amount_in = 0
            
        assert amount_in > 0, 'Balancer V1: INSUFFICIENT_INPUT_AMOUNT'        
        
        res_balance_in_adjusted = res_balance_in + amount_in 
        res_balance_out_adjusted = res_balance_out - amt_swap
              
        lside = round(math.ceil(res_balance_in_adjusted * res_balance_out_adjusted), 8)
        rside = round(math.ceil(new_balance_in * new_balance_out), 8)     
        
        assert lside  ==  rside , 'Balancer V1: LP BALANCES NOT ALIGNED TO TKN BALANCES'
        
        self._update(new_balance_in, tkn_in.token_name)
        self._update(new_balance_out, tkn_out.token_name)
        self._tally_fees(tkn_in, amt_fee)
        
    def mint(self, new_shares, amt_tkn_in, tkn_in, to): 
        
        """ mint

            Update reserve amount for specific token in the pool
                
            Parameters
            -------
            new_shares : float
                Amount of new pool shares requested for minting   
            amt_tkn_in : float
                Input token           
            tkn_in : ERC20
                Output token                    
            to : str
                User name/address                 
        """          
        
        tkn_balance = self.tkn_group.get_token(tkn_in.token_name).token_total
        _amt_tkn_in = tkn_balance - self.tkn_reserves[tkn_in.token_name]
        
        assert round(_amt_tkn_in,5) == round(amt_tkn_in,5), 'Balancer V1: MINT ERROR'

        if self.pool_shares == 0:
            new_shares = new_shares - MINIMUM_SHARES
            self._mint("0", MINIMUM_SHARES)        
        
        new_balance = tkn_in.token_total
        self._update(new_balance, tkn_in.token_name)
        self._mint(to, new_shares)
        
    def _mint(self, to, value):
        
        """ _mint

            Update reserve amount for specific token in the pool
                
            Parameters
            -------
            value : float
                Amount of new pool shares requested for minting                     
            to : str
                User name/address                 
        """           
                
        if self.pool_providers.get(to):
            self.pool_providers[to] += value
        else:
            self.pool_providers[to] = value

        self.last_pool_deposit = value     
        self.pool_shares += value        

    def _update(self, new_balance, tkn_nm):
        
        """ _update

            Update reserve amounts specified token
                
            Parameters
            -------   
            new_balance : float
                New reserve amount of token      
            tkn_nm : ERC20
                Name of token being updated                  
        """          
        
        self.tkn_reserves[tkn_nm] = new_balance      

    def _tally_fees(self, tkn, fee):
        
        
        """ _tally_fees

            Tally fee from swap and record last collected fee
                
            Parameters
            -------   
            tkn : ERC20
                Token where fees are being collected for     
            fee : float
                Fee being collected                
        """         
        
        if tkn.token_name not in self.tkn_fees:
            self.tkn_fees[tkn.token_name] = 0
         
        self.tkn_fees[tkn.token_name] += fee        
        
        
    def get_amount_out(self, amt_tkn_in, tkn_in, tkn_out):  
        
        """ get_amount_out

            Given some amount of an asset, quotes an equivalent amount of the other asset
                
            Parameters
            -------
            amt_tkn_in : float
                Amount of token requested for quote            
            tkn_in : ERC20
                Input token                    
            tkn_out : ERC20
                Output token                    
        """          
        
        assert self.tkn_group.get_token(tkn_in.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        out = BalancerMath.calc_out_given_in(token_amount_in = Decimal(amt_tkn_in),
                                        token_balance_in = Decimal(tkn_in.token_total),
                                        token_weight_in = Decimal(tkn_denorm_wts[tkn_in.token_name]),
                                        token_balance_out = Decimal(tkn_out.token_total),
                                        token_weight_out = Decimal(tkn_denorm_wts[tkn_out.token_name]),
                                        swap_fee = Decimal(SWAP_FEE))
        
        return {'tkn_out_amt': float(out.result), 'tkn_in_nm': tkn_in.token_name, 'tkn_in_fee': float(out.fee)}
    
    def get_amount_in(self, amt_tkn_out, tkn_out, tkn_in):  
        
        """ get_amount_in

            Given some amount of an asset, quotes an equivalent amount of the other asset
                
            Parameters
            -------
            amt_tkn_out : float
                Amount of token requested for quote            
            tkn_out : ERC20
                Input token                    
            tkn_in : ERC20
                Output token                    
        """          
        
        assert self.tkn_group.get_token(tkn_in.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()      
        out = BalancerMath.calc_in_given_out(token_balance_in=Decimal(tkn_in.token_total),
                                        token_weight_in=Decimal(tkn_denorm_wts[tkn_in.token_name]),
                                        token_balance_out=Decimal(tkn_out.token_total),
                                        token_weight_out=Decimal(tkn_denorm_wts[tkn_out.token_name]),
                                        token_amount_out=Decimal(amt_tkn_out),
                                        swap_fee=Decimal(SWAP_FEE))        
        
        return {'tkn_in_amt': float(out.result), 'tkn_out_nm': tkn_out.token_name, 'tkn_out_fee': float(out.fee)}    
        

    def get_price(self, base_tkn, opp_tkn):
        
        """ get_price

            Get price of select token in the exchange pair
                
            Parameters
            -------
            base_tkn : float
                Base token request for price quote           
            opp_tkn : ERC20
                Denomination token of price quote                                     
        """         
        
        assert self.tkn_group.get_token(base_tkn.token_name), 'Balancer V1: TOKEN NOT PART OF GROUP'
        
        tkn_denorm_wts = self.tkn_group.get_denorm_weights()
        price = BalancerMath.calc_spot_price(token_balance_in = Decimal(base_tkn.token_total),
                                            token_weight_in = Decimal(tkn_denorm_wts[base_tkn.token_name]),
                                            token_balance_out = Decimal(opp_tkn.token_total),
                                            token_weight_out = Decimal(tkn_denorm_wts[opp_tkn.token_name]),
                                            swap_fee = Decimal(SWAP_FEE))
        
        return float(price)        
        
    def get_reserve(self, token):
        
        """ get_reserve

            Get reserve amount of select token in the pool
                
            Parameters
            -------
            token : ERC20
                ERC20 token                
        """            
        
        return self.tkn_reserves[token.token_name]
    
    
    
    