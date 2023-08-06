__all__ = [
    'Form',
    'FormField',
    'Index',
    'Anchor',
    'Option',
    'Card',
    'Detail',
    'LocalDate',
    'Payment',
    'CardFooter',
    'CardImage',
    'CardText',
    'CardTitle',
    'CardHeader',
    'CardSubtitle',
    'Property',
    'Title',
    'Table',
    'Select',
    'TextArea',
    'Input',
    'Hidden',
    'Checkbox',
    'Money',
    'View',
    'Paragraph',
    'QueryItem',
    'QueryString',
    'Month',
    'ListGroupItem',
    'ListGroup'
]

from .types import *
from .enums import *
from .function import *
from .context import *


class ListGroupItem(NamedTuple):
    content: str
    bootstrap: str = ''

    def __str__(self):
        return f'<li class="list-group-item {self.bootstrap} ms-2">{self.content}</li>'


class ListGroup(NamedTuple):
    title: 'Title'
    items: list[Union[ListGroupItem, 'ListGroup']]
    bootstrap: str = ''

    def __str__(self):
        items = ''.join([str(item) for item in self.items])
        return f'{str(self.title)}<ul class="list-group {self.bootstrap} ms-4 mb-2">{items}</ul>'


class View(NamedTuple):

    class Base(NamedTuple):
        properties: list['Property']
        buttons: list['Anchor']
        query: str = None

    class Detail(Base):
        update: bool = True
        delete: bool = False

    class List(Base):
        pass

    class Table(Base):
        pass

    model: Callable
    form_fiels: list['Form.FieldHTML']
    detail: Detail
    list: List
    table: Table

    async def instance(self, request: Request):
        try:
            return self.model(**ctx.get(self.model.CONTEXT_VAR)[self.key_name])
        except BaseException as e:
            print(e)
            return await self.model.item(key=request.path_params[self.key_name])

    @property
    def key_name(self):
        return self.model.key_name()

    @property
    def item_name(self):
        return self.model.item_name()

    @staticmethod
    def query_params(request: Request):
        return {**request.query_params}

    def model_fields(self):
        return fields(self.model)

    def detail_url(self, request: Request):
        return request.url_for(f'{self.item_name}:detail', **{self.key_name: request.path_params[self.key_name]})

    def update_url(self, request: Request):
        return request.url_for(f'{self.item_name}:update', **{self.key_name: request.path_params[self.key_name]})

    def delete_url(self, request: Request):
        return request.url_for(f'{self.item_name}:delete', **{self.key_name: request.path_params[self.key_name]})


    @staticmethod
    def template_path(name: str):
        return f'model/{name}.jj'

    async def form_new(self, request: Request) -> 'Form':
        return Form(
            title=f'Adicionar {self.model.SINGULAR}',
            id=f'{self.item_name}-new',
            method='post',
            action=request.url_for(f'{self.item_name}:new'),
            form_fields=self.form_fiels
        )

    async def form_update(self, request: Request) -> 'Form':
        instance = await self.instance(request)
        form_fields: list['Form.FieldHTML'] = [item._replace(default=get_attribute(instance, item.name)) for item in self.form_fiels if item.update]
        form_fields.extend([Form.Hidden(item.name, default=get_attribute(instance, item.name)) for item in self.form_fiels if not item.update])
        form_fields.append(Form.Hidden('key', config='required', default=instance.key))
        return Form(
            title=f'Atualizar {self.model.SINGULAR}',
            id=f'{self.item_name}-update',
            method='post',
            action=request.url_for(f'{self.item_name}:update', **{self.key_name: request.path_params[self.key_name]}),
            form_fields=self.form_fiels
        )


class Month(NamedTuple):
    integer: int

    def __str__(self):
        months = {
            1: 'Janeiro',
            2: 'Fevereiro',
            3: 'Março',
            4: 'Abril',
            5: 'Maio',
            6: 'Junho',
            7: 'Julho',
            8: 'Agosto',
            9: 'Setembro',
            10: 'Outubro',
            11: 'Novembro',
            12: 'Dezembro'
        }
        return months[self.integer]


class Money(NamedTuple):
    value: Union[float, int]

    def __str__(self):
        return f'R$ {self.value}'


class LocalDate(NamedTuple):
    date: datetime.date
    short: bool = False

    def __str__(self):
        if self.short:
            return f'{add_zero_if_len_one(str(self.date.day))}/{add_zero_if_len_one(str(self.date.month))}/{self.date.year}'
        return f'{self.date.day} de {Month(self.date.month)} de {self.date.year}'


