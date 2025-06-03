# Copyright [2025] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from ...enums import Proc 
from uniswappy import TokenDeltaModel
from uniswappy import EventSelectionModel

class RemoveLiquidity():
    
    """ Remove liquidity process

        Parameters
        ----------
        kind : Proc
            Type of swap proceedure
        ev : EventSelectionModel
            EventSelectionModel object to randomly generate buy vs sell events
        tDel : TokenDeltaModel
            TokenDeltaModel to randomly generate token amounts        
    """       

    def __init__(self, kind = None, init_price = None, ev = None, tDel = None):
        self.kind = Proc.REMOVETKN if kind == None else kind
        self.ev = EventSelectionModel() if ev  == None else ev
        self.tDel = TokenDeltaModel(50) if tDel == None else tDel

    def apply(self, lp, token_out, user_nm, amount_out):    
        
        """ apply

            Remove liquidity based on token or share amounts 
                
            Parameters
            -------
            lp : Exchange
                LP exchange
            token_out : ERC20
                specified ERC20 token               
            user_nm : str
                account name
            amount_out : float
                token amount to be swap             
                
            Returns
            -------
            out : float
                exchanged token amount               
        """ 

        match self.kind:
            case Proc.REMOVETKN:
                out = lp.exit_swap_extern_amount_out(amount_out, token_out, user_nm)
            case Proc.REMOVESHARES:
                out = lp.exit_swap_pool_amount_in(amount_out, token_out, user_nm)
        
        return out