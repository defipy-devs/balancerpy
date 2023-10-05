# BalancerERC20Group.py
# Author: Ian Moore ( imoore@syscoin.org )
# Date: Sept 2023

from python.prod.cwpt.erc import BalancerERC20

class BalancerERC20Group:
  
    def __init__(self) -> None:
        self.tkns = []
        self.tkn_dic = {}
        self.base_tkn = None
       
    def add_base_token(self, tkn: BalancerERC20):
        self.base_tkn = tkn
        if tkn.token_name not in self.tkn_dic:
            self.tkns.append(tkn)
            self.tkn_dic[tkn.token_name] = tkn
        else:
            print('ERROR: token already exists within group')
            
        
    def add_token(self, tkn: BalancerERC20):
        if(self.base_tkn == None):
            print('ERROR: must add base token')
        elif tkn.token_name not in self.tkn_dic:    
            self.tkns.append(tkn) 
            self.tkn_dic[tkn.token_name] = tkn
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
    
    def get_weights(self):
        tkn_weights = {}
        for tkn in self.tkns:
            tkn_weights[tkn.token_name] = tkn.token_weight
        return tkn_weights      
        
    def get_base_token(self):
        return self.base_tkn
    
    def get_base_token_name(self):
        return self.base_tkn.token_name   
    
    def get_total_denorm_weight(self):
        total_weight = 0
        for tkn in self.tkns:
            if tkn.bound:
                total_weight += tkn.token_denorm_weight
        return total_weight    
        