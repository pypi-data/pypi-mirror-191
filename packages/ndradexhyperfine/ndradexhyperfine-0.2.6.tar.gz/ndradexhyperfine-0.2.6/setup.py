# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndradexhyperfine']

package_data = \
{'': ['*'],
 'ndradexhyperfine': ['bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md']}

install_requires = \
['astropy>=4.0',
 'astroquery>=0.4',
 'netcdf4>=1.5',
 'numpy>=1.18',
 'pandas>=0.25',
 'toml>=0.10',
 'tqdm>=4.41',
 'xarray>=0.15']

setup_kwargs = {
    'name': 'ndradexhyperfine',
    'version': '0.2.6',
    'description': 'Python package for RADEX grid calculation',
    'long_description': 'None',
    'author': 'Thomas Williams',
    'author_email': 'thomas.g.williams94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
