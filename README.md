# balancerpy
Python package for Balancer V2 modelling

🔗 SPDX-Anchor: [anchorregistry.ai/AR-2026-6pDkj46](https://anchorregistry.ai/AR-2026-6pDkj46)

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

* See [test notebook](https://github.com/defipy-devs/balancerpy/blob/main/notebooks/tests/test_abstract.ipynb) 
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


### Swap (out-given-in)

```
amt_tkn_in = 10000
tkn_in = dai
tkn_out = weth

res = Swap(Proc.SWAPOUT).apply(lp, tkn_in, tkn_out, user_nm, amt_tkn_in)
lp.summary()

print(f"{amt_tkn_in} {tkn_in.token_name} was swapped into {res['tkn_out_amt']} {tkn_out.token_name}")
```

#### OUTPUT:
Balancer Exchange: DAI-WETH (LP) <br/>
Reserves: DAI = 10010000, WETH = 67721.75437414162 <br/>
Weights: DAI = 0.2, WETH = 0.8 <br/>
Pool Shares: 100 <br/>  

10000 DAI was swapped into 16.881798960778035 WETH  <br/><br/> 

### Swap (out-given-in)

```
amt_tkn_out = 20
tkn_out = weth
tkn_in = dai

res = Swap(Proc.SWAPIN).apply(lp, tkn_in, tkn_out, user_nm, amt_tkn_out)
lp.summary()

print(f"{amt_tkn_out} {tkn_out.token_name} was swapped into {res['tkn_in_amt']} {tkn_in.token_name}")
```

#### OUTPUT:
Balancer Exchange: DAI-WETH (LP) <br/>
Reserves: DAI = 9998136.750149786, WETH = 67741.75437414162 <br/>
Weights: DAI = 0.2, WETH = 0.8 <br/>
Pool Shares: 100 <br/> 

20 WETH was swapped into 11863.249850213939 DAI  <br/><br/> 

## Testing

Run the full test suite from the repo root:

```
> python -m pytest python/test/ -v
```

Tests cover:

- **Process**: join, swap (exact-in/exact-out, price impact), add/remove liquidity (by token and by shares), exit pool
- **Quotes**: CWP share-to-amount and amount-to-share conversions with round-trip verification
- **Math**: all `BalancerMath` static methods (spot price, out-given-in, in-given-out, pool/single token conversions)

### Requirements

```
> pip install pytest
```

## License
Licensed under the Apache License, Version 2.0.  
See [LICENSE](./LICENSE) and [NOTICE](./NOTICE) for details.  
Portions of this project may include code from third-party projects under compatible open-source licenses.