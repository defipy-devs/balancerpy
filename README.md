# balancerpy
Python package for Balancer V2 modelling

## Install
To install package:
```
> git clone https://github.com/defipy-devs/balancerpy
> pip install .
```
or
```
> pip install BalancerPy
```

## Balancer

* See [test notebook](https://github.com/defipy-devs/uniswappy/blob/main/notebooks/tests/test_abstract.ipynb) 
for basic usage

```
from balancerpy import *

user_nm = 'user_test'

amt_dai = 10000000
denorm_wt_dai = 10

amt_eth = 67738.6361731024
denorm_wt_eth = 40

init_pool_shares = 100

dai = ERC20("DAI", "0x111")
dai.deposit(None, amt_dai)

weth = ERC20("WETH", "0x09")
weth.deposit(None, amt_eth)

bgrp = BalancerVault()
bgrp.add_token(dai, denorm_wt_dai)
bgrp.add_token(weth, denorm_wt_eth)

bfactory = BalancerFactory("WETH pool factory", "0x2")
exchg_data = BalancerExchangeData(vault = bgrp, symbol="LP", address="0x011")
lp = bfactory.deploy(exchg_data)

Join().apply(lp, user_nm, init_pool_shares)
lp.summary()
```

#### OUTPUT:
Balancer Exchange: DAI-WETH (LP)  <br/>
Reserves: DAI = 10000000, WETH = 67738.6361731024  <br/>
Weights: DAI = 0.2, WETH = 0.8  <br/>
Pool Shares: 100  <br/><br/> 
