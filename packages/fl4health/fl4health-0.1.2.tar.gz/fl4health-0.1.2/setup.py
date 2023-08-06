# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fl4health',
 'fl4health.client_managers',
 'fl4health.clients',
 'fl4health.model_bases',
 'fl4health.parameter_exchange',
 'fl4health.privacy',
 'fl4health.strategies',
 'fl4health.utils']

package_data = \
{'': ['*']}

install_requires = \
['flwr>=1.2.0,<2.0.0',
 'opacus>=1.3.0,<2.0.0',
 'tensorflow-privacy>=0.8.7,<0.9.0',
 'torch>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'fl4health',
    'version': '0.1.2',
    'description': 'Federated Learning for Health',
    'long_description': '# FL4Health\nRepository containing a federated learning engine aimed at health experimentation with an ultimate target of integration into the DHDP, the static code checker runs on python3.8\n\n# Installing dependencies\n```\npip install --upgrade pip\npip install -r requirements.txt\n```\n\n# using pre-commit hooks\nTo check your code at commit time\n```\npre-commit install\n```\n\nYou can also get pre-commit to fix your code\n```\npre-commit run\n```\n',
    'author': 'Vector AI Engineering',
    'author_email': 'fl4health@vectorinstitute.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
