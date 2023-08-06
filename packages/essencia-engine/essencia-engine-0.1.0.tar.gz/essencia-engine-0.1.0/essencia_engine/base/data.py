from typing import Generator
from starlette.requests import Request
from .database import *
from .context import *
from .function import *


async def object_from_key(table: str,  key: str):
	return await async_deta(table=table, key=key)


async def profile_from_key(table: str, key: str):
	data = await object_from_key(table, key)
	try:
		return {**data, 'person': ctx.get(person_var)[data['person_key']]}
	except BaseException as e:
		print(e)
		await ctx_person.update()
		return {**data, 'person': ctx.get(person_var)[data['person_key']]}


async def profile_list(table: str,  request: Request):
	query = None
	if request.query_params.get('search'):
		query = {'search?contains': normalize(request.query_params.get('search'))}
	return await async_deta(table=table, query=query)


async def person_list(request: Request):
	query = None
	if request.query_params.get('search'):
		query = {'search_name?contains': normalize(request.query_params.get('search'))}
	return await async_deta('Person', query=query)


async def make_profile_generator(table: str, request: Request) -> Generator:
	return (item for item in await profile_list(table, request))


async def add_person_to_profile_data(generator: Generator) -> list[dict]:
	result = list()
	try:
		while True:
			item = next(generator)
			result.append({**item, 'person': ctx.get(person_var)[item['person_key']]})
	except BaseException as e:
		print(e)
		await ctx_person.update()
		while True:
			item = next(generator)
			result.append({**item, 'person': ctx.get(person_var)[item['person_key']]})
	finally:
		return result


