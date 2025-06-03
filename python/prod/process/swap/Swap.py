# Copyright [2025] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from ...enums import Proc 
from uniswappy import TokenDeltaModel
from uniswappy import EventSelectionModel
import math

class Swap():
    
    """ Process to swap token X for token Y (and vice verse) 

        Parameters
        ----------
        kind : Proc
            Type of swap proceedure
        ev : EventSelectionModel
            EventSelectionModel object to randomly generate buy vs sell events
        tDel : TokenDeltaModel
            TokenDeltaModel to randomly generate token amounts                 
    """       

    def __init__(self, kind = None, ev = None, tDel = None):
        self.kind = Proc.SWAPOUT if kind == None else kind
        self.ev = EventSelectionModel() if ev  == None else ev
        self.tDel = TokenDeltaModel(50) if tDel == None else tDel

    def apply(self, lp, token_in, token_out, user_nm, amount):    
        
        """ apply

            Swap token X for token Y (and vice verse) 
                
            Parameters
            -------
            lp : Exchange
                LP exchange
            token_in : ERC20
                specified ERC20 input token     
            token_out : ERC20
                specified ERC20 output token     
            user_nm : str
                account name
            amount : float
                token amount to swapped (either swap-in or swap-out)            
                
            Returns
            -------
            amount_out_expected : float
                exchanged token amount               
        """ 
        match self.kind:
            case Proc.SWAPIN:
                out = lp.swap_exact_amount_out(amount, token_out, token_in, user_nm)
            case Proc.SWAPOUT:
                out = lp.swap_exact_amount_in(amount, token_in, token_out, user_nm)
        
        return out