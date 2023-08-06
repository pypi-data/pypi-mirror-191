# trade-lib
自己的交易常用库

```
pip install trade-lib
```

## 使用

```python

import trade_lib

# load exchange config from ~/.config/exchange.yaml
config = trade_lib.get_exchange_config(exname)

# set_dingding
dingding_config = {'robot_id':'', 'secret':''}
trade_lib.set_dingding(dingding_config)
trade_lib.dinding_send('ding...')
```

## upload to pypi

```
python3 setup.py sdist bdist_wheel

twine upload dist/*
```