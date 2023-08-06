from spgci.api_client import Paginator, get_data
from spgci.types import ContractType, CurveType, MatFrequency
from typing import List, Union, Optional
from datetime import date
from requests import Response
from spgci.utilities import list_to_filter
from pandas import DataFrame, to_datetime  # type: ignore


class ForwardCurves:
    """
    Platts Forward Curves.

    Includes
    --------
    ``get_curves()`` to get curve data, such as description, currency, maturity frequencies.\n
    ``get_assessments()`` to get assessment data for the symbols in a curve on a particular date.\n

    """

    _path = "market-data/forward-curve/v3/"
    _ref_path = "market-data/reference-data/v3/forward-curve/search"

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["totalPages"]

        if total_pages == 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages)

    @staticmethod
    def _convert_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = DataFrame(j["results"])

        # make date fields the correct datatype
        df["assessDate"] = to_datetime(df["assessDate"])
        df["roll_date"] = to_datetime(df["roll_date"])
        df["expiry_date"] = to_datetime(df["expiry_date"])

        return df

    @staticmethod
    def _ref_paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["total_pages"]

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages)

    @staticmethod
    def _ref_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = DataFrame(j["results"])

        return df

    def get_assessments(
        self,
        *,
        curve_code: Optional[Union[List[str], str]] = None,
        derivative_maturity_frequency: Optional[
            Union[List[str], List[MatFrequency], str, MatFrequency]
        ] = None,
        assess_date: Optional[date] = None,
        assess_date_gt: Optional[date] = None,
        assess_date_gte: Optional[date] = None,
        assess_date_lt: Optional[date] = None,
        assess_date_lte: Optional[date] = None,
        field: Optional[str] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 10000,
        raw: bool = False,
        paginate: bool = True,
    ) -> Union[DataFrame, Response]:
        """
        Fetch Forward Curves Metadata from the Market Data API.

        See ``get_curves()`` to search for curve codes.\n

        Parameters
        ----------
        curve_code : Optional[Union[List[str], str]], optional
            fitler by curve code, by default None
        derivative_maturity_frequency : Optional[ Union[List[str], List[MatFrequency], str, MatFrequency] ], optional
            fitler by maturity frequency, by default None
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
        **Get Latest Curve**
        >>> ForwardCurves.get_assessments(curve_code="CN003")

        **Get Multiple Curves**
        >>> ForwardCurves.get_assessments(curve_code=["CN003", "CN002"])

        **Get Monthly Contracts**
        >>> ForwardCurves.get_assessments(curve_code=["CN003", "CN002"], derivative_maturity_frequency="Month")

        **Get Assessments for a Curve on a particular date**
        >>> ForwardCurves.get_assessments(curve_code=["CN003"], assess_date=date(2023,2,13))
        """
        endpoint_path = "curve-codes"

        paramList: List[str] = []

        if curve_code:
            paramList.append(list_to_filter("curve_code", curve_code))

        if derivative_maturity_frequency:
            paramList.append(
                list_to_filter(
                    "derivative_maturity_frequency", derivative_maturity_frequency
                )
            )

        if assess_date:
            paramList.append(f'assessDate: "{assess_date}"')
        if assess_date_gt:
            paramList.append(f'assessDate > "{assess_date_gt}"')
        if assess_date_gte:
            paramList.append(f'assessDate >= "{assess_date_gte}"')
        if assess_date_lt:
            paramList.append(f'assessDate < "{assess_date_lt}"')
        if assess_date_lte:
            paramList.append(f'assessDate <= "{assess_date_lte}"')

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        params = {
            "filter": filter_exp,
            "page": page,
            "pageSize": page_size,
            "field": field,
        }

        response = get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            raw=raw,
            paginate=paginate,
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
        )

        return response

    def get_curves(
        self,
        *,
        q: Optional[str] = None,
        commodity: Optional[Union[List[str], str]] = None,
        contract_type: Optional[
            Union[List[str], List[ContractType], str, ContractType]
        ] = None,
        currency: Optional[Union[List[str], str]] = None,
        uom: Optional[Union[List[str], str]] = None,
        curve_code: Optional[Union[List[str], str]] = None,
        curve_type: Optional[Union[List[str], List[CurveType], str, CurveType]] = None,
        mdc: Optional[Union[List[str], str]] = None,
        derivative_maturity_frequency: Optional[
            Union[List[str], List[MatFrequency], str, MatFrequency]
        ] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = True,
        raw: bool = False,
        subscribed_only: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Fetch Forward Curves by Curve Code from the Market Data API.

        See ``get_assessments()`` to get assessments for each symbol in a curve.\n

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
         curve_code : Optional[Union[List[str], str]], optional
             filter by curve code, by default None
         curve_type : Optional[Union[List[str], List[CurveType], str, CurveType]], optional
             filter by curve type, by default None
         mdc : Optional[Union[List[str], str]], optional
             fitler by Market Data Category, by default None
         derivative_maturity_frequency : Optional[ Union[List[str], List[MatFrequency], str, MatFrequency] ], optional
             filter by maturity frequency, by default None
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
         subscribed_only : bool, optional
             return only curves which you have access to , by default False

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
         >>> ForwardCurves.get_curves(q="Brent")

         **Find Benzene Curves**
         >>> ForwardCurves.get_curves(commodity="Benzene")

         **Find Monthly Relative Curves by MDC**
         >>> ForwardCurves.get_curves(curve_type=CurveType.Relative, mdc=["DR"], derivative_maturity_frequency='Month')
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
        if derivative_maturity_frequency:
            paramList.append(
                list_to_filter(
                    "derivative_maturity_frequency", derivative_maturity_frequency
                )
            )
        if curve_code:
            paramList.append(list_to_filter("curve_code", curve_code))
        if curve_type:
            paramList.append(list_to_filter("curve_type", curve_type))
        if mdc:
            paramList.append(list_to_filter("mdc", mdc))

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        params = {
            "q": q,
            "filter": filter_exp,
            "page": page,
            "pageSize": page_size,
            "subscribed_only": subscribed_only,
        }
        return get_data(
            path=f"{self._ref_path}",
            df_fn=self._ref_to_df,
            paginate_fn=self._ref_paginate,
            params=params,
            paginate=paginate,
            raw=raw,
        )
