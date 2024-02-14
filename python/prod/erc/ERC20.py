# Copyright [2023] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

class ERC20:
    
    """ ERC20 token

        Parameters
        ---------------
        self.token_name : str
            Token name 
        self.token_addr : str
            Token address  
        self.token_total : float
            Token holdings 
    """   
    def __init__(self, name: str, addr: str) -> None:
        self.token_name = name
        self.token_addr = addr
        self.token_supply = 1_000_000_000
        self.token_total = 0
        self.type = 'standard'

    def deposit(self, _from, value):
        
        """ deposit

            Deposit token amount in
                
            Parameters
            ---------------
            _from : str
                user address   
            value : str
                delta to add to total                
        """           
        
        self.token_total += value

    def transfer(self, _to, value):
        
        """ transfer

            Transfer token amount out
                
            Parameters
            ---------------
            _to : str
                user address   
            value : str
                delta to remove from total                
        """         
        
        self.token_total -= value
        
