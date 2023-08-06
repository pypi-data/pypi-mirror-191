from __future__ import annotations

import logging
from dataclasses import dataclass

from aiobitrix24._bitrix24 import bx24
from aiobitrix24._builders import MAX_BATCH_SIZE, BatchQuery, build_chunks
from aiobitrix24.exceptions import BitrixError
from aiobitrix24.methods import crm

logger = logging.getLogger("aiobitrix24.crm")
logger.setLevel(logging.WARNING)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)


class BaseSelect:
    @classmethod
    async def json(
        cls,
        method: str,
        start: int,
        process_id: int,
        filters: dict,
        select: list[str] | None = None,
    ) -> dict:
        query_params = {
            "start": start,
            "entityTypeId": process_id,
            "select": select if select else ["*"],
            "filter": filters,
        }
        response_json = (
            await bx24.request(
                method,
                query_params,
            )
        ).json()
        if "error" in response_json:
            raise BitrixError(response_json["error_description"])
        return response_json


# class BaseBatchUpdate:
#     @classmethod
#     async def update(chunk)


@dataclass
class CRMItem:
    """Item in bitrix crm smart process."""

    fields: dict
    name: str = ""
    _select = BaseSelect

    @classmethod
    async def select(
        cls,
        process_id: int,
        filters: dict,
        select: list[str] | None = None,
        limit: int | None = None,
    ) -> list[CRMItem]:
        """Select all items from process satisfying filters.

        :param process_id: smart process id in bitrix
        :param filters: filters like in crm docs
        :param select: field for select, defaults to None
        :param limit: limit count of selected rows, defaults to None
        :return: list of selected smart process items
        """
        response_json = await cls._select.json(
            crm.Item.LIST,
            0,
            process_id,
            filters,
            select,
        )
        logger.debug(response_json)
        crm_items = [CRMItem(fields) for fields in response_json["result"]["items"]]
        if limit and len(crm_items) >= limit:
            return crm_items[:limit]
        for page in range(MAX_BATCH_SIZE, response_json["total"], MAX_BATCH_SIZE):
            response_json = await cls._select.json(
                crm.Item.LIST,
                page,
                process_id,
                filters,
                select,
            )
            page_items = [
                CRMItem(fields) for fields in response_json["result"]["items"]
            ]
            crm_items.extend(page_items)
            if limit and len(crm_items) >= limit:
                return crm_items[:limit]
        return crm_items

    @classmethod
    async def batch_update(cls, crm_items: list[CRMItem]) -> None:
        """Update crm items by batch requests.

        :param crm_items: list of crm items for update
        """
        queries = []
        for crm_item in crm_items:
            query_params = {
                "entityTypeId": crm_item.fields["entityTypeId"],
                "id": crm_item.fields["id"],
            }
            fields = dict(crm_item.fields)
            fields.pop("id")
            query_params["fields"] = fields
            queries.append(
                BatchQuery(
                    crm_item.fields["id"],
                    crm.Item.UPDATE,
                    query_params,
                ),
            )
        updated_items = {}
        for chunk in build_chunks(queries):
            chunk_json = (await bx24.batch_request(chunk)).json()
            logger.debug(chunk_json)
            if chunk_json["result"]["result_error"]:
                raise BitrixError(str(chunk_json["result"]["result_error"]))
            updated_items |= chunk_json["result"]["result"]
        for crm_item in crm_items:
            crm_item.fields = updated_items[str(crm_item.fields["id"])]["item"]
        return crm_items

    @classmethod
    async def batch_create(
        cls,
        process_id: int,
        crm_items: list[CRMItem],
        as_dict: bool = False,
    ) -> list[CRMItem] | dict[str, CRMItem]:
        """Add crm items by batch requests.

        :param process_id: smart process id in bitrix
        :param crm_items: list of crm items for create
        :param as_dict: result type, defaults to False
        :raises BitrixError: Error in bitrix response
        :return: list or dict of CRMItems
        """
        queries = []
        for crm_item in crm_items:
            query_params = {
                "entityTypeId": process_id,
                "fields": crm_item.fields,
            }
            queries.append(
                BatchQuery(crm_item.name, crm.Item.ADD, query_params),
            )
        created_items: dict | list = {} if as_dict else []
        for chunk in build_chunks(queries):
            chunk_json = (await bx24.batch_request(chunk)).json()
            if chunk_json["result"]["result_error"]:
                raise BitrixError(str(chunk_json["result"]["result_error"]))
            for name, created_item in chunk_json["result"]["result"].items():
                if as_dict:
                    created_items[name] = CRMItem(created_item["item"], name=name)
                else:
                    created_items.append(CRMItem(created_item["item"], name=name))  # type: ignore
        return created_items
