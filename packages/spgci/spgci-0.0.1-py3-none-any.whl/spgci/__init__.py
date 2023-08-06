"""
S&P Global Commodity Insights API\n
More details available here: https://developer.platts.com

Getting Started
---------------
>>> import spgci as ci
>>> ci.set_credentials(``username``, ``password``, ``appkey``)
>>> ci.MarketData().get_assessments_by_symbol(symbol="PCAAS00")
\n
"""

from .market_data import MarketData
from .forward_curves import ForwardCurves
from .ewindow_md import EWindowMarketData
from .api_client import get_token
from .types import *

from .config import username, password, set_credentials, appkey, version

__version__ = version


__all__ = [
    "MarketData",
    "username",
    "password",
    "appkey",
    "set_credentials",
    "ForwardCurves",
    "EWindowMarketData",
    "get_token",
]
