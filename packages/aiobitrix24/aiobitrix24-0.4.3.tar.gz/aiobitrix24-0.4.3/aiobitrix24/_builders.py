"""String query params builders for bx24."""

from dataclasses import dataclass
from urllib.parse import quote

from aiobitrix24.exceptions import BatchError

MAX_BATCH_SIZE = 50
HALT = 0


@dataclass
class BatchQuery:
    """Query for batch request."""

    name: str
    method: str
    params: dict  # noqa: WPS110


def build_query(query_params: dict, prefix: str = "") -> str:
    """Build complex params row from complex dict.

    :param query_params: query params for string conversion
    :param prefix: main param name in deep query, defaults to ""
    :return: specific string with query params for bx24
    """
    query_string = []
    for key, params_value in query_params.items():
        if isinstance(params_value, dict):
            query_string.append(build_query(params_value, key))
        elif isinstance(params_value, list):
            list_params = {
                str(index): parameter for index, parameter in enumerate(params_value)
            }
            query_string.append(build_query(list_params, key))
        else:
            params_value = params_value if params_value else "0"
            if prefix:
                query_string.append(
                    f"{quote(prefix)}[{quote(str(key))}]={quote(str(params_value))}",
                )
            else:
                query_string.append(f"{quote(str(key))}={quote(str(params_value))}")
    return f"{'&'.join(query_string)}"


def build_batch(queries: list[BatchQuery], halt: int = HALT) -> dict:
    """Build dict for json post batch bitrix24 request.

    :param queries: list of queries for batch request
    :param halt: bitrix24 param, if to stop request on error rises, defaults to HALT
    :raises BatchError: rises if count of queries is more than max batch count
    :return: dict for batch request via json
    """
    if len(queries) > MAX_BATCH_SIZE:
        raise BatchError
    result_query = {"halt": halt, "cmd": {}}
    for query in queries:
        result_query["cmd"][query.name] = f"{query.method}?{build_query(query.params)}"
    return result_query


def build_chunks(
    queries: list[BatchQuery],
    limit: int = MAX_BATCH_SIZE,
) -> list[list[BatchQuery]]:
    """Split list of queries on bathes with limited size.

    :param queries: list of queries for batch request
    :param limit: max count of queries in batch request, defaults to MAX_BATCH_SIZE
    :return: list of batches with queries
    """
    return [
        (queries[key_position : key_position + limit])
        for key_position in range(0, len(queries), limit)
    ]
