# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['markus_pettersen']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'markus-pettersen',
    'version': '0.1.1',
    'description': 'Random useful python stuff I sometimes use',
    'long_description': "# utils\nI'm tired of making these functions all the time\n",
    'author': 'Markus Pettersen',
    'author_email': 'mp.markus94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MPettersen/markus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
