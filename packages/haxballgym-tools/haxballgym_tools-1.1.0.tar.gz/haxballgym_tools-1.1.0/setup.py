# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haxballgym_tools',
 'haxballgym_tools.examples',
 'haxballgym_tools.model_testing',
 'haxballgym_tools.sb3_utils']

package_data = \
{'': ['*']}

install_requires = \
['haxballgym==0.5.6',
 'psutil>=5.9.4,<6.0.0',
 'stable-baselines3>=1.6.2,<2.0.0',
 'tensorboard>=2.11.2,<3.0.0']

setup_kwargs = {
    'name': 'haxballgym-tools',
    'version': '1.1.0',
    'description': '',
    'long_description': '# HaxBallGym-tools\n\nExtra tools for HaxballGym.\n\nContains environments for [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/)\n\n## Installation\n\n`pip install haxballgym-tools`\n',
    'author': 'Wazarr',
    'author_email': 'jeje_04@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
