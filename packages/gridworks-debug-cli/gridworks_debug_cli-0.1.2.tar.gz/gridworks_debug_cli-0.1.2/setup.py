# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gwdcli', 'gwdcli.events']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.4.2,<3.0.0',
 'anyio>=3.6.2,<4.0.0',
 'asyncio-mqtt>=0.16.1,<0.17.0',
 'click>=8.0.1',
 'gridworks-protocol>=0.2.3,<0.3.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'result>=0.9.0,<0.10.0',
 'rich>=13.2.0,<14.0.0',
 'typer>=0.7.0,<0.8.0',
 'types-aiobotocore[essential]>=2.4.2,<3.0.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['gwd = gwdcli.__main__:app',
                     'gwd-events = gwdcli.events.__main__:app']}

setup_kwargs = {
    'name': 'gridworks-debug-cli',
    'version': '0.1.2',
    'description': 'Gridworks Debug Cli',
    'long_description': '# Gridworks Debug Cli\n\n[![PyPI](https://img.shields.io/pypi/v/gridworks-debug-cli.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/gridworks-debug-cli.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-debug-cli)][python version]\n[![License](https://img.shields.io/pypi/l/gridworks-debug-cli)][license]\n\n[![Read the documentation at https://gridworks-debug-cli.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-debug-cli/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/thegridelectric/gridworks-debug-cli/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/thegridelectric/gridworks-debug-cli/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/gridworks-debug-cli/\n[status]: https://pypi.org/project/gridworks-debug-cli/\n[python version]: https://pypi.org/project/gridworks-debug-cli\n[read the docs]: https://gridworks-debug-cli.readthedocs.io/\n[tests]: https://github.com/anschweitzer/gridworks-debug-cli/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/anschweitzer/gridworks-debug-cli\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nInternal debugging tools for Gridworks systems:\n\n```shell\nbrew install awscli\naws configure\npip install gridworks-debug-cli\ngwd events mkconfig\ngwd events show\n```\n\nThis tool will be maintained only as long as it is internally useful. YMMV.\n\n## Features\n\n- Event viewing, either from local directory of events or from the cloud.\n\n## Requirements\n\n- [awscli](https://aws.amazon.com/cli/). This should be installable\n  per [Amazon instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or on a\n  mac with:\n  ```shell\n  brew install awscli\n  ```\n- AWS credentials from Gridworks installed per\n  [Amazon instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) or:\n  ```shell\n  aws configure\n  ```\n\n## Installation\n\nYou can install _Gridworks Debug Cli_ via [pip] from [PyPI]:\n\nInstall awscli per per [Amazon instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)\nor on a mac with:\n\n```shell\nbrew install awscli\n```\n\nGet AWS credentials from Gridworks and install them with:\n\n```shell\naws configure\n```\n\nInstall gridworks-debug-cli with:\n\n```shell\npip install gridworks-debug-cli\n```\n\nConfigure gridworks-debug-cli with:\n\n```shell\ngwd events mkconfig\nopen $HOME/.config/gridworks/debug-cli/events/gwd.events.config.json\n```\n\nYou **must** fill in values for the following keys with information from Gridworks:\n\n```json\n{\n  "mqtt": {\n    "hostname": "USE REAL VALUE",\n    "password": "USE REAL VALUE",\n    "username": "USE REAL VALUE"\n  },\n  "sync": {\n    "s3": {\n      "bucket": "USE REAL VALUE",\n      "prefix": "USE REAL VALUE",\n      "profile": "USE NAME YOU CHOSE in \'aws configure\'"\n    }\n  }\n}\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Gridworks Debug Cli_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/anschweitzer/gridworks-debug-cli/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/anschweitzer/gridworks-debug-cli/blob/main/LICENSE\n[contributor guide]: https://github.com/anschweitzer/gridworks-debug-cli/blob/main/CONTRIBUTING.md\n[command-line reference]: https://gridworks-debug-cli.readthedocs.io/en/latest/usage.html\n',
    'author': 'Andrew Schweitzer',
    'author_email': 'schweitz72@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/anschweitzer/gridworks-debug-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
