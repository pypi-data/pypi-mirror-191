# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astropic']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'astropy>=5.2.1,<6.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pyquery>=2.0.0,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'astropic',
    'version': '1.1.3',
    'description': 'Tool for editing astronomical object pictures',
    'long_description': "# astropic\nCode to modify the images using different redshifts and distances.\nMay be buggy, submit bugs in Github Issues.\nTo run your code, install the repository:\nWARNING: poetry and poetry-core are needed to build the package\n`pip install astropic`\nThen you are ready to run the main code.\nTo use the module in your code, do `from astropic.main import convert` and then run the `convert('info')`\nThere is also a bonus script fits2png.py, which modifies .fits files into .png files\n",
    'author': 'Aromik',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Aromik/image_modify_astro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
