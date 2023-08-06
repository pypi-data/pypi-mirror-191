# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['alpineer']

package_data = \
{'': ['*']}

install_requires = \
['charset-normalizer>=2.1.1,<3.0.0',
 'matplotlib>=3,<4',
 'natsort>=8,<9',
 'numpy>=1.0.0,<2.0.0',
 'pillow>=9,<10',
 'scikit-image<1.0.0',
 'tifffile',
 'xarray',
 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'alpineer',
    'version': '0.1.5',
    'description': 'Toolbox for Multiplexed Imaging. Contains scripts and little tools which are used throughout ark-analysis, mibi-bin-tools, and toffy.',
    'long_description': "# Alpineer\n\nToolbox for Multiplexed Imaging. Contains scripts and little tools which are used throughout [ark-analysis](https://github.com/angelolab/ark-analysis), [mibi-bin-tools](https://github.com/angelolab/mibi-bin-tools), and [toffy](https://github.com/angelolab/toffy)\n\n- [alpineer](#alpineer)\n  - [Requirements](#requirements)\n  - [Setup](#setup)\n  - [Development Notes](#development-notes)\n  - [Questions?](#questions)\n\n## Requirements\n\n* [Python Poetry](https://python-poetry.org)\n  * Recommeded to install it with either:\n    * [**Official Installer:**](https://python-poetry.org/docs/master/#installing-with-the-official-installer)\n        ```sh\n        curl -sSL https://install.python-poetry.org | python3 -\n        ```\n    * [**pipx**](https://python-poetry.org/docs/master/#installing-with-pipx), (requires [`pipx`](https://pypa.github.io/pipx/))\n      * If you are using `pipx`, run the following installation commands\n        ```sh\n        brew install pipx\n        pipx ensurepath\n        ```\n* [pre-commit](https://pre-commit.com)\n    ```sh\n    brew isntall pre-commit\n    ```\n\n## Setup\n\n1. Clone the repo: `git clone https://github.com/angelolab/alpineer.git`\n2. `cd` into `alpineer`.\n3. Install the pre-commit hooks with `pre-commit install`\n4. Set up `python-poetry` for `alpineer`\n   1. Run `poetry install` to install `alpineer` into your virtual environment. (Poetry utilizes [Python's Virtual Environments](https://docs.python.org/3/tutorial/venv.html))\n   2. Run `poetry install --with test`: Installs all the [dependencies needed for tests](pyproject.toml) (labeled under `tool.poetry.group.test.dependencies`)\n   3. Run `poetry install --with dev`: Installs all the [dependencies needed for development](pyproject.coml) (labeled under `tool.poetry.group.dev.dependencies`)\n   4. You may combine these as well with `poetry install --with dev,test`. Installing the base dependencies and the two optional groups.\n5. In order to test to see if Poetry is working properly, run `poetry show --tree`. This will output the dependency tree for the base dependencies (labeled under `tool.poetry.dependencies`).\n\n    Sample Output:\n\n   ```sh\n   matplotlib 3.6.1 Python plotting package\n   ├── contourpy >=1.0.1\n   │   └── numpy >=1.16\n   ├── cycler >=0.10\n   ├── fonttools >=4.22.0\n   ├── kiwisolver >=1.0.1\n   ├── numpy >=1.19\n   ├── packaging >=20.0\n   │   └── pyparsing >=2.0.2,<3.0.5 || >3.0.5\n   ├── pillow >=6.2.0\n   ├── pyparsing >=2.2.1\n   ├── python-dateutil >=2.7\n   │   └── six >=1.5\n   └── setuptools-scm >=7\n       ├── packaging >=20.0\n       │   └── pyparsing >=2.0.2,<3.0.5 || >3.0.5\n       ├── setuptools *\n       ├── tomli >=1.0.0\n       └── typing-extensions *\n   natsort 8.2.0 Simple yet flexible natural sorting in Python.\n   numpy 1.23.4 NumPy is the fundamental package for array computing with Python.\n   pillow 9.1.1 Python Imaging Library (Fork)\n   pip 22.3 The PyPA recommended tool for installing Python packages.\n   tifffile 2022.10.10 Read and write TIFF files\n   └── numpy >=1.19.2\n   ```\n\n\n## Development Notes\n\n1. I'd highly suggest refering to Poetry's extensive documentation on [installing packages](https://python-poetry.org/docs/master/cli/#add), [updating packages](https://python-poetry.org/docs/master/cli/#update) and more.\n2. Tests can be ran with `poetry run pytest`. No additional arguments needed, they are all stored in the [`pyproject.toml`](pyproject.toml) file.\n   1. As an aside, if you need to execute code in the poetry venv, use prefix your command with [`poetry run`](https://python-poetry.org/docs/master/cli/#run)\n\n## Updating\n\n* In order to update `alpineer`'s dependencies we can run:\n  *  `poetry update`: for all dependencies\n  *  `poetry update <package>`: where `<package>` can be something like `numpy`.\n* To update Poetry itself, run `poetry self update`.\n## Questions?\n\nFeel free to open an issue on our [GitHub page](https://github.com/angelolab/alpineer/issues)\n",
    'author': 'Noah Frey Greenwald',
    'author_email': 'nfgreen@stanford.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/angelolab/tmi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
