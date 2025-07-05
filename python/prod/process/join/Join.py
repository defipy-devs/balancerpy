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