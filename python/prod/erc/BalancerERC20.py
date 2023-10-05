# WeightedPoolERC20.py
# Author: Ian Moore ( imoore@syscoin.org )
# Date: Sept 2023

from python.prod.erc import ERC20

class BalancerERC20(ERC20):
    
    """ BalancerERC20 token

        Parameters
        ----------
        self.token_name : str
            Token name 
        self.token_addr : str
            Token address  
        self.token_total : float
            Token holdings 
        self.token_weight : float
            Token weight  
        self.token_denorm_weight : float
            Token denorm weight              
            
    """   
    def __init__(self, name: str, addr: str) -> None:
        self.token_name = name
        self.token_addr = addr
        self.token_total = 0
        self.token_weight = 0
        self.token_denorm_weight = 0
        self.bound = True
        self.type = 'weightedpool'
        
    def set_params(self, balance, weight, denorm, bound):
        self.token_weight = weight
        self.token_denorm_weight = denorm
        self.token_total = balance
        self.bound = bound
           
    def set_weight(self, token_weight):
        
        """ set_token_weight

            Reset token weight
                
            Parameters
            -------
            token_weight : float
                token weight        
        """         
        
        self.token_weight = token_weight    
        
        
    def set_denorm_weight(self, token_denorm_weight):
        
        """ set_token_denorm_weight

            Reset token denorm weight
                
            Parameters
            -------
            token_denorm_weight : float
                token denorm weight       
        """         
        
        self.token_denorm_weight = token_denorm_weight 
        
        
    def set_bound(self, bound):
        
        """ set_bound

            Reset token bound
                
            Parameters
            -------
            set_bound : boolean
                token bound        
        """         
        
        self.bound = bound           