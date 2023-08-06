# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trade_lib']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0', 'aiohttp>=3.8.3,<4.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'trade-lib',
    'version': '0.2.0',
    'description': '我的交易库',
    'long_description': "# trade-lib\n自己的交易常用库\n\n```\npip install trade-lib\n```\n\n## 使用\n\n```python\n\nimport trade_lib\n\n# load exchange config from ~/.config/exchange.yaml\nconfig = trade_lib.get_exchange_config(exname)\n\n# set_dingding\ndingding_config = {'robot_id':'', 'secret':''}\ntrade_lib.set_dingding(dingding_config)\ntrade_lib.dinding_send('ding...')\n```\n\n## upload to pypi\n\n```\npython3 setup.py sdist bdist_wheel\n\ntwine upload dist/*\n```",
    'author': 'oscar',
    'author_email': 'oscnet@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
