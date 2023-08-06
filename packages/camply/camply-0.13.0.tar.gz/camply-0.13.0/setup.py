# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camply',
 'camply.config',
 'camply.containers',
 'camply.notifications',
 'camply.providers',
 'camply.providers.going_to_camp',
 'camply.providers.recreation_dot_gov',
 'camply.providers.reserve_california',
 'camply.providers.xanterra',
 'camply.search',
 'camply.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<7.0',
 'click>=8.0.1',
 'fake-useragent>=1.1.1,<2.0.0',
 'pandas>=1.3,<1.4',
 'pydantic>=1.2,<2.0',
 'python-dotenv>=0.10.4',
 'pytz>=2019.1',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.26.0',
 'rich-click>=1.6.1,<2.0.0',
 'rich>=10.0.0',
 'tenacity>=5.1.0']

extras_require = \
{'all': ['twilio>=7.14.0'], 'twilio': ['twilio>=7.14.0']}

entry_points = \
{'console_scripts': ['camply = camply.cli:cli']}

setup_kwargs = {
    'name': 'camply',
    'version': '0.13.0',
    'description': 'camply, the campsite finder 🏕',
    'long_description': '<div align="center">\n<a href="https://github.com/juftin/camply">\n  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"\n    width="400" height="400" alt="camply">\n</a>\n</div>\n\n**`camply`**, the campsite finder ⛺️, is a tool to help you book a campground online. Finding\nreservations at sold out campgrounds can be tough. That\'s where camply comes in. It searches the\nAPIs of booking services like https://recreation.gov (which indexes thousands of campgrounds across\nthe USA) to continuously check for cancellations and availabilities to pop up. Once a campsite\nbecomes available, camply sends you a notification to book your spot!\n\n---\n\n---\n\n[![PyPI](https://img.shields.io/pypi/v/camply?color=blue&label=⛺️camply)](https://github.com/juftin/camply)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camply)](https://pypi.python.org/pypi/camply/)\n[![Docker Image Version](https://img.shields.io/docker/v/juftin/camply?color=blue&label=docker&logo=docker)](https://hub.docker.com/r/juftin/camply)\n[![Testing Status](https://github.com/juftin/camply/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/juftin/camply/actions/workflows/tests.yaml)\n[![GitHub License](https://img.shields.io/github/license/juftin/camply?color=blue&label=License)](https://github.com/juftin/camply/blob/main/LICENSE)\n[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)\n[![Discord Chat](https://img.shields.io/static/v1?label=chat&message=discord&color=blue&logo=discord)](https://discord.gg/qZDr78kKvB)\n\n## [Check Out The Docs](https://juftin.com/camply/)\n\n## Installing\n\nInstall camply via `pip` or [pipx](https://github.com/pypa/pipx):\n\n```commandline\npipx install camply\n```\n\n## Usage\n\nSearch for a specific recreation area (recreation areas contain campgrounds):\n\n```commandline\ncamply recreation-areas --search "Glacier National Park"\n```\n\nSearch for campgrounds (campgrounds contain campsites):\n\n```commandline\ncamply campgrounds --search "Fire Lookout Towers" --state CA\n```\n\nSearch for available campsites, get a notification whenever one becomes\navailable, and continue searching after the first one is found. The below command\nis using `silent` notifications as an example but camply also supports `Email`,\n`Slack`, `Twilio` (SMS), `Pushover`, `Pushbullet`, and `Telegram`.\n\n```commandline\ncamply campsites \\\n    --rec-area 2725 \\\n    --start-date 2023-07-10 \\\n    --end-date 2023-07-18 \\\n    --notifications silent \\\n    --search-forever\n```\n\n## Providers\n\ncamply works with a number of providers. A "provider" is an online booking\nservice that lists camping and recreation inventory.\n\n-   **`RecreationDotGov`**: Searches on [Recreation.gov](https://recreation.gov) for Campsites (default provider)\n-   **`Yellowstone`**: Searches on [YellowstoneNationalParkLodges.com](https://yellowstonenationalparklodges.com) for Campsites\n-   **`GoingToCamp`**: Searches on [GoingToCamp.com](https://goingtocamp.com) for Campsites\n-   **`ReserveCalifornia`**: Searches on [ReserveCalifornia.com](https://reservecalifornia.com) for Campsites\n-   **`RecreationDotGovTicket`**: Searches on [Recreation.gov](https://recreation.gov) for Tickets and Tours\n-   **`RecreationDotGovTimedEntry`**: Searches on [Recreation.gov](https://recreation.gov) for Timed Entries\n\nRun **`camply providers`** to list current providers and visit the [Providers](https://juftin.com/camply/providers/)\nsection in the docs to learn more.\n\n## Documentation\n\nHead over to the [camply documentation](https://juftin.com/camply/) to see what you can do!\n\n```console\n❯ camply --help\n\n Usage: camply [OPTIONS] COMMAND [ARGS]...\n\n Welcome to camply, the campsite finder.\n Finding reservations at sold out campgrounds can be tough. That\'s where camply comes in.\n It searches the APIs of booking services like https://recreation.gov (which indexes\n thousands of campgrounds across the USA) to continuously check for cancellations and\n availabilities to pop up. Once a campsite becomes available, camply sends you a\n notification to book your spot!\n\n\n visit the camply documentation at https://juftin.com/camply\n\n╭─ Options ──────────────────────────────────────────────────────────────────────────────╮\n│                                                                                        │\n│  --version                      Show the version and exit.                             │\n│  --debug/--no-debug             Enable extra debugging output                          │\n│  --provider              TEXT   Camping Search Provider. Defaults to                   │\n│                                 \'RecreationDotGov\'                                     │\n│  --help                         Show this message and exit.                            │\n│                                                                                        │\n╰────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ─────────────────────────────────────────────────────────────────────────────╮\n│                                                                                        │\n│  campgrounds        Search for Campgrounds (inside of Recreation Areas) and list them  │\n│  campsites          Find Available Campsites with Custom Search Criteria               │\n│  configure          Set up camply configuration file with an interactive console       │\n│  equipment-types    Get a list of supported equipment                                  │\n│  providers          List the different camply providers                                │\n│  recreation-areas   Search for Recreation Areas and list them                          │\n│                                                                                        │\n╰────────────────────────────────────────────────────────────────────────────────────────╯\n\n```\n\n## Contributing\n\nCamply doesn\'t support your favorite campsite booking provider yet? Consider\n[contributing](https://juftin.com/camply/contributing/) 😉.\n\n<br/>\n\nRecreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)\n\n---\n\n---\n\n<br/>\n\n[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)\n',
    'author': 'Justin Flannery',
    'author_email': 'juftin@juftin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juftin/camply',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
