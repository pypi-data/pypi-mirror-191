# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orion', 'orion.types', 'orion.utils']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.12.2,<0.13.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.28.0,<3.0.0',
 'shapely>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'orion-nais',
    'version': '0.1.0',
    'description': 'A client for the NAIS API from FThe Norwegian Coastal Administration',
    'long_description': '# Orion-NAIS\n\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#requirements">Requirements</a></li>\n        <li><a href="#structure">Structure</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n    <li><a href="#contributing">Contributing</a></li>\n    <li><a href="#contact">Contact</a></li>\n  </ol>\n</details>\n\n<!-- ABOUT THE PROJECT -->\n\n## About The Project\n\nOrion-NAIS is a client to work with the NAIS API. It helps with authentication and provides a simple interface to work with the API.\n\nWhen working with the API you need to have a valid token. The token is valid for a set period of time. The client will automatically refresh the token when it expires.\n\n### Why the name Orion?\n\nThe NAIS Api is provided through BarentsWatch. BarentsWatch is a Norwegian information portal that provides overview of activity and knowledge in coastal and sea areas. The Norwegian movie "Orion\'s Belt" from 1985 is an action movie set in the Barents region. About three men, a bulldozer, a Russian helicopter and a ship. Thus the name Orion.\n\n## Installation\n\nRequires Python 3.10 or later.\n\n```bash\n\npip install orion-nais\n\n```\n\nor using pipenv:\n\n```bash\n\npipenv install orion-nais\n\n```\n\nor using poetry:\n\n```bash\npoetry add orion-nais\n```\n\n## Usage\n\nThere are a heap of functions for you to use. Enjoy.\n\n## Local development\n\n### Requirements\n---\n\n- pyenv - manage python versions\n- poetry - manage python dependencies\n\nTo install on mac you can use homebrew:\n\n```bash\nbrew upgrade\nbrew install pyenv\n```\n\nYou can either install poetry with homebrew or the way described in the [documentation](https://python-poetry.org/docs/#installation)\n\n\n### Makefile commands\n\n- `make lint`\n  - lint the code in the src folder with black, isort and flake8. Mypy will check for correct typing.\n- `make format`\n  - format the code in the src folder with black and isort.\n\n### Structure\n\n```\n.\n├── .bumpversion.cfg\n├── .editorconfig\n├── .flake8\n├── .gitignore\n├── Makefile\n├── README.md\n├── orion\n│   ├── client.py\n│   ├── mmsi.py\n│   ├── types\n│   │   └── ais.py\n│   ├── urls.py\n│   ├── utils\n│   │   └── get_data.py\n│   └── vessel_codes.py\n├── poetry.lock\n├── pyproject.toml\n└── tests\n    ├── make_mock_data.py\n    ├── mocks\n    └── test_orion.py\n    \n```\n\n- `.bumpversion.cfg`\n  - Configuration file for bumpversion.\n- `.editorconfig`\n  - Configuration file for editorconfig.\n- `.flake8`\n  - Configuration file for flake8.\n- `.gitignore`\n  - Configuration file for git.\n- `pyproject.toml`\n  - Configuration file for poetry. Mypy and isort is configured here.\n- `poetry.lock`\n  - Lock file for poetry.\n- `Makefile`\n  - Makefile for the project. Here you can find commands for linting and formatting.\n- `README.md`\n  - This file.\n- `orion`\n  - The source code for the package.\n  - `client.py`\n    - The client class.\n  - `mmsi.py`\n    - A dataclass for handling MMSI numbers and MID-codes (jurisdiction).\n  - `types`\n    - A folder for types.\n    - `ais.py`\n      - A class for handling AIS messages.\n  - `urls.py`\n    - A file with urls for the API.\n  - `utils`\n    - A folder for utility functions.\n    - `get_data.py`\n      - A function for getting data from other sources. Not used by the Orion client. Contains code for getting data from the Norwegian Petroleum Directorate.\n  - `vessel_codes.py`\n    - A dataclass for looking up vessel codes.\n- `tests`\n  - Tests for the package.\n\n## Usage\n\nTo install the package in your project run\n\n```bash\n\npoetry add orion-nais\n```\n\n## Contributing\n\nDo you have write permissions to the repo? Then you can clone this project to a folder on your computer.\n\n```bash\ngit clone https://github.com/BergensTidende/orion-nais.git\n```\n\nIf not do the following:\n\n- Create a personal fork of the project on Github.\n- Clone the fork on your local machine. Your remote repo on Github is called `origin`.\n- Add the original repository as a remote called `upstream`.\n- If you created your fork a while ago be sure to pull upstream changes into your local repository.\n\nThis will clone the repo into `pakkenellik`. \n\nCreate a branch for your changes\n\n```bash\ngit checkout -b name-of-branch\n```\n\nMake your changes, rememeber to commit. And always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.\n\nIf you\'re working on a clone push the branch to github and make PR.\n\nIf your\'re working a fork:\n\n- Squash your commits into a single commit with git\'s [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.\n- Push your branch to your fork on Github, the remote `origin`.\n- From your fork open a pull request in the correct branch. Target the project\'s `develop` branch if there is one, else go for `master`!\n- …\n- If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.\n- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete\n  your extra branch(es).\n\n <!-- CONTACT -->\n\n## Contact\n\nBord4 - bord4@bt.no\n',
    'author': 'Lasse Lambrechts',
    'author_email': 'lasse.lambrechts@bt.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
