# SPGCI

Python Client for the [S&P Global Commodity Insights API](https://developer.platts.com).

## Installation

Requires Python >= 3.8.10.

```bash
pip install spgci
```

## Getting Started

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/achristie/images/blob/master/readme.ipynb)

```python
    import spgci as ci

    ci.set_credentials(<username>, <password>, <appkey>)
    mdd = ci.MarketData()

    symbols = ["PCAAS00", "PCAAT00"]
    mdd.get_assessments_by_symbol_current(symbol=symbols)
```

## ![image](https://raw.githubusercontent.com/achristie/images/master/getting_started.gif)

---

Alternatively, you can set your credentials via Environment Variables and _omit_ the `set_credentials` call:
| Environment Variable | Description |
| :------------------- | :----------------|
| SPGCI_USERNAME | Your Username |
| SPGCI_PASSWORD | Your Password |
| SPGCI_APPKEY | Your AppKey |

## Features

- Automatically generates token prior to making request.
- Returns response as a pandas `DataFrame` (set `raw=False` to disable).
- Automatically paginates response and concatenates in a single `DataFrame` (set `paginate=False` to disable).
- Sets datatype for `date` and `datetime` fields.
- Methods support familiar Python data type and convert to filter expressions.

## Datasets Supported

### Market Data

```python
import spgci as ci

mdd = ci.MarketData()

mdd.get_symbols(commodity="Crude oil")
# DataFrame of symbols with commodity = "Crude oil"

mdd.get_mdcs(subscribed_only=True)
# DataFrame of all Market Data Categories you are subscribed to

mdd.get_assessments_by_mdc_current(mdc="ET")
# DataFrame of current assessments for all symbols in the Market Data Category "ET"
```

### Forward Curves

```python
import spgci as ci

fc = ci.ForwardCurves()

fc.get_curves(
    commodity=["Benzene", "Crude oil"],
    derivative_maturity_frequency="Month"
    )
# DataFrame of all curves with commodity in ("Benzene", "Crude Oil") and have a Monthly frequency

fc.get_assessments(curve_code=["CN003", "CN006"])
# DataFrame of the latest assessments for all symbols in the curves ("CN003", "CN006")
```

### EWindow Market Data

```python
import spgci as ci
from datetime import date

ewmd = ci.EWindowMarketData()

ewmd.get_markets()
# DataFrame of Markets

d = date(2023,2,13)
ewmd.get_botes(market=["EU BFOE", "US MidWest"], order_time=d)
# DataFrame of all BOTes in the markets ("EU BFOE", "US MidWest") on Feb 13, 2023

```

## Disclaimer

Please note that by using this Alpha offering, you agree that you are participating in a prototype to develop these software development kits (“Alpha SDKs”) and that your participation and use of the Alpha SDKs is at your own risk. You will be liable for all activities by anyone using your application in connection with the Alpha SDKs.

If you are dissatisfied with the Alpha SDKs, your sole remedy is to stop using it, and S&P Global Commodity Insights (“SPGCI”) will not pay you any damages (direct, indirect, special, or consequential) in connection with your use of the Alpha SDKs. Commodity Insights SPGCI disclaims any and all representations and warranties, express or implied, including but not limited to any warranties of merchantability or fitness for a particular purpose or use as to the Alpha SDKs, and does not guarantee the adequacy, accuracy, timeliness or completeness of the Alpha SDKs or any component of them.
