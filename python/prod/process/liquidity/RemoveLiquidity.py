# Copyright [2025] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from ..Process import Process
from uniswappy import TokenDeltaModel
from uniswappy import EventSelectionModel

class RemoveLiquidity(Process):
    
    """ Remove liquidity process

        Parameters
        ----------
        ev : EventSelectionModel
            EventSelectionModel object to randomly generate buy vs sell events
        tDel : TokenDeltaModel
            TokenDeltaModel to randomly generate token amounts        
    """       

    def __init__(self, ev = None, tDel = None):
        self.ev = EventSelectionModel() if ev  == None else ev
        self.tDel = TokenDeltaModel(50) if tDel == None else tDel

    def apply(self, lp, token_in, user_nm, amount_in):    
        
        """ apply

            Swap token X for token Y (and vice verse) 
                
            Parameters
            -------
            lp : Exchange
                LP exchange
            token_in : ERC20
                specified ERC20 token               
            user_nm : str
                account name
            amount_in : float
                token amount to be swap             
                
            Returns
            -------
            amount_out_expected : float
                exchanged token amount               
        """ 

        return None