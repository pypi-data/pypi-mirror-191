# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['magnify']

package_data = \
{'': ['*']}

install_requires = \
['basicpy>=1.0.1,<2.0.0',
 'numpy>=1.21.0,<2.0.0',
 'opencv-python>=4.7.0,<5.0.0',
 'scipy==1.9.1']

setup_kwargs = {
    'name': 'magnify',
    'version': '0.1.0',
    'description': 'A microscopy image processing toolkit.',
    'long_description': '# magnify\nA microscopy image processing toolkit.\n',
    'author': 'Karl Krauth',
    'author_email': 'karl.krauth@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
