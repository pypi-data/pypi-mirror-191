from spgci.api_client import get_data, Paginator
from typing import List, Union, Optional
from requests import Response
from spgci.utilities import list_to_filter
from pandas import DataFrame, to_datetime  # type: ignore
from datetime import date, datetime
from spgci.types import OrderState, OrderType


class EWindowMarketData:
    """
    EWindow Market Data - Bids, Offers, Trades

    Includes
    --------
    ``get_products()`` to see the list of Products and their latest order date.
    ``get_markets()`` to see the list of Markets and their latest order date.
    ``get_botes()`` to get Bids, Offers, Trades.

    """

    _path = "tradedata/v3/"

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["total_pages"]

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages)

    @staticmethod
    def _convert_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = DataFrame(j["results"])

        df["order_begin"] = to_datetime(df["order_begin"])
        df["order_end"] = to_datetime(df["order_end"])
        df["order_date"] = to_datetime(df["order_date"])
        df["order_time"] = to_datetime(df["order_time"])
        df["deal_begin"] = to_datetime(df["deal_begin"])
        df["deal_end"] = to_datetime(df["deal_end"])

        return df

    @staticmethod
    def _convert_agg_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = DataFrame(j["aggResultValue"])

        df["max(order_date)"] = to_datetime(df["max(order_date)"])

        return df

    def get_markets(self, raw: bool = False) -> Union[DataFrame, Response]:
        """
        Fetch the list of Markets.

        Parameters
        ----------
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
        >>> EWindowMarketData.get_markets()
        """
        params = {
            "groupBy": "market",
            "field": "max(order_date)",
            "pageSize": 1000,
            "sort": "order_time:desc",
        }

        return get_data(
            path=f"{self._path}ewindowdata",
            raw=raw,
            params=params,
            paginate=True,
            paginate_fn=self._paginate,
            df_fn=self._convert_agg_to_df,
        )

    def get_products(self, raw: bool = False) -> Union[DataFrame, Response]:
        """
        Fetch the list of Products.

        Parameters
        ----------
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
        >>> EWindowMarketData.get_products()
        """
        params = {
            "groupBy": "product, market",
            "field": "max(order_date)",
            "pageSize": 1000,
            "sort": "order_time:desc",
        }

        return get_data(
            path=f"{self._path}ewindowdata",
            raw=raw,
            params=params,
            paginate=True,
            paginate_fn=self._paginate,
            df_fn=self._convert_agg_to_df,
        )

    def get_botes(
        self,
        *,
        market: Optional[Union[List[str], str]] = None,
        product: Optional[Union[List[str], str]] = None,
        hub: Optional[Union[List[str], str]] = None,
        strip: Optional[Union[List[str], str]] = None,
        order_type: Optional[Union[List[str], List[OrderType], str, OrderType]] = None,
        order_state: Optional[
            Union[List[str], List[OrderState], str, OrderState]
        ] = None,
        order_id: Optional[Union[List[str], str]] = None,
        order_time: Optional[Union[datetime, date]] = None,
        order_time_lt: Optional[Union[datetime, date]] = None,
        order_time_lte: Optional[Union[datetime, date]] = None,
        order_time_gt: Optional[Union[datetime, date]] = None,
        order_time_gte: Optional[Union[datetime, date]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Fetch BOTes (Bids, Offers, Trades) from the EWindow MarketData API.

        See ``get_products()`` to search for products.\n
        See ``get_markets()`` to search for markets.\n

        Parameters
        ----------
        market : Optional[Union[List[str], str]], optional
            filter by market, by default None
        product : Optional[Union[List[str], str]], optional
            filter by product, by default None
        hub : Optional[Union[List[str], str]], optional
            filter by hub, by default None
        strip : Optional[Union[List[str], str]], optional
            filter by strip, by default None
        order_type : Optional[Union[List[str], List[OrderType], str, OrderType]], optional
            filter by order type, by default None
        order_state : Optional[ Union[List[str], List[OrderState], str, OrderState] ], optional
            filter by order state, by default None
        order_id : Optional[Union[List[str], str]], optional
            filter by order id, by default None
        order_time : Optional[Union[datetime, date]], optional
            filter by ``order_time = x``, by default None
        order_time_lt : Optional[Union[datetime, date]], optional
            filter by ``order_time < x``, by default None
        order_time_lte : Optional[Union[datetime, date]], optional
            filter by ``order_time <= x``, by default None
        order_time_gt : Optional[Union[datetime, date]], optional
            filter by ``order_time > x``, by default None
        order_time_gte : Optional[Union[datetime, date]], optional
            filter by ``order_time >= x``, by default None
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
        >>> EWindowMarketData.get_botes(market=["EU BFOE", "US MidWest"])

        **Date Range**
        >>> d1 = date(2023, 2, 1)
        >>> d2 = date(2023, 2, 3)
        >>> EWindowMarketData.get_botes(market=["EU BFOE", "US MidWest"], order_time_gt=d1, order_time_lt=d2)
        """
        endpoint_path = "ewindowdata"

        paramList: List[str] = []

        if market:
            paramList.append(list_to_filter("market", market))
        if product:
            paramList.append(list_to_filter("product", product))
        if hub:
            paramList.append(list_to_filter("hub", hub))
        if strip:
            paramList.append(list_to_filter("strip", strip))
        if order_type:
            paramList.append(list_to_filter("order_type", order_type))
        if order_id:
            paramList.append(list_to_filter("order_id", order_id))
        if order_state:
            paramList.append(list_to_filter("order_state", order_state))

        if order_time:
            paramList.append(f'order_time: "{order_time}"')
        if order_time_gt:
            paramList.append(f'order_time > "{order_time_gt}"')
        if order_time_gte:
            paramList.append(f'order_time >= "{order_time_gte}"')
        if order_time_lt:
            paramList.append(f'order_time < "{order_time_lt}"')
        if order_time_lte:
            paramList.append(f'order_time <= "{order_time_lte}"')

        if filter_exp is None:
            filter_exp = " AND ".join(paramList)
        else:
            filter_exp += " AND " + " AND ".join(paramList)

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            raw=raw,
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            paginate=paginate,
        )

        return response
