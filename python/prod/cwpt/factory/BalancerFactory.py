# BalancerFactory.py
# Author: Ian Moore ( utiliwire@gmail.com )
# Date: Sept 2023

from ...erc import ERC20
from ...cwpt.exchg import BalancerExchange 
from ...utils.interfaces import IExchangeFactory 
from ...utils.data import BalancerExchangeData
from ...utils.data import FactoryData
from ...vault import BalancerVault

class BalancerFactory(IExchangeFactory):
    
    """ 
        Create liquidity pools for given token pairs.
        
        Parameters
        ----------
        self.name : str
            Token name 
        self.address : str
            Token 0 name  
        self.exchange_from_token : dictionary
            Map of tokens to exchanges
        self.tokens_from_exchange : dictionary
            Map of exchanges to pair tokens          
    """       
      
    def __init__(self, name: str, address: str) -> None:
        self.name = name
        self.address = address
        self.exchange_from_token = {}
        self.token_from_exchange = {} 
        self.parent_lp = None
        
    def deploy(self, exchg_data : BalancerExchangeData):   
        
        vault = exchg_data.vault
        symbol = exchg_data.symbol
        address = exchg_data.address        
     
        assert symbol not in self.token_from_exchange, 'BalancerFactory: EXCHANGE_CREATED'            
            
        factory_struct = FactoryData(self.token_from_exchange,  self.parent_lp, self.name, self.address)
        exchg_struct = BalancerExchangeData(vault = vault, symbol=symbol, address=address)
        exchange = BalancerExchange(factory_struct, exchg_struct)             
            
        self.exchange_from_token[vault.get_name()] = exchange
        self.token_from_exchange[exchange.name] = vault.get_dict()
        
        return exchange  
    
    def get_exchange(self, token):
        
        return self.exchange_from_token.get(token)

    def get_token(self, exchange):       
        
        return self.token_from_exchange.get(exchange)
    