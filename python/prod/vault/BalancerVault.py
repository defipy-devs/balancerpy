# Copyright [2023] [Ian Moore]
# Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
# Email: defipy.devs@gmail.com

import numpy as np
from ..erc import ERC20

class BalancerVault:
    
    """ 
        Create Balancer vault for pool token management
        
        Parameters
        ---------------
        self.tkns : list
            List of ERC20 tokens within vault
        self.tkn_dic : dictionary
            Dictionary of ERC20 tokens within vault referenced by token name
        self.tkn_denorm_wts : dictionary
            Dictionary of denormalization weights referenced by token name
        self.tkn_bounds : dictionary
            Dictionary of booleans (indicating token bound) referenced by token name             
    """       
  
    def __init__(self) -> None:
        self.tkns = []
        self.tkn_dic = {}   
        self.tkn_denorm_wts = {}
        self.tkn_bounds = {}
        
    def add_token(self, tkn: ERC20, weight: float, bound: bool = True):
        
        """ add_token

            Deploy a Balancer liquidity pool (LP) exchange
                
            Parameters
            -----------------
            tkn : ERC20
                ERC20 token   
            weight : float
                Denormalized weight in pool    
            bound : boolean
                Indicator of whether token is bound to pool                        
        """          
        
        if tkn.token_name not in self.tkn_dic:    
            self.tkns.append(tkn) 
            self.tkn_dic[tkn.token_name] = tkn
            self.tkn_denorm_wts[tkn.token_name] = weight
            self.tkn_bounds[tkn.token_name] = bound
        else:
            print('ERROR: token already exists within group')

    def check_tkn(self, tkn):
        
        """ check_tkn

            Check if ERC20 token is in vault
                
            Parameters
            -----------------
            tkn : ERC20
                ERC20 token
                
            Returns
            -----------------
            contains : boolean
                Indicator of whether token is contained in vault                         
        """             
        
        tkn_nms = self.get_names()
        return tkn.token_name in tkn_nms         
            
    def get_name(self):
        
        """ get_name

            Get token names
                
            Returns
            -----------------
            tkn_nms : str
                Token names delimited by hyphen
        """          
        
        tkn_nms = self.get_names()
        return "-".join(tkn_nms)  
    
    def get_coins_str(self):
        tkn_nms = self.get_names()
        return "-".join(tkn_nms)    
 
    def get_token(self, tkn_name):
        
        """ get_token

            Get token from vault given its name symbol
            
            Parameters
            -----------------
            tkn_name : str
                Token name symbol            
                
            Returns
            -----------------
            tkn : ERC20
                Retrieved ERC20 token
        """           
        
        return self.tkn_dic[tkn_name]

    def get_tokens(self):
        
        """ get_tokens

            Get list of tokens
                    
            Returns
            -----------------
            tkns : list
                List of tokens
        """            
        
        return self.tkns
    
    def get_names(self):
        
        """ get_names

            Get token string names
                    
            Returns
            -----------------
            tkn_nms : list
                Token string names
        """           
        
        tkn_nms = []
        for tkn in self.tkns:
            tkn_nms.append(tkn.token_name) 
        return tkn_nms    
    
    def get_dict(self):
        
        """ get_dict

            Get dictionary of tokens referened by token name
                    
            Returns
            -----------------
            tkn_dict : dict
                Dictionary of tokens
        """          
        
        tkn_dict = {}
        for tkn in self.tkns:
            tkn_dict[tkn.token_name] = tkn
        return tkn_dict      
    
    def get_balances(self):
        
        """ get_balances

            Get dictionary of token balances referened by token name
                    
            Returns
            -----------------
            tkn_balances : dict
                Dictionary of token balances
        """          
        
        tkn_balances = {}
        for tkn in self.tkns:
            tkn_balances[tkn.token_name] = tkn.token_total
        return tkn_balances   
    
    def get_norm_weights(self):
        
        """ get_norm_weights

            Get dictionary of token normalized weights referened by token name
                    
            Returns
            -----------------
            norm_wts_dict : dict
                Dictionary of token normalized weights 
        """          
        
        tkn_denorm_wts = self.get_denorm_weights()
        norm_wts = self.normalize_float_arr(list(tkn_denorm_wts.values()))
        norm_wts_dict = {e:norm_wts[k] for k, e in enumerate(tkn_denorm_wts)} 
        return norm_wts_dict        
   
    def get_denorm_weights(self):
        
        """ get_norm_weights

            Get dictionary of token denormalized weights referened by token name
                    
            Returns
            -----------------
            norm_wts_dict : dict
                Dictionary of token denormalized weights 
        """          
        
        return self.tkn_denorm_wts   
    
    def get_bounds(self):
        
        """ get_bounds

            Get dictionary of token bounds referened by token name
                    
            Returns
            -----------------
            norm_wts_dict : dict
                Dictionary of token bounds indicating whether token is bound to pool
        """          
        
        return self.tkn_bounds       
        
    def get_base_token(self):
        return self.base_tkn
    
    def get_base_token_name(self):
        return self.base_tkn.token_name   
    
    def get_total_denorm_weight(self):
        total_weight = 0
        for tkn in self.tkns:
            if self.tkn_bounds[tkn.token_name]:
                total_weight += self.tkn_denorm_wts[tkn.token_name] 
        return total_weight 
    
    def normalize_float_arr(self, float_arr):
        return list(float_arr/np.sum(float_arr))    
        