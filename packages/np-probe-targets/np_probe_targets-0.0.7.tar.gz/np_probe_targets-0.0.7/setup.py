# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_probe_targets']

package_data = \
{'': ['*'], 'np_probe_targets': ['.ipynb_checkpoints/*']}

setup_kwargs = {
    'name': 'np-probe-targets',
    'version': '0.0.7',
    'description': '',
    'long_description': None,
    'author': 'bjhardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
