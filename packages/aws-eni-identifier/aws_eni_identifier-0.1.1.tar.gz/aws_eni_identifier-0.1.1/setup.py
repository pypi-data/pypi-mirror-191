# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_eni_identifier']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'glom>=23.1.1,<24.0.0', 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['aws-eni-identifier = aws_eni_identifier.cli:main']}

setup_kwargs = {
    'name': 'aws-eni-identifier',
    'version': '0.1.1',
    'description': 'Identify to which AWS service network interface is associated',
    'long_description': '# aws-eni-identifier\nIdentify to which AWS service network interface is associated\n\n![aws-eni-identifier-cli.png](docs/aws-eni-identifier-cli.png?raw=true)\n\n# Installation\n\n```bash\npip install git+https://github.com/fivexl/aws-eni-identifier.git\n```\nTODO: pip install aws-eni-identifier\n\n# Usage\naws-eni-identifier does not connect to AWS by itself, so you will need to load data wit aws-cli\n\nLogin to aws:\n```bash\naws sso login --profile my-profile\n```\n\nUse pipe:\n```bash\naws ec2 describe-network-interfaces | aws-eni-identifier\n```\n\nOr save to file with aws-cli and read it:\n```bash\naws ec2 describe-network-interfaces > ni.json\naws-eni-identifier -i ni.json\n```\n\n\n\n# Developing\n\nInstall the package:\n```bash\npoetry install\n```\nRun tests:\n```bash\npytest\n```',
    'author': 'Eremin',
    'author_email': 'haru.eaa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
