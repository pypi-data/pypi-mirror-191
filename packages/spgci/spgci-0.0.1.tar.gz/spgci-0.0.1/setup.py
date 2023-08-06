# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spgci']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'retry>=0.9.2,<0.10.0',
 'tqdm>=4.64.1,<5.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'spgci',
    'version': '0.0.1',
    'description': 'SPGCI is an API Client for the S&P Commodity Insights REST API',
    'long_description': '# SPGCI\n\nPython Client for the [S&P Global Commodity Insights API](https://developer.platts.com).\n\n## Installation\n\nRequires Python >= 3.8.10.\n\n```bash\npip install spgci\n```\n\n## Getting Started\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/achristie/images/blob/master/readme.ipynb)\n\n```python\n    import spgci as ci\n\n    ci.set_credentials(<username>, <password>, <appkey>)\n    mdd = ci.MarketData()\n\n    symbols = ["PCAAS00", "PCAAT00"]\n    mdd.get_assessments_by_symbol_current(symbol=symbols)\n```\n\n## ![image](https://raw.githubusercontent.com/achristie/images/master/getting_started.gif)\n\n---\n\nAlternatively, you can set your credentials via Environment Variables and _omit_ the `set_credentials` call:\n| Environment Variable | Description |\n| :------------------- | :----------------|\n| SPGCI_USERNAME | Your Username |\n| SPGCI_PASSWORD | Your Password |\n| SPGCI_APPKEY | Your AppKey |\n\n## Features\n\n- Automatically generates token prior to making request.\n- Returns response as a pandas `DataFrame` (set `raw=False` to disable).\n- Automatically paginates response and concatenates in a single `DataFrame` (set `paginate=False` to disable).\n- Sets datatype for `date` and `datetime` fields.\n- Methods support familiar Python data type and convert to filter expressions.\n\n## Datasets Supported\n\n### Market Data\n\n```python\nimport spgci as ci\n\nmdd = ci.MarketData()\n\nmdd.get_symbols(commodity="Crude oil")\n# DataFrame of symbols with commodity = "Crude oil"\n\nmdd.get_mdcs(subscribed_only=True)\n# DataFrame of all Market Data Categories you are subscribed to\n\nmdd.get_assessments_by_mdc_current(mdc="ET")\n# DataFrame of current assessments for all symbols in the Market Data Category "ET"\n```\n\n### Forward Curves\n\n```python\nimport spgci as ci\n\nfc = ci.ForwardCurves()\n\nfc.get_curves(\n    commodity=["Benzene", "Crude oil"],\n    derivative_maturity_frequency="Month"\n    )\n# DataFrame of all curves with commodity in ("Benzene", "Crude Oil") and have a Monthly frequency\n\nfc.get_assessments(curve_code=["CN003", "CN006"])\n# DataFrame of the latest assessments for all symbols in the curves ("CN003", "CN006")\n```\n\n### EWindow Market Data\n\n```python\nimport spgci as ci\nfrom datetime import date\n\newmd = ci.EWindowMarketData()\n\newmd.get_markets()\n# DataFrame of Markets\n\nd = date(2023,2,13)\newmd.get_botes(market=["EU BFOE", "US MidWest"], order_time=d)\n# DataFrame of all BOTes in the markets ("EU BFOE", "US MidWest") on Feb 13, 2023\n\n```\n\n## Disclaimer\n\nPlease note that by using this Alpha offering, you agree that you are participating in a prototype to develop these software development kits (“Alpha SDKs”) and that your participation and use of the Alpha SDKs is at your own risk. You will be liable for all activities by anyone using your application in connection with the Alpha SDKs.\n\nIf you are dissatisfied with the Alpha SDKs, your sole remedy is to stop using it, and S&P Global Commodity Insights (“SPGCI”) will not pay you any damages (direct, indirect, special, or consequential) in connection with your use of the Alpha SDKs. Commodity Insights SPGCI disclaims any and all representations and warranties, express or implied, including but not limited to any warranties of merchantability or fitness for a particular purpose or use as to the Alpha SDKs, and does not guarantee the adequacy, accuracy, timeliness or completeness of the Alpha SDKs or any component of them.\n',
    'author': 'S&P Global Commodity Insights',
    'author_email': 'pl_api_support@spglobal.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
