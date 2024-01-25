# BalancerERC20Group.py
# Author: Ian Moore ( utiliwire@gmail.com )
# Date: Sept 2023

import numpy as np
from ..erc import ERC20

class BalancerVault:
  
    def __init__(self) -> None:
        self.tkns = []
        self.tkn_dic = {}   
        self.tkn_denorm_wts = {}
        self.tkn_bounds = {}
        
    def add_token(self, tkn: ERC20, weight: float, bound: bool = True):
        if tkn.token_name not in self.tkn_dic:    
            self.tkns.append(tkn) 
            self.tkn_dic[tkn.token_name] = tkn
            self.tkn_denorm_wts[tkn.token_name] = weight
            self.tkn_bounds[tkn.token_name] = bound
        else:
            print('ERROR: token already exists within group')

    def check_tkn(self, tkn):
        tkn_nms = self.get_names()
        return tkn.token_name in tkn_nms         
            
    def get_name(self):
        tkn_nms = self.get_names()
        return "-".join(tkn_nms)  
    
    def get_coins_str(self):
        tkn_nms = self.get_names()
        return "/".join(tkn_nms)    
 
    def get_token(self, tkn_name):
        return self.tkn_dic[tkn_name]

    def get_tokens(self):
        return self.tkns
    
    def get_names(self):
        tkn_nms = []
        for tkn in self.tkns:
            tkn_nms.append(tkn.token_name) 
        return tkn_nms    
    
    def get_dict(self):
        tkn_dict = {}
        for tkn in self.tkns:
            tkn_dict[tkn.token_name] = tkn
        return tkn_dict      
    
    def get_balances(self):
        tkn_balances = {}
        for tkn in self.tkns:
            tkn_balances[tkn.token_name] = tkn.token_total
        return tkn_balances   
    
    def get_norm_weights(self):
        tkn_denorm_wts = self.get_denorm_weights()
        norm_wts = self.normalize_float_arr(list(tkn_denorm_wts.values()))
        norm_wts_dict = {e:norm_wts[k] for k, e in enumerate(tkn_denorm_wts)} 
        return norm_wts_dict        
   
    def get_denorm_weights(self):
        return self.tkn_denorm_wts   
    
    def get_bounds(self):
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
        