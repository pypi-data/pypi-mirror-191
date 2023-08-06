# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kronos']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.21.0,<0.22.0', 'pytz>=2022.1,<2023.0']

setup_kwargs = {
    'name': 'kronos-daterange',
    'version': '0.0.9',
    'description': 'Kronos makes date ranges easier.',
    'long_description': '\n# Kronos\n\n\n<div align="center">\n\n[![PyPI - Version](https://img.shields.io/pypi/v/kronos-daterange.svg)](https://pypi.python.org/pypi/kronos-daterange)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kronos-daterange.svg)](https://pypi.python.org/pypi/kronos-daterange)\n[![Tests](https://github.com/nat5142/kronos/workflows/tests/badge.svg)](https://github.com/nat5142/kronos/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/nat5142/kronos/branch/main/graph/badge.svg)](https://codecov.io/gh/nat5142/kronos)\n[![Read the Docs](https://readthedocs.org/projects/nat5142-kronos/badge/)](https://kronos.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/kronos-daterange.svg)](https://pypi.python.org/pypi/kronos-daterange)\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n</div>\n\n\nKronos makes dateranges easier.\n\n\n* GitHub repo: <https://github.com/nat5142/kronos.git>\n* Documentation: <https://nat5142-kronos.readthedocs.io/>\n* Free software: BSD\n\n<br>\n\n## Quickstart\n---\n\nInstall from pip:\n\n```shell\npip install kronos-daterange\n```\n\nImport & basic init:\n```python\nfrom kronos import Kronos\n\nkronos = Kronos(start_date=\'2022-01-01\', end_date=\'2022-01-31\')\n```\n\n<br>\n\n## Feature Demo\n---\n\n```python\n# import\nfrom kronos import Kronos\n\n# init --> defaults to range of <yesterday, today> unless otherwise specified by `KRONOS_DATERANGE` environment variable\nkronos = Kronos()\n\n# manually set dates\nkronos = Kronos(start_date=\'2022-10-17\', end_date=\'2022-10-23\')\n\n# set timezone\nkronos = Kronos(timezone=\'America/New_York\') \n\n# specify date format\nkronos = Kronos(start_date=\'10/20/2022\', end_date=\'10/31/2022\', date_format=\'%m/%d/%Y\')\n\n# access start, end dates\nkronos = Kronos()\nkronos.start_date\n# 2022-10-19\nkronos.end_date\n# 2022-10-20\n\n# `date_format` carries over to properties:\nkronos = Kronos(date_format=\'%m/%d/%Y\')\nkronos.start_date\n# 10/19/2022\nkronos.end_date\n# 10/20/2022\n\n# format start and end date with new format\nkronos.format_start(\'%Y-%m-%d %H:%M:%S\')\n# 2022-10-20 00:00:00\nkronos.format_end(\'%Y-%m-%d %H:%M:%S\')\n# 2022-10-21 23:59:59\n\n# get the current date in specified timezone\nkronos = Kronos(\'America/Los_Angeles\')\nkronos.current_date\n# 2022-10-20\nkronos = Kronos(\'America/Los_Angeles\', date_format=\'%m/%d/%Y\')\nkronos.current_date\n# 10/20/2022\n\n# overwrite your object\'s timezone without altering the time\nkronos = Kronos(timezone=\'UTC\')\nkronos.change_timezone(tz=\'America/New_York\')\n\n# relative shift forward/back\nkronos = Kronos()\nkronos.shift_range(weeks=-1)  # pipes kwargs into timedelta\n# Kronos(start_date=\'2022-10-12\', end_date=\'2022-10-13\', ... )\n```\n\n<br>\n\n## Defaults/Environment Variables\n---\n\nKronos is prepared to accept the following environment variables:\n\n- `KRONOS_TIMEZONE`, which defaults to UTC if not set. Can often be overridden at method-levels for one-off timezone conversions.\n- `KRONOS_FORMAT`, the strptime date format string for your dates.\n- `KRONOS_DATERANGE` (see below)\n\nNote that both `KRONOS_TIMEZONE` and `KRONOS_FORMAT` can be set during init as `timezone=` and `date_format=` arguments, respectively.\n\n### `KRONOS_TIMEZONE`:\n\nCan be any valid timezone name (find them at `pytz.all_timezones`)\n\n### `KRONOS_DATERANGE`:\n\nList of accepted values:\n\n- `LATEST`: start/end dates of yesterady/today\n- `YESTERDAY_TODAY`: same as `LATEST`\n- `LAST_MONTH`: previous calendar month\n- `MTD`: month-to-date\n- `LAST_{X}_DAYS`: relative range where end_date is today, start date is set X days behind.\n- `THIS_WEEK__{X}`: week-to-date starting on previous day of week specified by X. Valid values for X: `SUN, MON, TUES, WED, THURS, FRI, SAT`\n\n<br>\n\n## Credits\n---\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n',
    'author': 'Nick Tulli',
    'author_email': 'ntulli.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nat5142/kronos',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
