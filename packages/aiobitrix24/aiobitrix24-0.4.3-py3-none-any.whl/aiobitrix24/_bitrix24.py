"""Main bitrix24 module."""
import asyncio
import time

import httpx

from aiobitrix24 import _builders
from aiobitrix24.methods.common import BATCH


class _Bitrix24:
    """Class for making bitrix24 requests."""

    def __init__(
        self,
        url: str | None = None,
        sleep_sec: int = 3,
        httpx_timeout: int = 20,
    ) -> None:
        """Init class.

        :param url: base url for bitrix24 rest api, defaults to None
        :param sleep_sec: sleep seconds between queries, defaults to 3
        :param httpx_timeout: request timeout, defaults to 20
        """
        self._url = url
        self._sleep_sec = sleep_sec
        self._httpx_timeout = httpx_timeout
        self._last_request_time = time.time() - sleep_sec

    def url(self, url: str) -> None:
        """Set base url for Birtix24 class.

        :param url: base bitrix url
        """
        self._url = url

    def timeout(self, timeout: int | float) -> None:
        """Set bitrix timeout.

        :param timeout: timeout_sec
        """
        self._sleep_sec = timeout

    async def request(
        self,
        method: str,
        query_params: dict,
        is_query_complex: bool = False,
    ) -> httpx.Response:
        """Request to bitrix24.

        :param method: call method
        :param query_params: query params
        :param is_query_complex: build custom param string, defaults to False
        :raises ValueError: url parameter not set
        :return: http response
        """
        if self._url is None:
            raise ValueError("Url parameter not set")
        await self._sleep()
        async with httpx.AsyncClient() as client:
            if is_query_complex:
                complex_query = _builders.build_query(query_params)
                return await client.post(
                    f"{self._url}{method}?{complex_query}",
                    timeout=self._httpx_timeout,
                )
            return await client.post(
                f"{self._url}{method}",
                json=query_params,
                timeout=self._httpx_timeout,
            )

    async def batch_request(
        self,
        queries: list[_builders.BatchQuery],
    ) -> httpx.Response:
        """Batch request to bitrix24.

        :param queries: batch of queries
        :raises ValueError: url parameter not set
        :return: http response
        """
        if self._url is None:
            raise ValueError("Url parameter not set")
        await self._sleep()
        batch_query = _builders.build_batch(queries)
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{self._url}{BATCH}",
                json=batch_query,
                timeout=self._httpx_timeout,
            )

    async def _sleep(self) -> None:
        current_time = time.time()
        if current_time - self._last_request_time < self._sleep_sec:
            self._last_request_time = current_time + self._sleep_sec
            await asyncio.sleep(self._sleep_sec)
        else:
            self._last_request_time = current_time


bx24 = _Bitrix24()
