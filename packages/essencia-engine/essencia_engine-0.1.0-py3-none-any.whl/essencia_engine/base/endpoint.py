
__all__ = [
    'BaseEndpoint',
    'Home'
]

from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from .types import *
from .function import *
from .setup import *
from .context import *
from .ntuple import *
from .model import BaseModel


class Home(HTTPEndpoint):
    async def get(self, request: Request):
        await ModelContext.update_all()
        return templates.TemplateResponse('index.jj', {'request': request})

    @classmethod
    def routes(cls):
        return [
            Route('/', cls, name='home'),
            Mount('/static', app=static, name='static')
        ]


class BaseEndpoint(HTTPEndpoint):
    MODEL: ClassVar['BaseModel']
    INITIAL_ROUTES: list[Mount, Route] = None

    @classmethod
    async def json_data_response(cls, request: Request) -> JSONResponse:
        instances = await cls.MODEL.items({**request.query_params})
        return JSONResponse({item.key: item.json() for item in instances})

    @classmethod
    async def json_list_response(cls, request: Request) -> JSONResponse:
        instances = await cls.MODEL.items({**request.query_params})
        return JSONResponse([{**item.json(), 'str': str(item)} for item in instances])

    @classmethod
    async def json_detail_response(cls, request: Request) -> JSONResponse:
        instance = await cls.MODEL.item(request.path_params.get('key'))
        return JSONResponse(instance.json())


    @classmethod
    def additional_routes(cls) -> list[Mount, Route]:
        return list()

    @classmethod
    def additional_partial_routes(cls) -> list[Mount, Route]:
        return list()

    @classmethod
    def additional_json_routes(cls) -> list[Mount, Route]:
        return list()

    @classmethod
    async def item(cls, key: str):
        return await cls.MODEL.item(key)

    @classmethod
    def model_query(cls):
        return cls.MODEL.DETA_QUERY or dict()

    @classmethod
    async def items(cls, request: Request):
        query = cls.model_query()
        query.update(request.query_params)
        return await cls.MODEL.items(query)

    @classmethod
    def initial_routes(cls):
        MODEL_MAP[cls.MODEL.__name__] = cls.MODEL
        return cls.INITIAL_ROUTES or list()

    @classmethod
    async def context_update(cls):
        if cls.MODEL.CONTEXT_TABLES:
            await ctx_update(cls.MODEL.CONTEXT_TABLES)
        else:
            await ctx_update()

    @classmethod
    def model(cls):
        return cls.MODEL

    @classmethod
    async def query_title(cls, request: Request, models: list['BaseModel'] = None) -> str:
        query_title = ''
        if models:
            for item in request.query_params:
                for model in models:
                    if model.key_name() == item:
                        query_title += str(Title(
                            content=f"{cls.MODEL.PLURAL} de {str(await model.item(request.query_params.get(item)))}"))
        return query_title

    @classmethod
    def index_info(cls):
        paragraph1 = Paragraph(
            f'Aqui você tem acesso ao portal de {cls.MODEL.PLURAL.lower()} do sistema. No campo acima, '
            f'busque os itens {cls.MODEL.PLURAL.lower()} já '
            f'cadastrados e clique no nome do objeto {cls.MODEL.SINGULAR.lower()} '
            f'encontrado para acessar informações detalhadas sobre o objeto.')
        paragraph2 = Paragraph('Caso seja necessário voltar para esta página, clique em <span class="text-primary">'
                               '"Buscar"</span>.')
        paragraph4 = Paragraph(f'Na opção <span class="text-primary">"Listar"</span> você terá uma lista dos '
                               f'itens {cls.MODEL.PLURAL.lower()} salvos.')
        paragraph3 = Paragraph(f'Em <span class="text-primary">"Adicionar"</span> é possível salvar um novo objeto.')
        paragraph5 = Paragraph(f'Por fim, em <span class="text-primary">"Tabela"</span> terá acesso a informações '
                               f'dos itens {cls.MODEL.PLURAL.lower()}.')
        return Card(
            title=f'Informações sobre o painel de {cls.MODEL.PLURAL}',
            title_size=3,
            content=str(paragraph1) + str(paragraph2) + str(paragraph3) + str(paragraph4) + str(paragraph5)
        )


    @classmethod
    def index_html(cls):
        index = Index(cls.model())
        return index.html(str(cls.index_info()))

    @classmethod
    async def index(cls, request: Request):
        return templates.TemplateResponse(
            'model/index.jj', {
                'index': Markup(cls.index_html()),
                **cls.MODEL.template_data(request=request),
            })

    @classmethod
    async def update_response(cls, request: Request) -> Union[TemplateResponse, Response]:
        await cls.context_update()
        if request.method == 'GET':
            instance = await cls.item(request.path_params.get('key'))
            return templates.TemplateResponse('model/update.jj', {
                'update_form': await instance.form_update().html(request=request),
                **cls.MODEL.template_data(request)
            })
        elif request.method == 'POST':
            instance = cls.MODEL(**await form_data(request=request))
            saved = await instance.save()
            if saved:
                return RedirectResponse(saved.detail_path(), 303)
            return HTMLResponse(
                'Infelizmente os dados não foram processados com sucesso. Por favor repetir a operação!')


    @classmethod
    async def detail_response(cls, request: Request, status_code: int = 200):
        await cls.context_update()
        instance = await cls.item(request.path_params.get('key'))
        return templates.TemplateResponse('model/detail.jj', {
            'instance': instance,
            'detail': await instance.detail_html(),
            **instance.template_data(request)
        }, status_code=status_code)

    @classmethod
    async def list_response(cls, request: Request) -> TemplateResponse:
        await cls.context_update()
        return templates.TemplateResponse('model/list.jj', {
            'instances': await cls.MODEL.items({**request.query_params}),
            **cls.MODEL.template_data(request)
        })

    @classmethod
    async def table(cls, request: Request):
        await cls.context_update()
        if request.query_params:
            query_params = {**request.query_params}
        else:
            query_params = {}
        instances = await cls.MODEL.items(query=query_params)
        return templates.TemplateResponse('model/table.jj', {
            **cls.MODEL.template_data(request),
            'query_title': Markup(await cls.query_title(request)),
            'table': Markup(str(Table(request, cls, instances,
                                      cls.MODEL.THEAD or cls.MODEL.DETAIL_PROPERTIES or cls.MODEL.thead()))),
        })

    @classmethod
    async def delete_response(cls, request: Request) -> TemplateResponse:
        await cls.context_update()
        if request.method == 'GET':
            instance = await cls.item(request.path_params.get('key'))
            return templates.TemplateResponse('model/delete.jj', {
                'instance': instance,
                **instance.template_data(request)
            })
        elif request.method == 'POST':
            instance = await cls.item(request.path_params.get('key'))
            await instance.delete()
            return await cls.list_response(request)

    @classmethod
    async def save_response(cls, request: Request) -> Union[Response, TemplateResponse]:
        await cls.context_update()
        if request.method == 'GET':
            return templates.TemplateResponse('model/new.jj', {
                'form': await cls.MODEL.form_new().html(request),
                **cls.MODEL.template_data(request)
            })
        elif request.method == 'POST':
            instance = cls.MODEL(** await form_data(request))
            exist = await instance.exist()
            if exist:
                return RedirectResponse(exist.detail_path(), 303)
            saved = await instance.save()
            if saved:
                return RedirectResponse(saved.detail_path(), 303)
            return HTMLResponse('Infelizmente os dados não foram processados com sucesso. Por favor repetir a operação!')


    # @classmethod
    # async def new_response(cls, request: Request):
    #     await cls.context_update()
    #     return await cls.MODEL.save_response(request=request)

    @classmethod
    async def search_response(cls, request: Request):
        await cls.context_update()
        query = {f'{cls.MODEL.SEARCH_PARAM}?contains': normalize(request.query_params.get(cls.MODEL.SEARCH_PARAM))}
        instances = await cls.MODEL.items(query)
        return templates.TemplateResponse('model/partial/search.jj', {
            'instances': instances,
            **cls.MODEL.template_data(request)
        })

    @classmethod
    async def search_partial_response(cls, request: Request):
        await cls.context_update()
        user = request.session.get('user')
        query = {f'{cls.MODEL.SEARCH_PARAM}?contains': normalize(request.query_params.get(cls.MODEL.SEARCH_PARAM))}
        instances = await cls.MODEL.items(query)
        content = templates.get_template('dashboard/search-result.jj').render({
            'request': request,
            'model': cls.MODEL,
            'instances': instances,
            'user': user
        })
        return HTMLResponse(Markup(content))


    @classmethod
    async def partial_list_response(cls, request: Request):
        await cls.context_update()
        return templates.TemplateResponse('model/partial/list.jj', {
            'instances': await cls.items(),
            **cls.MODEL.template_data(request)
        })
    @classmethod
    async def partial_detail_response(cls, request: Request):
        await cls.context_update()
        instance = await cls.item(request.path_params.get('key'))
        return templates.TemplateResponse('model/partial/detail.jj', {
            'instance': instance,
            'detail': await instance.detail_html(),
            **instance.template_data(request)
        })

    @classmethod
    def routes(cls):
        return [
            *cls.initial_routes(),
            Mount(f'/{cls.MODEL.item_name()}', name=cls.MODEL.item_name(), routes=[
                Mount('/partial', name='partial', routes=[
                    Route('/list', cls.partial_list_response, name='list'),
                    Route('/search', cls.search_partial_response, name='search'),
                    *cls.additional_partial_routes(),
                    Route('/{key}', cls.partial_detail_response, name='detail'),
                ]),
                Mount('/json', name='json', routes=[
                    Route('/list', cls.json_list_response, name='list'),
                    Route('/data', cls.json_data_response, name='data'),
                    Route('/search', cls.search_partial_response, name='search'),
                    *cls.additional_json_routes(),
                    Route('/{key}', cls.json_detail_response, name='detail'),
                ]),
                Route('/index', cls.index, name='index'),
                Route('/search', cls.search_response, name='search'),
                Route('/list', cls.list_response, name='list'),
                Route('/table', cls.table, name='table'),
                Route('/new', cls.save_response, name='new', methods=['GET', 'POST']),
                Route('/update/{key}', cls.update_response, name='update', methods=['GET', 'POST']),
                Route('/delete/{key}', cls.delete_response, name='delete', methods=['GET', 'POST']),
                *cls.additional_routes(),
                Route('/{key}', cls.detail_response, name='detail', methods=['GET']),
            ])

        ]

    # @classmethod
    # def route_names(cls):
    #     return RouteNames.construct(cls.MODEL.item_name())
    #
