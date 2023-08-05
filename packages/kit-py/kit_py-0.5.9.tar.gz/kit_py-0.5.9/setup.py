# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kit',
 'kit.decorator',
 'kit.dict',
 'kit.list',
 'kit.rpc',
 'kit.rpc.broker',
 'kit.rpc.config',
 'kit.rpc.middleware',
 'kit.store',
 'kit.tool']

package_data = \
{'': ['*']}

install_requires = \
['amqpstorm[rabbitmq]>=2.10.5,<3.0.0',
 'croniter>=1.3.8,<2.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'loguru>=0.6.0,<0.7.0',
 'nacos-sdk-python==0.1.8',
 'redis[redis]>=4.3.4,<5.0.0',
 'uvicorn>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['kit-tool = kit.cmdline:execute']}

setup_kwargs = {
    'name': 'kit-py',
    'version': '0.5.9',
    'description': '个人代码工具包',
    'long_description': "### miclon 个人代码工具包\n\n### APIS\n\n- [Dict](kit/dict/addict.py)\n\n```python\nfrom kit.dict import Dict\n\nd = Dict({'a': {'d': {'e': 100}}, 'b': 2, 'c': 3})\nprint(d.a.d.e)  # 100\nprint(d.a.c)  # {}\n```",
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mic1on/kit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
