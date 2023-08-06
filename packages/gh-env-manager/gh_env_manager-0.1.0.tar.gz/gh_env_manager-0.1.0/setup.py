# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gh_env_manager']

package_data = \
{'': ['*']}

install_requires = \
['pynacl>=1.5.0,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gh-env-manager = gh_env_manager.main:app']}

setup_kwargs = {
    'name': 'gh-env-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': '# GitHub Environment Manager - `gh_env_manager`\n\n![Python](https://img.shields.io/badge/python-3.9%20-blue)\n![Pytest coverage](./.github/badges/coverage.svg)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Antvirf_gh-environment-manager&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Antvirf_gh-environment-manager)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Antvirf_gh-environment-manager&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Antvirf_gh-environment-manager)\n\n## Installation (coming soon!)\n\n<!-- \n```bash\npip install gh-env-manager\n``` -->\n\n---\n\n## Usage\n\n`PATH_TO_FILE` is always required for each command.\n\n```bash\n$ gh_env_manager [COMMANDS] PATH_TO_FILE [OPTIONS]\n\n# examples\n$ gh_env_manager read .env.yaml\n$ gh_env_manager fetch .env.yaml\n$ gh_env_manager update .env.yaml\n```\n\n### Commands\n\n* `read`:    Read given YAML file and output the interpreted contents.\n* `fetch`:   Fetch all secrets and all variables from the specific GitHub repositories provided in your environment YAML file.\n* `update`:  Update secrets and variables of the GitHub repositories using data from the provided YAML file. By default, existing secrets or variables are NOT overwritten. Try `gh-env-manager update --help` to view the available options.\n\n### Options for `update`\n\n* `-o, --overwrite`: If enabled, overwrite existing secrets and values in GitHub to match the provided YAML file.  [default: False]\n* `-d, --delete-nonexisting`: If enabled, delete secrets and variables that are not found in the provided YAML file.  [default: False]\n* `--delete-nonexisting-without-prompt`: Applies the same commands as `delete_nonexisting`, but without prompting the user for confirmation. [default: False]\n<!-- \n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit. -->\n',
    'author': 'Antti Viitala',
    'author_email': 'antti.viitala@icloud.com',
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
