# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_per_file_ignores']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'pylint-per-file-ignores',
    'version': '1.2.0',
    'description': 'A pylint plugin to ignore error codes per file.',
    'long_description': '# Pylint Per File Ignores 😲\n\nThis pylint plugin will enable per-file-ignores in your project!\n\n## Install\n\n```\n# w/ poetry\npoetry add --dev pylint-per-file-ignores\n\n# w/ pip\npip install pylint-per-file-ignores\n```\n\n## Add to Pylint Settings\n\nEdit your `pyproject.toml`:\n\n```\n[tool.pylint.MASTER]\nload-plugins=[\n    "pylint_per_file_ignores",\n    ...\n]\n```\n\n\n## Usage\n\nAdd a section to your `pyproject.toml` with the patterns and codes you would like to ignore.\n\n```\n[tool.pylint-per-file-ignores]\n"/folder_1/"="missing-function-docstring,W0621,W0240,C0115"\n"file.py"="C0116,E0001"\n```\n\n## Thanks\n\nTo pylint :) And the plugin `pylint-django` who produced most of the complex code.\n\n## Contributing\n\nThis repo uses commitizen and semantic release. Please commit using `npm run commit` .\n',
    'author': 'Christopher Pickering',
    'author_email': 'christopher@going.bg',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/christopherpickering/pylint-per-file-ignores.git',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
