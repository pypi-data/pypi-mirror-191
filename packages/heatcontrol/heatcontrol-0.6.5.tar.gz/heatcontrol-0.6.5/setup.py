# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heatcontrol']

package_data = \
{'': ['*']}

install_requires = \
['mock-gpio>=0.1.8,<0.2.0',
 'requests>=2.28.2,<3.0.0',
 'rpi-gpio>=0.7.1,<0.8.0',
 'schedule>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['spot_price_control = heatcontrol:main']}

setup_kwargs = {
    'name': 'heatcontrol',
    'version': '0.6.5',
    'description': '',
    'long_description': '# spot-price-heating-control\nReduces power of central heating on most expensive hours of a day\n',
    'author': 'Rami Rahikkala',
    'author_email': 'rami.rahikkala@gmail.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
