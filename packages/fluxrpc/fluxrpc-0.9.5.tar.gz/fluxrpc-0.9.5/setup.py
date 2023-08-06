# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluxrpc',
 'fluxrpc.auth',
 'fluxrpc.dispatch',
 'fluxrpc.protocols',
 'fluxrpc.server',
 'fluxrpc.transports',
 'fluxrpc.transports.socket']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.16.0,<2.0.0']

extras_require = \
{':extra == "socket"': ['pymongo>=4.3.2,<5.0.0'],
 'gevent': ['gevent>=21.1.2,<22.0.0'],
 'httpclient': ['gevent-websocket>=0.10.1,<0.11.0', 'requests>=2.28.1,<3.0.0'],
 'msgpack': ['msgpack>=1.0.2,<2.0.0'],
 'rabbitmq': ['pika>=1.2.0,<2.0.0'],
 'socket': ['pycryptodomex>=3.15.0,<4.0.0',
            'python-bitcoinlib>=0.11.2,<0.12.0'],
 'websocket': ['gevent-websocket>=0.10.1,<0.11.0'],
 'wsgi': ['werkzeug>=2.2.2,<3.0.0'],
 'zmq': ['pyzmq>=22.0.3,<23.0.0']}

setup_kwargs = {
    'name': 'fluxrpc',
    'version': '0.9.5',
    'description': '"A sercure RPC provider for Flux"',
    'long_description': 'None',
    'author': 'David White',
    'author_email': 'dr.white.nz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