class Payment(NamedTuple):
    date: datetime.date
    value: Union[float, int]
    method: PaymentMethod

    def __str__(self):
        return f'{LocalDate(self.date)}, {self.method.value}, R$ {self.value}'


class Title(NamedTuple):
    content: str
    size: int = 3
    bootstrap: str = 'bg-primary text-white pt-2'

    def __str__(self):
        return f'<h{self.size} class="{self.bootstrap}">{self.content}</h{self.size}>'


# class RouteNames(NamedTuple):
#     index: str
#     detail: str
#     list: str
#     new: str
#     update: str
#     delete: str
#     search: str
#     table: str
#
#     @classmethod
#     def defaults(cls, item_name: str):
#         return [f'{item_name}:index', f'{item_name}:detail', f'{item_name}:list', f'{item_name}:new', f'{item_name}:update',
#                 f'{item_name}:delete', f'{item_name}:search', f'{item_name}:table']
#
#     @classmethod
#     def construct(cls, item_name: str):
#         return cls(*cls.defaults(item_name))


class Option(NamedTuple):
    name: str = ''
    label: str = ''

    def __str__(self):
        return self.html()

    @staticmethod
    def make_options(data: list[tuple[str, str]]):
        text = Option(label='').html()
        for item in data:
            text += Option(item[0], item[1]).html()
        return text

    def html(self):
        if not self.name and not self.label:
            return f'<option></option>'
        return f'<option value="{self.name}">{self.label}</option>'


