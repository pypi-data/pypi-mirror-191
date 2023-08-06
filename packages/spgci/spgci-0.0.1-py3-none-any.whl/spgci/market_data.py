from spgci.utilities import list_to_filter
from spgci.api_client import get_data, Paginator
from spgci.types import ContractType, AssessmentFrequency
from typing import List, Optional, Union
import pandas as pd
from requests import Response
from datetime import date


class MarketData:
    """
    Platts Symbols and Assessments.

    Includes
    --------
    Methods to get symbol data (such as description, currency, unit of measure)\n
    Methods to get assessment data (such as the assessment of a given symbol on a particular date)

    """

    _path = "market-data/v3/value/"
    _ref_path = "market-data/reference-data/v3/search"

    @staticmethod
    def _convert_to_df(resp: Response) -> pd.DataFrame:
        j = resp.json()
        df = pd.json_normalize(j["results"], record_path=["data"], meta="symbol")  # type: ignore

        df["assessDate"] = pd.to_datetime(df["assessDate"])  # type: ignore
        df["modDate"] = pd.to_datetime(df["modDate"])  # type: ignore

        return df

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["totalPages"]

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages=total_pages)

    @staticmethod
    def _search_to_def(resp: Response) -> pd.DataFrame:
        j = resp.json()
        df = pd.DataFrame(j["results"])
        return df

    @staticmethod
    def _ref_paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["total_pages"]

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages=total_pages)

    def get_assessments_by_symbol_current(
        self,
        *,
        symbol: Optional[Union[List[str], str]] = None,
        bate: Optional[Union[List[str], str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 10000,
        raw: bool = False,
        paginate: bool = True,
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch Current Assessments by Symbol from the Market Data API.

        See ``get_symbols()`` to search for symbol codes.\n
        See ``get_assessments_by_symbol_historical()`` to include historical assessments as well.\n

        Parameters
        ----------
        symbol : Optional[Union[List[str], str]], optional
            filter by symbol, by default None
        bate : Optional[Union[List[str], str]], optional
            filter by bate, by default None
        filter_exp : Optional[str], optional
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None
        page : int, optional
            pass-thru ``page`` query param to request a particular page of results, by default 1
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default True
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object

        Examples
        --------
        **Simple**
        >>> MarketData.get_assessments_symbol_current(symbol="PCAAS00")

        **Multiple Symbols and Bates**
        >>> MarketData.get_assessments_symbol_current(symbol=["PCAAS00", "PCAAT00"], bate=["c", "h"])
        """
        paramList: List[str] = []

        if symbol:
            paramList.append(list_to_filter("symbol", symbol))
        if bate:
            paramList.append(list_to_filter("bate", bate))

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        endpoint_path = "current/symbol"
        params = {"filter": filter_exp, "page": page, "pageSize": page_size}

        return get_data(
            path=f"{self._path}{endpoint_path}",
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            params=params,
            raw=raw,
            paginate=paginate,
        )

    def get_assessments_by_symbol_historical(
        self,
        *,
        symbol: Optional[Union[List[str], str]] = None,
        bate: Optional[Union[List[str], str]] = None,
        assess_date: Optional[date] = None,
        assess_date_lt: Optional[date] = None,
        assess_date_lte: Optional[date] = None,
        assess_date_gt: Optional[date] = None,
        assess_date_gte: Optional[date] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 10000,
        paginate: bool = True,
        raw: bool = False,
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch Historical Assessments by Symbol from the Market Data API.

        See ``get_symbols()`` to search for symbol codes.\n
        See ``get_assessments_by_symbol_current()`` for the latest assessments only.\n

        Parameters
        ----------
        symbol : Optional[Union[List[str], str]], optional
            filter by symbol, by default None
        bate : Optional[Union[List[str], str]], optional
            filter by bate, by default None
        assess_date : Optional[date], optional
            filter by ``assessDate = x`` , by default None
        assess_date_lt : Optional[date], optional
            filter by ``assessDate < x``, by default None
        assess_date_lte : Optional[date], optional
            filter by ``assessDate <= x``, by default None
        assess_date_gt : Optional[date], optional
            filter by ``assessDate > x``, by default None
        assess_date_gte : Optional[date], optional
            filter by ``assessDate >= x``, by default None
        filter_exp : Optional[str], optional
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None
        page : int, optional
            pass-thru ``page`` query param to request a particular page of results, by default 1
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default True
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object

        Examples
        --------
        **Simple**
        >>> MarketData.get_assessments_symbol_historical(symbol="PCAAS00")

        **Multiple Symbols and Bates**
        >>> MarketData.get_assessments_symbol_historical(symbol=["PCAAS00", "PCAAT00"], bate=["c", "h"])

        **Date Range**
        >>> d1 = date(2023, 1, 1)
        >>> d2 = date(2023, 2, 1)
        >>> MarketData.get_assessments_symbol_historical(symbol=["PCAAS00", "PCAAT00"], assess_date_gte=d1, assess_date_lte=d2])
        """
        paramList: List[str] = []

        if symbol:
            paramList.append(list_to_filter("symbol", symbol))
        if bate:
            paramList.append(list_to_filter("bate", bate))

        if assess_date != None:
            paramList.append(f'assessDate: "{assess_date}"')
        if assess_date_gt != None:
            paramList.append(f'assessDate > "{assess_date_gt}"')
        if assess_date_gte != None:
            paramList.append(f'assessDate >= "{assess_date_gte}"')
        if assess_date_lt != None:
            paramList.append(f'assessDate < "{assess_date_lt}"')
        if assess_date_lte != None:
            paramList.append(f'assessDate <= "{assess_date_lte}"')

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        endpoint_path = "history/symbol"
        params = {"filter": filter_exp, "page": page, "pageSize": page_size}
        return get_data(
            path=f"{self._path}{endpoint_path}",
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            params=params,
            paginate=paginate,
            raw=raw,
        )

    def get_assessments_by_mdc_current(
        self,
        *,
        mdc: str,
        bate: Optional[List[str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 10000,
        paginate: bool = True,
        raw: bool = False,
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch Current Assessments by MDC from the MarketData API.

        See ``get_mdcs()`` for a list of Market Data Categories.\n
        See ``get_assessments_by_mdc_historical()`` to include historical assessments as well.\n

        Parameters
        ----------
        mdc : str
            filter by Market Data Category
        bate : Optional[List[str]], optional
            filter by bate, by default None
        filter_exp : Optional[str], optional
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None
        page : int, optional
            pass-thru ``page`` query param to request a particular page of results, by default 1
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default True
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object

        Examples
        --------
        **Simple**
        >>> MarketData.get_assessments_by_mdc_current(mdc="ET")

        **Include bate**
        >>> MarketData.get_assessments_by_mdc_current(mdc="ET", bate=['c', 'u'])

        **Turn off auto pagination**
        >>> MarketData.get_assessments_by_mdc_current(mdc="ET", paginate=false)
        """
        paramList: List[str] = []
        paramList.append(f'MDC: "{mdc}"')
        if bate:
            paramList.append(list_to_filter("bate", bate))

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        endpoint_path = "current/mdc"
        params = {"filter": filter_exp, "page": page, "pageSize": page_size}
        return get_data(
            path=f"{self._path}{endpoint_path}",
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            params=params,
            paginate=paginate,
            raw=raw,
        )

    def get_assessments_by_mdc_historical(
        self,
        *,
        mdc: str,
        assess_date: Optional[date] = None,
        assess_date_lt: Optional[date] = None,
        assess_date_lte: Optional[date] = None,
        assess_date_gt: Optional[date] = None,
        assess_date_gte: Optional[date] = None,
        bate: Optional[List[str]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 10000,
        paginate: bool = True,
        raw: bool = False,
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch Historical Assessments by MDC from the MarketData API.

        See ``get_mdcs()`` for a list of Market Data Categories.\n
        See ``get_assessments_by_mdc_current()`` for the latest assessments only.\n

        Parameters
        ----------
        mdc : str
            filter by Market Data Category
        assess_date : Optional[date], optional
            filter by ``assessDate = x`` , by default None
        assess_date_lt : Optional[date], optional
            filter by ``assessDate < x``, by default None
        assess_date_lte : Optional[date], optional
            filter by ``assessDate <= x``, by default None
        assess_date_gt : Optional[date], optional
            filter by ``assessDate > x``, by default None
        assess_date_gte : Optional[date], optional
            filter by ``assessDate >= x``, by default None
        bate : List[str], optional
            filter by bate, by default []
        filter_exp : Optional[str], optional
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None
        page : int, optional
            pass-thru ``page`` query param to request a particular page of results, by default 1
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default True
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object

        Examples
        --------
        **Simple**
        >>> MarketData.get_assessments_by_mdc_historical(mdc="ET", assess_date=date(2023,2,1))

        **Date Range**
        >>> d1 = date(2023,1,1)
        >>> d2 = date(2023,2,1)
        >>> MarketData.get_assessments_by_mdc_historical(mdc="ET", assess_date_gte=d1, assess_date_lte=d2)
        """
        paramList: List[str] = []
        paramList.append(f'MDC: "{mdc}"')
        if bate:
            paramList.append(list_to_filter("bate", bate))

        if assess_date != None:
            paramList.append(f'assessDate: "{assess_date}"')
        if assess_date_gt != None:
            paramList.append(f'assessDate > "{assess_date_gt}"')
        if assess_date_gte != None:
            paramList.append(f'assessDate >= "{assess_date_gte}"')
        if assess_date_lt != None:
            paramList.append(f'assessDate < "{assess_date_lt}"')
        if assess_date_lte != None:
            paramList.append(f'assessDate <= "{assess_date_lte}"')

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        endpoint_path = "history/mdc"
        params = {"filter": filter_exp, "page": page, "pageSize": page_size}
        return get_data(
            path=f"{self._path}{endpoint_path}",
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            params=params,
            paginate=paginate,
            raw=raw,
        )

    def get_symbols(
        self,
        *,
        q: Optional[str] = None,
        commodity: Optional[Union[List[str], str]] = None,
        contract_type: Optional[
            Union[List[str], List[ContractType], str, ContractType]
        ] = None,
        currency: Optional[Union[List[str], str]] = None,
        uom: Optional[Union[List[str], str]] = None,
        symbol: Optional[Union[List[str], str]] = None,
        delivery_region_basis: Optional[Union[List[str], str]] = None,
        curve_code: Optional[Union[List[str], str]] = None,
        mdc: Optional[Union[List[str], str]] = None,
        assessment_frequency: Optional[
            Union[List[str], List[AssessmentFrequency], str, AssessmentFrequency]
        ] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = True,
        raw: bool = False,
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch Symbols from the MarketData API.

        Parameters
        ----------
        q : Optional[str], optional
            filter across fields using free text search, by default None
        commodity : Optional[Union[List[str], str]], optional
            filter by commodity, by default None
        contract_type : Optional[ Union[List[str], List[ContractType], str, ContractType] ], optional
            filter by contract type, by default None
        currency : Optional[Union[List[str], str]], optional
            filter by currency, by default None
        uom : Optional[Union[List[str], str]], optional
            filter by unit of measure, by default None
        symbol : Optional[Union[List[str], str]], optional
            filter by symbol, by default None
        delivery_region_basis : Optional[Union[List[str], str]], optional
            filter by delivery region basis, by default None
        curve_code : Optional[Union[List[str], str]], optional
            filter by curve code, by default None
        mdc : Optional[Union[List[str], str]], optional
            filter by Market Data Category, by default None
        assessment_frequency: Optional[Union[List[str], List[AssessmentFrequency], str, AssessmentFrequency]], optional
            filter by Assessment Frequency, by default None
        filter_exp : Optional[str], optional
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None
        page : int, optional
            pass-thru ``page`` query param to request a particular page of results, by default 1
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default True
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object
        Examples
        --------
        **Free text search**
        >>> MarketData.get_symbols(q="Brent")

        **Using String**
        >>> MarketData.get_symbols(contract_type="Forward")

        **Using List**
        >>> MarketData.get_symbols(currency=["USD", "EUR"])

        **Using Enum**
        >>> MarketData.get_symbols(currency=["USD", "EUR"], contract_type=[spgci.ContractType.Forward, spgci.ContractType.Spot])
        """
        paramList: List[str] = []

        if commodity:
            paramList.append(list_to_filter("commodity", commodity))
        if contract_type:
            paramList.append(list_to_filter("contract_type", contract_type))
        if currency:
            paramList.append(list_to_filter("currency", currency))
        if uom:
            paramList.append(list_to_filter("uom", uom))
        if delivery_region_basis:
            paramList.append(list_to_filter("delivery_region_basis", delivery_region_basis))
        if curve_code:
            paramList.append(list_to_filter("curve_code", curve_code))
        if symbol:
            paramList.append(list_to_filter("symbol", symbol))
        if mdc:
            paramList.append(list_to_filter("mdc", mdc))
        if assessment_frequency:
            paramList.append(list_to_filter("assessment_frequency", assessment_frequency))

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        params = {
            "q": q,
            "filter": filter_exp,
            "page": page,
            "pageSize": page_size,
        }
        return get_data(
            path=f"{self._ref_path}",
            df_fn=self._search_to_def,
            paginate_fn=self._ref_paginate,
            params=params,
            paginate=paginate,
            raw=raw,
        )

    def get_mdcs(
        self, *, subscribed_only: bool = True, raw: bool = False
    ) -> Union[pd.DataFrame, Response]:
        """
        Fetch the list of Market Data Categories (MDC)

        Parameters
        ----------
        subscribed_only : bool, optional
            return only MDC which you have access to, by default True
        raw : bool, optional
            return a ``requests.Response`` object instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object
        """
        params = {"subscribed_only": subscribed_only}

        return get_data(
            path="market-data/reference-data/v3/mdc",
            params=params,
        )
