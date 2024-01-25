# balancerpy
Python package for Balancer V1 modelling
* Currently in Beta (version 0.0.5) until fully tested and analyzed

## Install
To install package:
```
> git clone https://github.com/icmoore/balancerpy
> pip install .
```
or
```
> pip install BalancerPy
```

## Basic Weighted Pool Overview
* See [test notebook](https://github.com/icmoore/balancerpy/blob/main/notebooks/tests/weighted_pool_tests.ipynb) for example implementation
* Python implementation of Balancer Weighted Pools 'broadly' consists of two main components
    * BalancerMath.py: refactor of [Balancer V1 Math solidity contract code](https://github.com/balancer/balancer-core/blob/master/contracts/BMath.sol), and was copied from [BalancerPools_Model GH repos](https://github.com/TokenEngineeringCommunity/BalancerPools_Model/blob/main/model/parts/balancer_math.py)
    * BalancerExchange.py: refactor of [Balancer Pool solidity contract code](https://github.com/balancer/balancer-core/blob/master/contracts/BPool.sol), created in-house (+ supporting classes)
* The mapping (contract code -> math refactor -> exchange refactor) is as follows:
    * **Price**
        * BMath.calcSpotPrice() -> BalancerMath.calc_spot_price() -> BalancerExchange.get_price()
    * **Swapping**    
        * BMath.calcOutGivenIn() -> BalancerMath.calc_out_given_in() -> BalancerExchange.get_amount_out()
        * BMath.calcInGivenOut() -> BalancerMath.calc_in_given_out() -> BalancerExchange.get_amount_in()
    * **Adding Liquidity**    
        * BMath.calcPoolOutGivenSingleIn() -> BalancerMath.calc_pool_out_given_single_in() -> BalancerExchange.join_swap_extern_amount_in()    
        * BMath.calcSingleInGivenPoolOut() -> BalancerMath.calc_single_in_given_pool_out() -> BalancerExchange.join_swap_pool_amount_out()
    * **Removing Liquidity**     
        * BMath.calcPoolInGivenSingleOut() -> BalancerMath.calc_pool_in_given_single_out() -> BalancerExchange.exit_swap_extern_amount_out()
        * BMath.calcSingleOutGivenPoolIn() ->  BalancerMath.calc_single_out_given_pool_in() -> BalancerExchange.exit_swap_pool_amount_in()

