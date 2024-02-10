from abc import *
from .IExchange import IExchange 

class IExchangeFactory(ABC):
    
    @abstractmethod        
    def deploy(self, agents):
        pass
    
    @abstractmethod        
    def get_exchange(self, exchange: IExchange):
        pass
    
    @abstractmethod        
    def get_token(self, exchange: IExchange):
        pass    