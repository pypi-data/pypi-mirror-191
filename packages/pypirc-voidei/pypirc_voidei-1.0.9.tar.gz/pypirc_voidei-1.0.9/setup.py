# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypirc']

package_data = \
{'': ['*']}

install_requires = \
['prettyprinter>=0.18.0,<0.19.0']

entry_points = \
{'console_scripts': ['pypirc = pypirc.cmd:main']}

setup_kwargs = {
    'name': 'pypirc-voidei',
    'version': '1.0.9',
    'description': 'PyPiRC: .pypirc Manager',
    'long_description': '<!-- markdownlint-disable MD026 MD036-->\n\n# `.pypirc` File Management Client\n\n**"This is hopefully a temporary fork, as the official project looks dead."**\nsaid [Chappers](https://github.com/charliec443), who originally forked this project. Unfortunately, that fork is also dead.\nSo here I am. Forking it again, making it work with Python 3.10+ (no backwards compatibility).\n\nIf you want to have it work in older versions of Python, please go download the [original](https://github.com/ampledata/pypirc), or [Chapper\'s fork](https://github.com/charliec443/pypirc).\n\n## Installation\n\nInstall from [pypi](https://pypi.org) via the following:\n\n```bash\npip install pypirc-voidei\n```\n\n## Usage Example\n\nDisplay current pypi configuration:\n\n```bash\npypirc\n```\n\nAdd a pypi server:\n\n```bash\npypirc -s mypypi -u foo -p bar -r https://mypypi.example.com/\n```\n\n### Credits:\n\n#### Source\n\nOfficial: <https://github.com/ampledata/pypirc>\nChappers: <https://github.com/chappers/pypirc>\nvoidei: <https://github.com/voidei/pypirc>\n\n#### Author\n\nGreg Albrecht <gba@splunk.com>\n<http://ampledata.org/>\n\n#### Copyright\n\n```plaintext\nCopyright 2012 Splunk, Inc.\n```\n\n#### License\n\n**Apache License 2.0**\n',
    'author': 'Greg Albrecht',
    'author_email': 'gba@splunk.com',
    'maintainer': 'Dawn Walker',
    'maintainer_email': 'dawniepieuwu@gmail.com',
    'url': 'https://github.com/voidei/pypirc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4',
}


setup(**setup_kwargs)
