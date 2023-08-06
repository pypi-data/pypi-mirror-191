# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blazectl',
 'blazectl.cli',
 'blazectl.cluster',
 'blazectl.commons',
 'blazectl.job',
 'blazectl.kube',
 'blazectl.kube.eks',
 'blazectl.namespace']

package_data = \
{'': ['*'], 'blazectl.kube': ['airflow/*', 'mysql/*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'dnspython>=2.2.1,<3.0.0',
 'kubernetes>=25.3.0,<26.0.0',
 'mysql-connector-python>=8.0.32,<9.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'ray[default]>=2.2.0,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'shellingham>=1.5.0.post1,<2.0.0',
 'typer==0.7']

entry_points = \
{'console_scripts': ['blazectl = blazectl.cli.main_cli:app']}

setup_kwargs = {
    'name': 'blazectl',
    'version': '0.5.0',
    'description': '',
    'long_description': '# blaze-ctl\n\nController to manage blaze cluster in cloud (aws) environment\n\n## Concepts\n\n### Namespace\n\nBlaze clusters are created in a namespace, where a namespace defines and manges associated resources, such as -\n\n* EKS Cluster\n* Provisioner\n* Block Device\n* FSX Volumes\n* Service Account\n\nBefore we can create a cluster, we need to have a namespace and permission to manage cluster in that namespace.\n\nEach namespace has two group of users -\n\n* `blaze-user`: they can create / delete cluster and see pod and svc status\n* `blaze-admin`: they can additionally manage FSX Volumes, service accounts, gpu support\n\n## [Commands](docs/commands.md)\n\n[Link](docs/commands.md)\n\n## Install\n\n`pip install blazectl`\n\n## Build\n\n`poetry build`\n\n## Publish\n\n`poetry publish`',
    'author': 'Shailendra Sharma',
    'author_email': 'shailendra.sharma@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
