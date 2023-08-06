# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_workflows', 'np_workflows.models', 'np_workflows.shared']

package_data = \
{'': ['*'], 'np_workflows': ['assets/images/*']}

install_requires = \
['ipywidgets>=7,<8',
 'np_datajoint',
 'np_probe_targets',
 'np_services',
 'pydantic>=1,<2']

extras_require = \
{'dev': ['pip-tools', 'isort', 'mypy', 'black', 'pytest', 'poetry']}

setup_kwargs = {
    'name': 'np-workflows',
    'version': '1.2.0',
    'description': 'Ecephys and behavior workflows for the Mindscope Neuropixels team.',
    'long_description': '# np_workflows',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
