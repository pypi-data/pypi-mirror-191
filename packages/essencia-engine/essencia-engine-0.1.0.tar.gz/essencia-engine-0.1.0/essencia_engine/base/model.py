__all__ = [
    'BaseModel',
    'Key'
]

import inspect
from dataclasses import Field
from collections import ChainMap
from abc import ABC
from abc import ABC, abstractmethod

from anyio import create_task_group
from .types import *
from .ntuple import *
from .function import *
from .database import *
from .setup import *
from .context import *


class Key:

    def __init__(self, model_name: str):
        self.model_name = model_name

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.key_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.key_name, value)

    @abstractmethod
    def validate(self, value):
        pass

    @property
    def model(self):
        return MODEL_MAP[self.model_name]

    @property
    def key_name(self):
        return self.model.key_name()

    def instance(self, obj):
        data = templates.env.globals.get(self.model_name, {}).get(getattr(obj, self.key_name))
        if data:
            return self.model(**data)
        return None


@dataclass
class BaseModel(ABC):
    DETA_QUERY: ClassVar[DetaQuery] = None
    SINGULAR: ClassVar[str] = None
    PLURAL: ClassVar[str] = None
    ITEM_NAME: ClassVar[str] = None
    KEY_NAME: ClassVar[str] = None
    TABLE: ClassVar[str] = None
    EXIST_PARAMS: ClassVar[Union[str, list[str]]] = None
    FORM_FIELDS: ClassVar[list[Form.FieldHTML]] = None
    DETAIL_PROPERTIES: ClassVar[list[Property]] = None
    DETAIL_BUTTONS: ClassVar[list[Anchor]] = None
    THEAD: ClassVar[list[Table.THead]] = None
    SEARCH_PARAM: ClassVar[Union[list[str], str]] = 'search'
    UPDATE_BUTTON: ClassVar[bool] = True
    DELETE_BUTTON: ClassVar[bool] = False
    CONTEXT_TABLES: ClassVar[list[str]] = None
    MICRO: ClassVar[str] = None
    FORM_SCRIPT = None

    @property
    def _search(self):
        return str(self)

    def __post_init__(self):
        self.setup_instance()

    @classmethod
    async def search_from_database(cls, query: DetaQuery) -> list['BaseModel']:
        return [cls(**item) for item in await async_deta(cls.table(), query=query)]

    @classmethod
    def context_tables(cls) -> list[str]:
        return cls.CONTEXT_TABLES or list()

    @classmethod
    def plural(cls):
        return cls.PLURAL or f'{cls.SINGULAR}s'

    @classmethod
    async def context_update(cls):
        try:
            table_list = [cls.table(), *cls.context_tables()]
            await ctx_update(table_list=table_list)
            for item in table_list:
                templates.env.globals[item] = CONTEXT_DATA[item]
        except:
            pass

    def export_to_context(self):
        return self.export()

    def setup_instance(self):
        for item in fields(self):
            value = getattr(self, item.name)
            if item.type is not str:
                if isinstance(value, str):
                    if item.type is datetime.date:
                        try:
                            setattr(self, item.name, datetime.date.fromisoformat(value))
                        except BaseException as e:
                            pass
                    elif item.type is datetime.datetime:
                        try:
                            setattr(self, item.name, datetime.datetime.fromisoformat(value))
                        except BaseException as e:
                            pass
                    elif item.type is float:
                        _value = value.replace(',', '.')
                        try:
                            setattr(self, item.name, float(_value))
                        except BaseException as e:
                            pass
                    elif item.type is int:
                        _value = value.replace(',', '.')
                        try:
                            setattr(self, item.name, int(_value))
                        except BaseException as e:
                            pass
                    else:
                        try:
                            if item.type.is_enum():
                                if '+' in value:
                                    values = [item.strip() for item in value.split('+')]
                                    setattr(self, item.name, [item.type[en] for en in values])
                                else:
                                    setattr(self, item.name, item.type[value])
                        except BaseException as e:
                            pass
                            try:
                                if item.type.is_enum():
                                    if '+' in value:
                                        values = [item.strip() for item in value.split('+')]
                                        setattr(self, item.name, [item.type(en) for en in values])
                                    else:
                                        setattr(self, item.name, item.type(value))
                            except BaseException as e:
                                pass
                elif isinstance(value, list):
                    if item.type is list[datetime.datetime]:
                        try:
                            setattr(self, item.name, [datetime.datetime.isoformat(item) for item in value])
                        except BaseException as e:
                            pass
                    elif item.type is list[datetime.date]:
                        try:
                            setattr(self, item.name, [datetime.date.isoformat(item) for item in value])
                        except BaseException as e:
                            pass
                    elif item.type is list[float]:
                        _value = [item.replace(',', '.') for item in value]
                        try:
                            setattr(self, item.name, [float(item) for item in _value])
                        except BaseException as e:
                            pass
                    elif item.type is list[float]:
                        _value = [item.replace(',', '.') for item in value]
                        try:
                            setattr(self, item.name, [int(item) for item in _value])
                        except BaseException as e:
                            pass
                    else:
                        try:
                            if item.type.is_enum():
                                setattr(self, item.name, [item.type[item] for item in value])
                        except BaseException as e:
                            pass
                            try:
                                if item.type.is_enum():
                                    setattr(self, item.name, [item.type(item) for item in value])
                            except BaseException as e:
                                pass
                elif isinstance(value, dict):
                    try:
                        setattr(self, item.name, item.type(**value))
                    except:
                        pass

        for item in self.fields().values():
            if isinstance(item.type, Key):
                if item.type.key_name == 'creator':
                    setattr(self, '_creator', item.type.instance(self))
                else:
                    setattr(self, item.type.key_name.replace('_key', ''), item.type.instance(self))
        if self.fields().get('creator'):
            if not getattr(self, 'creator'):
                if templates.env.globals.get('user'):
                    setattr(self, 'creator', templates.env.globals.get('user').get('key'))

    @classmethod
    def micro(cls):
        if MICRO_TYPE == 'normal':
            if MICRO_NAME:
                return f'/{MICRO_NAME}'
        return ''

    @classmethod
    def base_path(cls) -> str:
        return f'{cls.micro()}/{cls.item_name()}'

    def detail_path(self) -> str:
        return f'{self.base_path()}/{getattr(self, "key")}'

    def detail_partial_path(self) -> str:
        return f'{self.base_path()}/partial/{getattr(self, "key")}'

    def delete_path(self) -> str:
        return f'{self.base_path()}/delete/{getattr(self, "key")}'

    def update_path(self) -> str:
        return f'{self.base_path()}/update/{getattr(self, "key")}'

    @classmethod
    def new_path(cls) -> str:
        return f'{cls.base_path()}/new'

    @classmethod
    def index_path(cls):
        return f'{cls.base_path()}/index'

    @classmethod
    def list_path(cls, deta_query: DetaQuery = None):
        if deta_query:
            items = list()
            for key, value in deta_query.items():
                items.append(QueryItem(key=key, value=value))
            string = str(QueryString(items=items))
        else:
            string = ''
        return f'{cls.base_path()}/list{string}'

    @classmethod
    def list_partial_path(cls):
        return f'{cls.base_path()}/partial/list'

    @classmethod
    def search_param(cls):
        return cls.SEARCH_PARAM or 'search'

    @classmethod
    def search_path(cls):
        return f'{cls.base_path()}/search'

    @classmethod
    def table_path(cls):
        return f'{cls.base_path()}/table'

    @classmethod
    def table(cls) -> str:
        return cls.TABLE or cls.__name__

    def __lt__(self, other) -> bool:
        return normalize(str(self)) < normalize(str(other))

    @classmethod
    def item_name(cls) -> str:
        return cls.ITEM_NAME or cls.__name__.lower()

    @property
    def self_key(self) -> str:
        return getattr(self, 'key')

    @classmethod
    def key_name(cls) -> str:
        return cls.KEY_NAME or f'{cls.item_name()}_key'

    @classmethod
    def item_name_plural(cls) -> str:
        return f'{cls.item_name()}_list'

    @classmethod
    def init_vars(cls) -> list:
        return [item for item, value in inspect.signature(cls).parameters.items() if str(value).__contains__('InitVar')]

    @classmethod
    def class_vars(cls) -> list:
        return [item for item, value in inspect.signature(cls).parameters.items() if str(value).__contains__('ClassVar')]

    @classmethod
    def fields(cls) -> dict[str, Field]:
        return {item.name: item for item in fields(cls)}

    @classmethod
    def init_data(cls, data: JsonDict) -> dict:
        init_kwords = [*cls.fields().keys(), *cls.init_vars()]
        return {item: value for item, value in data.items() if item in init_kwords}

    def export(self) -> Jsonable:
        data = asdict(self)
        result = dict()
        for key, value in data.items():
            result[key] = parse_json(type(self), value)
        if 'search' in self.fields().keys():
            result['search'] = normalize(self._search)
        return result

    @classmethod
    def thead(cls):
        return cls.THEAD or [Property(item.name, item.name) for item in fields(cls)]

    @classmethod
    async def model_context_update(cls):
        if MODEL_CONTEXT_MAP.get(cls.table()):
            await MODEL_CONTEXT_MAP.get(cls.table()).update()

    async def save(self) -> Optional['BaseModel']:
        await self.context_update()
        saved = await async_deta(type(self).__name__, data=self.export())
        if saved:
            await self.model_context_update()
            return type(self)(**saved)
        return None

    async def delete(self) -> None:
        await async_deta(table=self.table(), delete=getattr(self, 'key'))
        await self.model_context_update()
        return

    @classmethod
    def list_from_context(cls) -> list[Optional['BaseModel']]:
        context = MODEL_CONTEXT_MAP.get(cls.table())
        if context:
            data = context.database()
            if data:
                return [cls(**item) for item in data.values()]
        return list()

    @classmethod
    def instance_from_context(cls, key: str) -> Optional['BaseModel']:
        context = MODEL_CONTEXT_MAP.get(cls.table())
        if context:
            data = context.key(key)
            if data:
                return cls(**data)
        return None

    @classmethod
    async def from_database(
            cls,
            table: str = None,
            key: str = None,
            query: DetaQuery = None,
            limit: int = 1000
    ) -> Union['BaseModel', list['BaseModel'], None]:
        table = table or cls.table()
        if key:
            item = await async_deta(table=table, key=key)
            if item:
                return cls(**item)
            return None
        else:
            return sorted([cls(**item) for item in await async_deta(table=table, query=query, limit=limit)])

    @classmethod
    async def items(cls, query: DetaQuery = None) -> list['BaseModel']:
        await cls.context_update()
        if not query:
            if cls.DETA_QUERY:
                query = cls.DETA_QUERY
        if query:
            query = {f'{name}?contains': normalize(value) for name, value in query.items()}
        return await cls.from_database(table=cls.table(), query=query)

    @classmethod
    async def item(cls, key: str) -> 'BaseModel':
        await cls.context_update()
        return await cls.from_database(table=cls.table(), key=key)

    @classmethod
    async def select_options(cls, query: DetaQuery = None) -> str:
        items = await cls.items(query=query)
        text = f'<option></option>'
        for item in items:
            text += f'<option value="{item.key}">{str(item)}</option>\n'
        return text

    def display(self) -> Union[Markup, str]:
        return str(self)

    def json(self):
        return self.export()

    async def exist(self) -> Union['BaseModel', bool]:
        if self.EXIST_PARAMS:
            if isinstance(self.EXIST_PARAMS, str):
                query = dict()
                for item in self.EXIST_PARAMS.split():
                    query.update({item: getattr(self, item)})
            elif isinstance(self.EXIST_PARAMS, list):
                query = list()
                for item in self.EXIST_PARAMS:
                    query.append({item: getattr(self, item)})
            data = await async_deta(self.table(), query=query)
            if data:
                return type(self)(**data[0])
            return False
        return NotImplemented

    @classmethod
    def form_new(cls) -> Form:
        return Form(
            title=f'Adicionar {cls.SINGULAR}',
            id=f'{cls.item_name()}-new',
            method='post',
            action=f'/{cls.item_name()}/new',
            form_fields=cls.FORM_FIELDS,
            script=cls.FORM_SCRIPT
        )

    def form_update(self) -> Form:
        data = self.export()
        form_fiels = list()
        for item in self.FORM_FIELDS:
            form_fiels.append(item._replace(default=data.get(item.name, item.default)))
        form_fiels.append(Form.Hidden('key', config='required', default=getattr(self, 'key')))
        return Form(
            title=f'Atualizar {self.SINGULAR}',
            id=f'{self.item_name()}-update',
            method='post',
            action=self.update_path(),
            form_fields=form_fiels,
            update_form=True,
            script=self.FORM_SCRIPT
        )

    @classmethod
    def template_data(cls, request: Request) -> dict[str, Union[Request, 'BaseModel', ChainMap[str, 'BaseModel']]]:
        return {
            'request': request,
            'model': cls,
            'models': MODEL_MAP
        }

    async def detail_html(self) -> Markup:
        return Markup(Detail(instance=self))




    # @classmethod
    # async def detail_response(cls, request: Request, status_code: int = 200) -> TemplateResponse:
    #     async def run():
    #         instance = await cls.item(request.path_params.get('key'))
    #         return templates.TemplateResponse('model/detail.jj', {
    #             'instance': instance,
    #             'detail': await instance.detail_html(),
    #             **instance.template_data(request)
    #         }, status_code=status_code)
    #     try:
    #         return await run()
    #     except BaseException as e:
    #         print(e)
    #         await cls.context_update()
    #         return await run()



    # @classmethod
    # async def search_response(cls, request: Request) -> TemplateResponse:
    #     await cls.context_update()
    #     keys, items = dict(), list()
    #     for item, value in request.query_params.items():
    #         if value:
    #             keys[f'{item}?contains'] = normalize(value)
    #     if keys:
    #         items = await cls.items(query=keys)
    #     return templates.TemplateResponse('model/partial/search.jj', {
    #         'instances': items,
    #         **cls.template_data(request)
    #     })

