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
    'version': '1.1.2',
    'description': 'Tool for editing astronomical object pictures',
    'long_description': "# astro-pics\nCode to modify the images using different redshifts and distances.\nMay be buggy, submit bugs in Github Issues.\nTo run your code, install the repository:\n`pip install astro-pics`\nThen you are ready to run the main code.\nTo use the module in your code, do `from astro_pics.main import convert` and then run the `convert('info')`\nThere is also a bonus script fits2png.py, which modifies .fits files into .png files\n\nWARNING: The version on pypi.org is outdated, since the package isn't being updated there. Instead go and see https://github.com/Aromik/image_modify_astro\n",
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
