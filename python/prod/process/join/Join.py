# Copyright [2025] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

from ...utils.data import BalancerExchangeData
import math

class Join():
    
    """ Process to join x and y amounts to pool              
    """       

    def __init__(self):
        pass

    def apply(self, lp, user_nm, shares):
        """ apply

            Join x and y amounts to pool
                
            Parameters
            -------
            lp : Exchange
                LP exchange            
            user_nm : str
                account name
            shares : float
               x token amount      
                     
            Returns
            -------
            out : dictionary
                join output               
        """ 
        vault = lp.vault    
        out = lp.join_pool(vault, shares, user_nm)

        return None