class Form(NamedTuple):
    title: str
    id: str
    action: Optional[str] = None
    route: Optional[str] = None
    query_params: Optional[list[dict[str, str]]] = None
    path_params: Optional[list[dict[str, str]]] = None
    request: Optional[Request] = None
    method: Literal['get', 'post', 'hx-get', 'hx-post'] = 'get'
    config: Optional[str] = None
    form_fields: list['Form.FieldHTML'] = None
    update_form: bool = False
    script: str = None

    class FieldHTML(NamedTuple):
        name: str
        label: str = None
        config: str = ''
        default: Union[Coroutine, Callable, str] = ''
        bootstrap: str = 'form-control'
        container: str = 'form-floating mb-2'
        options: Union[Coroutine, Callable, str] = ''
        type: str = 'text'
        height: int = 200
        update: bool = True
        table: bool = True
        detail: bool = True


        @staticmethod
        async def resolve(value: Union[Coroutine, Callable, str, bool]) -> str:
            if isinstance(value, str):
                return value
            else:
                try:
                    result = await value()
                    return result
                except:
                    try:
                        result = value()
                        return result
                    except:
                        return value

        async def content(self):
            return await self.resolve(self.default)

        def _config(self, update_form: bool):
            config = self.config
            if self.tag == 'input':
                config += f' type="{self.type}"'
            if update_form:
                if not self.update:
                    return f'{config} disabled'
            return config

        @property
        def tag(self):
            return type(self).__name__.lower()

        async def html(self, update_form: bool = True):
            content = await self.content()
            config = self._config(update_form)
            text = ''
            if 'disabled' in config:
                text += f'<input type="hidden" name="{self.name}" value="{await self.resolve(self.default)}">'
                if self.tag == 'input':
                    text += f'<div class="{self.container}">' \
                            f'<{self.tag} id="{self.name}" name="{self.name}" class="{self.bootstrap}" value="{await self.resolve(self.default)}" {config} style>' \
                            f'{content}' \
                            f'<label for="{self.name}">{self.label or self.name}</label>' \
                            f'</div>'
                else:
                    text += f'<div class="{self.container}">' \
                       f'<{self.tag} id="{self.name}" class="{self.bootstrap}" {config} style>' \
                       f'{content}' \
                       f'</{self.tag}>' \
                       f'<label for="{self.name}">{self.label or self.name}</label>' \
                       f'</div>'
            else:
                if self.tag == 'input':
                    text = f'<div class="{self.container}">' \
                           f'<{self.tag} name="{self.name}" id="{self.name}" class="{self.bootstrap}" value="{await self.resolve(self.default)}" {config} style>' \
                           f'{content}' \
                           f'<label for="{self.name}">{self.label or self.name}</label>' \
                           f'</div>'
                else:
                    text = f'<div class="{self.container}">' \
                           f'<{self.tag} name="{self.name}" id="{self.name}" class="{self.bootstrap}" {config} style>' \
                           f'{content}' \
                           f'</{self.tag}>' \
                           f'<label for="{self.name}">{self.label or self.name}</label>' \
                           f'</div>'
            return text

    class TextArea(FieldHTML):

        async def html(self, update_form: bool = True):
            text = await super().html()
            text = text.replace('style', f'style="height:{self.height}px"')
            return text

        def _config(self, update_form: bool = True):
            config = super()._config(update_form)
            return f'{config} placeholder="{self.name}"'

    class Select(FieldHTML):

        def _config(self, update_form: bool = True):
            config = super()._config(update_form)
            return f'{config} placeholder="{self.name}"'

        async def content(self):
            default = await self.resolve(self.default)
            options = await self.resolve(self.options)
            if default:
                options = options.replace(f'{default}"', f'{default}" selected')
            return options

    class Input(Select):

        async def content(self):
            if self.options:
                options = await self.resolve(self.options)
                return f'<datalist id="{self.name}_list">{options}</datalist>'
            return ''

        # async def html(self, update_form: bool = True):
        #     content = await self.content()
        #     config = self._config(update_form) + f' value="{await self.resolve(self.default)}"'
        #     return f'<div class="{self.container}">' \
        #            f'<{self.tag} type="{self.type}" name="{self.name}" id="{self.name}" class="{self.bootstrap}" {config}>' \
        #            f'{content}' \
        #            f'<label for="{self.name}">{self.label or self.name}</label>' \
        #            f'</div>'

    class Hidden(Input):

        async def html(self, update_form: bool = True):
            config = self.config + f' value="{await self.resolve(self.default)}"'
            return f'<input type="hidden" name="{self.name}" id="{self.name}" {config}>'

    class Checkbox(Input):
        type: str = 'checkbox'
        container: str = 'form-check form-switch mb-2'
        bootstrap: str = 'form-check-input'

        def _config(self, update_form: bool = True):
            config = super()._config(update_form)
            if self.default:
                config += ' checked'
            return config

        async def html(self, update_form: bool = True):
            config = self._config(update_form) + ' role="switch"'
            return f'<div class="{self.container}">' \
                   f'<input type="checkbox" name="{self.name}" id="{self.name}" class="{self.bootstrap}" {config}>' \
                   f'<label for="{self.name}" class="text-white">{self.label or self.name}</label>' \
                   f'</div>'

    async def setup_fields(self):
        text = ''
        for item in self.form_fields:
            text += await item.html(update_form=self.update_form)
        return text

    def creator(self, request: Request):
        field_names = [item.name for item in self.form_fields]
        if 'creator' in field_names:
            user_key = request.session.get("user", {}).get("key")
            return f'<input type="hidden" value="{user_key}" name="creator">'
        return ''

    async def html(self, request: Request):
        fields = await self.setup_fields()
        return Markup(f"""
        <div class="mt-2 bg-dark bg-opacity-25">
        <h4 class="bg-dark text-white p-3">{self.title}</h4>
        <form id="{self.id}" action="{self.action}" method="{self.method}" class="p-3">
        <input type="hidden" name="csrftoken" value="{request.scope.get('csrftoken')()}">
        {fields}{self.creator(request)}
        <button class="btn btn-primary form-control">ENVIAR</button>
        </form>
        </div>
        <script>{self.script or ""}</script>""")


FormField = Form.FieldHTML
Select = Form.Select
Input = Form.Input
Checkbox = Form.Checkbox
TextArea = Form.TextArea
Hidden = Form.Hidden


class Paragraph(NamedTuple):
    content: str = None
    id: str = None
    bootstrap: str = None

    def __str__(self):
        bootstrap = f' class="{self.bootstrap}"' if self.bootstrap else ""
        id = f' id="{self.id}"' if self.id else ""
        content = self.content or ''
        return f'<p{id}{bootstrap}>{content}</p>'


class Index(NamedTuple):
    model: 'BaseModel'

    def html(self, info: str = ''):
        return Markup(f"""
        <div class="bg-secondary bg-opacity-50 p-3">
        <form id="{self.model.item_name()}-search-form">
            <input name="{self.model.search_param()}" 
            hx-get="{self.model.search_path()}" 
            hx-target="#{self.model.item_name()}-search-result"
            hx-trigger="keyup changed delay:300ms" 
            hx-indicator="#{self.model.item_name()}-indicator" 
            placeholder="buscar {self.model.SINGULAR.lower()}" 
            class="form-control text-center">
        </form>
        </div>
        <div id="{self.model.item_name()}-search-result" class="list-group">
        {info}
        </div>
        """)


