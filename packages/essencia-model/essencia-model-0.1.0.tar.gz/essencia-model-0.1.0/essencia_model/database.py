
from typing import Union
from deta import Deta
from .config import config


async def get_list_by_table(table: str, query: Union[dict[str, str], list[dict[str, str]]] = None):
	base = Deta(config.get('ESSENCIA_PROJECT_KEY')).AsyncBase(table)
	try:
		response = await base.fetch(query=query)
		all_items = response.items
		while response.last:
			response = await base.fetch(last=response.last)
			all_items.extend(response.items)
		return all_items
	finally:
		await base.close()


async def get_deta_object_by_key(table: str, key: str):
	base = Deta(config.get('ESSENCIA_PROJECT_KEY')).AsyncBase(table)
	try:
		return await base.get(key)
	finally:
		await base.close()