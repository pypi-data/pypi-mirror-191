# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3head']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.69,<2.0.0', 'click>=8.1.3,<9.0.0', 'smart-open>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['s3head = s3head.main:main']}

setup_kwargs = {
    'name': 's3head',
    'version': '0.1.1',
    'description': 'head command for AWS S3 objects',
    'long_description': "[![PyPI version](https://badge.fury.io/py/s3head.svg)](https://badge.fury.io/py/s3head)\n[![Python Versions](https://img.shields.io/pypi/pyversions/s3head.svg)](https://pypi.org/project/s3head/)\n# s3head\n\n`s3head` is the `head` command for AWS S3.\n\n## Install\n```\npip install s3head\n```\nIf you use pipx, it's nice to install by it.\n\n```\npipx iinstall s3head\n```\n## Usage\nBefore using, create `.s3cfg` file by `s3cmd --configure`. See [s3cmd](https://github.com/s3tools/s3cmd)\n```\nUsage: s3head [OPTIONS] URI\n\nOptions:\n  -n, --num-lines INTEGER   lines\n  -c, --count-byte INTEGER  bytes\n  --config TEXT             Path to the `.s3cfg`\n  --help                    Show this message and exit.\n```\n\nFor example,\n```\ns3head -n 100 s3://your_bucket/your_file.txt\n```",
    'author': 'Kenta Shinzato',
    'author_email': 'hoppiece@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hoppiece/s3head',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