class QueryItem(NamedTuple):
    key: str
    value: str

    def __str__(self):
        return f'{self.key}={self.value}'


class QueryString(NamedTuple):
    items: list[QueryItem] = None

    def __str__(self):
        if not self.items:
            return ''
        return f'?{"&".join([str(item) for item in self.items])}'


class Anchor(NamedTuple):
    content: str
    url: str = None
    route: str = None
    request: Request = None
    instance: Any = None
    path_params: list[str] = None
    query_params: list[str] = None
    container: Literal['card', 'nav', 'list-group', 'button'] = 'list-group'
    bootstrap: str = ''

    def _class(self):
        if self.container == 'list-group':
            return f'{self.container}-item {self.container}-item-action'
        elif self.container == 'button':
            if self.bootstrap != '':
                return f'{self.bootstrap}'
            else:
                return 'btn btn-primary me-2'
        else:
            return f'{self.container}-link'

    def _url(self):
        if self.url:
            return self.url
        else:
            if self.path_params:
                return f'{self.request.url_for(self.route, **{item: get_attribute(self.instance, item) for item in self.path_params})}{self.query()}'
            else:
                return f'{self.request.url_for(self.route)}{self.query()}'

    def _query_items(self):
        if self.query_params:
            return '&'.join([str(QueryItem(key=key, value=value)) for key, value in {item: get_attribute(self.instance, item) for item in self.query_params}.items()])
        return None

    def query(self):
        if self._query_items():
            return f'?{self._query_items()}'
        return ''

    def __str__(self):
        return f'<a class="{self._class()} {self.bootstrap}" href="{self._url()}">{self.content}</a>'


class CardText(NamedTuple):
    label: str
    content: str
    bootstrap: str = ''

    def __str__(self):
        return f'<p class="card-text {self.bootstrap}">' \
               f'<span class="text-muted" style="text-variation: small-caps">{self.label}:</span> ' \
               f'<b>{self.content}</b>' \
               f'</p>'


class CardTitle(NamedTuple):
    content: str
    size: int = 3
    bootstrap: str = ''

    def __str__(self):
        return f'<h{self.size} class="card-title {self.bootstrap}">{self.content}</h{self.size}>'


class CardSubtitle(NamedTuple):
    content: str
    size: int = 6
    bootstrap: str = 'mb-2 text-muted'

    def __str__(self):
        return f'<h{self.size} class="card-subtitle {self.bootstrap}">{self.content}</h{self.size}>'


class CardHeader(NamedTuple):
    content: str
    bootstrap: str = ''

    def __str__(self):
        return f'<div class="card-header {self.bootstrap}">{self.content}</div>'


class CardFooter(NamedTuple):
    content: str
    bootstrap: str = ''

    def __str__(self):
        return f'<div class="card-footer {self.bootstrap}">{self.content}</div>'


class CardImage(NamedTuple):
    url: str
    alt: str = ''
    position: Literal['top', 'bottom'] = 'top'
    bootstrap: str = ''

    def __str__(self):
        return f'<img src="{self.url}" class="card-img-{self.position} {self.bootstrap}" alt="{self.alt}">'


class Property(NamedTuple):
    label: str
    name: str


class Card(NamedTuple):
    width: str = None
    title: str = None
    title_size: int = 3
    subtitle: str = None
    content: str = None
    props: list[Property] = None
    img: Union[Url, str] = None
    links: list[Anchor] = None
    buttons: list[Anchor] = None
    header: str = None
    footer: str = None
    bootstrap: str = 'text-bg-light'
    instance: Any = None

    class Header(CardHeader):
        pass

    class Anchor(Anchor):
        container = 'card'

    class Title(CardTitle):
        pass

    class Text(CardText):
        pass

    class Footer(CardFooter):
        pass

    class Image(CardImage):
        pass

    def _title(self):
        if self.title:
            return str(CardTitle(self.title, self.title_size))
        return ''

    def _subtitle(self):
        if self.subtitle:
            return str(CardSubtitle(self.subtitle))
        return ''

    def _links(self):
        if self.links:
            text = ''
            for item in self.links:
                text += str(Anchor(content=item[0], url=item[1], container='card'))
            return text
        return ''

    def _props(self):
        text = ''
        if self.props:
            for prop in self.props:
                text += CardText(prop.label, get_attribute(self.instance, prop.name))
        return text

    def _buttons(self):
        if self.buttons:
            text = ''
            for item in self.buttons:
                text += str(Anchor(content=item.content, url=item._url(), container='button', bootstrap=item.bootstrap))
            return text
        return ''

    def _content(self):
        if self.content:
            return self.content
        return ''

    def _header(self):
        if self.header:
            return str(CardHeader(self.header))
        return ''

    def _footer(self):
        if self.footer:
            return str(CardFooter(self.footer))
        return ''

    def _img(self):
        if self.img:
            return
        return ''

    def _width(self):
        if self.width:
            return f'style="width: {self.width}"'
        return ''

    def _body(self):
        return f'<div class="card-body">{self._title()}{self._subtitle()}' \
               f'<hr>{self._content()}{self._links()}{self._buttons()}</div>'

    def __str__(self):
        return f'<div class="card {self.bootstrap} mt-3" {self._width()}>' \
               f'{self._header()}{self._img()}{self._body()}{self._footer()}</div>'


