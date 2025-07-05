# Copyright 2023–2025 Ian Moore
# Email: defipy.devs@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

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
        
