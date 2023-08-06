# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['np_datajoint', 'np_datajoint.hpc']

package_data = \
{'': ['*']}

install_requires = \
['datajoint==0.13',
 'djsciops>=1,<2',
 'fabric>=2,<3',
 'ipywidgets>=7,<8',
 'np_logging',
 'np_session',
 'numpy>=1,<2',
 'pandas>=1,<2',
 'requests',
 'seaborn']

setup_kwargs = {
    'name': 'np-datajoint',
    'version': '0.0.4',
    'description': 'Tools for spike-sorting Mindscope neuropixels ecephys sessions on DataJoint, retrieving results and comparing with locally-sorted equivalents.',
    'long_description': 'Tools for spike-sorting Mindscope neuropixels ecephys sessions on DataJoint, retrieving results and comparing with locally-sorted equivalents.',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben Hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
