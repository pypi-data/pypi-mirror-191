# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fxtracker']

package_data = \
{'': ['*']}

install_requires = \
['altair-viewer>=0.4.0,<0.5.0',
 'altair>=4.2.0,<5.0.0',
 'ipykernel>=6.20.2,<7.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.12.0,<6.0.0',
 'python-semantic-release>=7.33.0,<8.0.0',
 'yfinance>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'fxtracker',
    'version': '1.0.2',
    'description': 'A package that plots current and historical price graphs for currency pairs as well as converts currency.',
    'long_description': '[![ci-cd](https://github.com/UBC-MDS/fxtracker/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/UBC-MDS/fxtracker/actions/workflows/ci-cd.yml) [![codecov](https://codecov.io/gh/UBC-MDS/fxtracker/branch/main/graph/badge.svg?token=N4sBOXKB87)](https://codecov.io/gh/UBC-MDS/fxtracker) [![Documentation Status](https://readthedocs.org/projects/fxtracker/badge/?version=latest)](https://fxtracker.readthedocs.io/en/latest/?badge=latest)\n\n# fxtracker\n\nThis is a package created as a group project for DSCI_524 Collaborative Software Development of UBC Master of Data Science (MDS) program 2022-2023. Based on the foreign exchange data in Yahoo Finance, this package allows user to perform currency conversion based on the latest available exchange rate, lookup a target exchange rate from historical data as well plotting exchange rate history and profit/loss percentage history by specifying a currency pair (and other input parameters).\n\nThe full documentation of this package can also be found on <https://fxtracker.readthedocs.io/en/latest/>\n\n## Function Description\n\n-   `fx_conversion` <br> Convert the input amount of currency 1 to currency 2 based on the latest available exchange rate.\n-   `fx_rate_lookup` <br> Lookup for the most recent date on which the input target rate of a currency pair is within the day\'s high/low.\n-   `price_trend_viz` <br> Plot the historical exchange rate of the input currency pair for a specific period of time.\n-   `pl_trend_viz` <br> Plot the historical profit/loss percentage of the input currency pair for a specific period of time.\n\nThere is a python package ([`forex-python`](https://pypi.org/project/forex-python/)) relevant to foreign exchange. That package is basically for retrieving exchange rates and bitcoin prices in plain text as well as performing conversion. It does not provide visualizations and lookup function like `fxtracker` does. `fxtracker` allows user to visualize the trends and understand if a target price of a currency pair of interest is within a reasonable range.\n\n## Installation\n\n```bash\n$ pip install fxtracker\n```\n\n## Usage\n\nIf the package is installed successfully, users then need the following nine input parameters:\n\n`curr`, `target_px`, `start_date`, `end_date`, `chart_type`, `option`, `curr1`, `curr2`, `amt`. The output of the functions will be in forms of a datetime string, a float and interactive plots from the "altair" package.\n\n`fxtracker` can be used to convert a specific amount of money from one currency to another, find the most recent date on which the target price falling between day high and day low of that day, visualize the trend of the exchange rate of a currency pair and the trend of the profit and loss of a currency pair between the selected start date and end date.\n\nThe functions can be imported from the package as follows:\n\n```python\nfrom fxtracker.fxtracker import fx_conversion\nfrom fxtracker.fxtracker import fx_rate_lookup\nfrom fxtracker.fxtracker import price_trend_viz\nfrom fxtracker.fxtracker import pl_trend_viz\n```\n\n### To convert a specific amount of money from current currency (curr1) to desired currency (curr2):\n\n    fx_conversion(\'EUR\', \'USD\', 150.75)\n\n163.68\n\n### To look up the most recent date on which the target price falling between day high and day low of that day:\n\n    fx_rate_lookup(\'EURUSD\', 1.072)\n\n\'2023-01-10\'\n\n### To visualize the trend of the exchange rate of a currency pair between the selected start date and end date:\n\n    price_trend_viz(\'EURUSD\', \'2018-12-01\', \'2022-12-01\', \'High\').show()\n\n![](https://user-images.githubusercontent.com/112665905/215251534-3d452198-23bc-4b42-885c-d76a5ca68f25.png)\n\n### To visualize the trend of the profit and loss of a currency pair between the selected start date and end date:\n\n**If a line chart is specified in the input:**\n\n    pl_trend_viz("EURUSD", "2020-01-01", "2022-01-01", \'line\').show()\n\n![](https://user-images.githubusercontent.com/112665905/215251530-8a3cf86f-6854-47b5-b7b4-2ff214e88217.png)\n\n**If an area chart is specified in the input:**\n\n    pl_trend_viz("EURUSD", "2020-01-01", "2022-01-01", \'area\').show()\n\n![](https://user-images.githubusercontent.com/112665905/215251527-3381d5de-c776-4b5f-9777-c687b287f089.png)\n\n## Dependencies\n\n-   python = "\\^3.9"\n-   pandas = "\\^1.5.2"\n-   altair = "\\^4.2.0"\n-   numpy = "\\^1.24.1"\n-   plotly = "\\^5.12.0"\n-   yfinance = "\\^0.2.3"\n-   ipykernel = "\\^6.20.2"\n-   altair-viewer = "\\^0.4.0"\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`fxtracker` was created by Sarah Abdelazim, Markus Nam, Crystal Geng and Lennon Au-Yeung. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`fxtracker` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n```python\n\n```\n',
    'author': 'Sarah Abdelazim, Markus Nam, Crystal Geng, Lennon Au-Yeung',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UBC-MDS/fxtracker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
