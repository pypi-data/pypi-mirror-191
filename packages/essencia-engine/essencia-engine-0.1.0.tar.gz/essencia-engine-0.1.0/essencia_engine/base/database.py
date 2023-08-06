__all__ = [
    'async_deta',
    'async_base',
]

from deta import Deta
from contextlib import asynccontextmanager
from .types import *
from .setup import *


async def async_base(table: str) -> Deta.AsyncBase:
    return Deta(config.get('ESSENCIA_PROJECT_KEY')).AsyncBase(table)


@asynccontextmanager
async def async_deta_context(
        table: str,
        key: Optional[str] = None,
        query: Optional[DetaQuery] = None,
        data: Optional[Jsonable] = None,
        items: Optional[list[Jsonable]] = None,
        delete: str = None,
        expire_in: str = None,
        expire_at: str = None,
        limit: int = 25000,
):
    abase = await async_base(table)
    result = None
    try:
        if key:
            result = await abase.get(key=key)
        elif data:
            assert isinstance(data, dict), 'async_deta data has to be a dict'
            found_key = data.pop('key', None)
            result = await abase.put(data=data, key=found_key, expire_in=expire_in, expire_at=expire_at)
        elif items:
            result = list()
            size = len(items)
            gen = (item for item in items)
            mod = size % 20
            loops = (size - mod) / 20
            while loops > 0:
                result.extend(await abase.put_many(
                    items=[next(gen) for _ in range(20)],
                    expire_in=expire_in,
                    expire_at=expire_at))
                loops -= 1
            result.append(await abase.put_many(items=list(gen), expire_in=expire_in, expire_at=expire_at))
        elif delete:
            result = await abase.delete(delete)
        else:
            result = list()
            response = await abase.fetch(query=query, limit=limit)
            result.extend(response.items)
            last = response.last
            print(f'last: {last}')
            try:
                while last:
                    response = await abase.fetch(query=query, limit=limit, last=last)
                    last = response.last
                    print(f'last: {last}')
                    result.extend(response.items)
            except BaseException as e:
                print(e)
    except BaseException as e:
        print(f'async_deta => {e}')
    finally:
        yield result
        await abase.close()


async def async_deta(
        table: str,
        key: Optional[str] = None,
        query: Optional[DetaQuery] = None,
        data: Optional[Jsonable] = None,
        items: Optional[list[Jsonable]] = None,
        delete: str = None,
        expire_in: str = '',
        expire_at: str = '',
        limit: int = 1000):

    async with async_deta_context(
            table=table,
            key=key,
            query=query,
            data=data,
            items=items,
            delete=delete,
            expire_in=expire_in,
            expire_at=expire_at,
            limit=limit,
    ) as final_result:
        return final_result