class Detail(NamedTuple):
    instance: 'BaseModel'
    content: str = ''
    width: str = None
    header: str = None
    footer: str = None
    # update: bool = True
    # delete: bool = False

    class Property(Property):
        pass

    @staticmethod
    def paragraph(label: str, value: Any):
        if value != '':
            text = str(CardText(label=label, content=value))
            text = text.replace('True', 'Sim').replace('False', 'Não')
            return text
        return ''

    def detail_properties(self):
        text = ''
        if self.instance.DETAIL_PROPERTIES:
            for item in self.instance.DETAIL_PROPERTIES:
                text += self.paragraph(label=item.label, value=get_attribute(self.instance, item.name))
        return text

    def update_button(self) -> Optional[Anchor]:
        if self.instance.UPDATE_BUTTON:
            return Anchor(url=self.instance.update_path(),
                          content='Atualizar', container='button', bootstrap='btn btn-warning me-2')
        return None

    def delete_button(self) -> Optional[Anchor]:
        if self.instance.DELETE_BUTTON:
            return Anchor(url=self.instance.delete_path(),
                          content='Excluir', container='button', bootstrap='btn btn-danger me-2')
        return None

    def detail_buttons(self) -> list[Anchor]:
        if self.instance.DETAIL_BUTTONS:
            return [Anchor(content=item.content, url=item.detail_path(), instance=self.instance,
                           route=item.route, container='button') for item in self.instance.DETAIL_BUTTONS]
        return list()

    def buttons(self) -> list[Anchor]:
        buttons = [item for item in [self.update_button(), self.delete_button(), *self.detail_buttons()] if item is not None]
        return [item for item in buttons if item is not False]

    def __str__(self):
        return Card(
            header=self.header or f'Cadastro de {self.instance.SINGULAR}',
            title=str(self.instance),
            subtitle=f'Chave {self.instance.key}',
            content=self.content + self.detail_properties(),
            buttons=self.buttons(),
            width=self.width,
            footer=self.footer,
            instance=self.instance
            ).__str__()


class Table(NamedTuple):
    request: Request
    endpoint: Any
    instances: list[Any]
    thead: list[Union['Table.THead', Property]]

    class THead(NamedTuple):
        label: str
        name: str

    def __str__(self):
        return f'<table class="container">{self._thead() + self._tbody()}</table>'

    @property
    def properties(self):
        if self.thead:
            return self.thead
        field_tables = [Property(item.label, item.name) for item in self.endpoint.MODEL.FORM_FIELDS if item.table]
        table_properties = self.thead or list()
        names = [item.name for item in table_properties]
        return [*table_properties, *[item for item in field_tables if item.name not in names]]

    def _thead(self):
        text = '<thead id="table-head" class="bg-dark text-white mt-5 p-1"><tr>'
        for item in self.properties:
            text += f'<th scope="col" class="p-1 border-end border-white" style="font-variant: small-caps">{item.label}</th>'
        return text

    def _tbody_tr_item(self, instance):
        text = '<tr>'
        for item in self.properties:
            text += f'<td class="text-white p-1 border-end border-secondary">{get_attribute(instance, item.name)}</td>'
        text += '</tr>'
        return text

    def _tbody(self):
        text = '<tbody  style="overflow: auto" class="bg-dark bg-opacity-75">'
        for instance in self.instances:
            text += self._tbody_tr_item(instance)
        text += '</tbody>'
        return text


