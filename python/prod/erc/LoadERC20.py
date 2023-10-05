# BalancerERC20.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: Token class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: May 2023

from decimal import Decimal

class LoadERC20:
    
    def __init__(self, weight: Decimal, denorm_weight: Decimal, balance: Decimal, bound: bool):
        self.weight = weight
        self.denorm_weight = denorm_weight
        self.balance = balance
        self.bound = bound

    def __repr__(self):
        return "Token weight: {}, denorm_weight: {}, balance: {}, bound: {}".format(self.weight, self.denorm_weight, self.balance, self.bound)

    def __eq__(self, other):
        if isinstance(other, BalancerERC20):
            return (self.weight == other.weight) and (self.denorm_weight == other.denorm_weight) and (self.balance == other.balance) and (self.bound == other.bound)
        return NotImplemented

    def add(self, num):
        self.amount = self.amount + num
        return self.amount

    @property
    def balance(self):
        return self.__dict__['balance']

    @balance.setter
    def balance(self, value):
        self.__dict__['balance'] = self.__ensure_type(value, Decimal)
        
    def __ensure_type(self, value, types):
        if isinstance(value, types):
            return value
        else:
            raise TypeError('Value {value} is {value_type}, but should be {types}!'.format(
                value=value, value_type=type(value), types=types))    
        
        
        
        
