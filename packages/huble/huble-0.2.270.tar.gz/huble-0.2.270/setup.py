# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['huble',
 'huble.automl',
 'huble.connector',
 'huble.error',
 'huble.sklearn',
 'huble.sklearn.essentials',
 'huble.sklearn.metrics',
 'huble.sklearn.process',
 'huble.sklearn.temp',
 'huble.sklearn.temp.content',
 'huble.sklearn.train',
 'huble.util']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.8.0,<23.0.0',
 'boto3>=1.26.63,<2.0.0',
 'catboost>=1.1.1,<2.0.0',
 'datacleaner>=0.1.5,<0.2.0',
 'kaleido==0.2.1',
 'lightgbm>=3.3.5,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'py-AutoClean>=1.1.3,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'scikit-learn==1.1.2',
 'scipy>=1.7.0,<1.8.0',
 'woodwork>=0.21.1,<0.22.0',
 'xgboost>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'huble',
    'version': '0.2.270',
    'description': '',
    'long_description': '',
    'author': 'Rugz007',
    'author_email': 'rugvedsomwanshi007@gmail.com',
    'maintainer': 'Arjit Agarwal',
    'maintainer_email': 'arjitagarwal123@gmail.com',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
