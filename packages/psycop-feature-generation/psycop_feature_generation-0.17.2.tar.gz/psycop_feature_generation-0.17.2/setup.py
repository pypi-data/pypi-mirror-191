# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psycop_feature_generation',
 'psycop_feature_generation.application_modules',
 'psycop_feature_generation.data_checks',
 'psycop_feature_generation.data_checks.flattened',
 'psycop_feature_generation.data_checks.raw',
 'psycop_feature_generation.featurizers',
 'psycop_feature_generation.loaders',
 'psycop_feature_generation.loaders.example',
 'psycop_feature_generation.loaders.flattened',
 'psycop_feature_generation.loaders.raw',
 'psycop_feature_generation.loaders.synth.raw']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<1.5.42',
 'catalogue>=2.0.0,<2.1.0',
 'dask>=2022.9.0,<2023.2.0',
 'deepchecks>=0.8.0,<0.11.0',
 'dill>=0.3.0,<0.3.6',
 'frozendict>=2.3.4,<3.0.0',
 'numpy>=1.23.3,<1.23.6',
 'pandas>=1.4.0,<1.6.0',
 'protobuf<=3.20.3',
 'psutil>=5.9.1,<6.0.0',
 'psycopmlutils>=0.2.4,<0.4.0',
 'pyarrow>=9.0.0,<9.1.0',
 'pydantic>=1.9.0,<1.10.0',
 'pyodbc>=4.0.34,<4.0.36',
 'scikit-learn>=1.1.2,<1.1.3',
 'scipy>=1.8.0,<1.9.4',
 'srsly>=2.4.4,<2.4.6',
 'timeseriesflattener>=0.21.0',
 'transformers>=4.22.2,<5.0.0',
 'wandb>=0.12.0,<0.13.5',
 'wasabi>=0.9.1,<0.10.2']

setup_kwargs = {
    'name': 'psycop-feature-generation',
    'version': '0.17.2',
    'description': '',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
