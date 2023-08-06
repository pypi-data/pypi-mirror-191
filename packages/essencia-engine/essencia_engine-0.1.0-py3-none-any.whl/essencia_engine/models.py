__all__ = [
    'Person',
]

import asyncio

from .base.enums import *
from .base.types import *
from .base.context import *
from .base.function import *
from .base.ntuple import *
from .base.database import *
from .base.setup import *
from .base.security import *
from .base.model import BaseModel, Key


class Profile:
    TABLES = ['Patient', 'Employee', 'Doctor', 'Therapist']

    class Table(NamedTuple):
        name: str

        def __str__(self):
            return 'Paciente' if self.name == 'Patient' else 'Médico' if self.name == 'Doctor' else 'Terapeuta' if self.name == 'Therapist' else 'Funcionário'

    def __init__(self, **kwargs):
        self.person_key = kwargs.get('person_key')
        self.key = kwargs.get('key')
        self.search = kwargs.get('search')
        self.model = kwargs.get('model')

    @staticmethod
    async def items(tables: list[str] = None) -> list['Profile']:
        table_names = tables or Profile.TABLES
        await ctx_update([*table_names, 'Person'])
        data = list()
        for item in table_names:
            data.extend([Profile(**x, model=item) for x in templates.env.globals[item].values()])
        return data

    def __str__(self):
        return f'{self.person} ({Profile.Table(self.model)})'

    @property
    def person(self):
        return Person(**templates.env.globals['Person'].get(self.person_key))

    @property
    def option(self):
        return f'<option value="{self.model}.{self.key}">{str(self)}</option>'

    @classmethod
    async def select_options(cls):
        return ''.join([item.option for item in await Profile.items()])


@dataclass
class Person(BaseModel):
    SINGULAR = 'Pessoa'
    PLURAL = 'Pessoas'
    SORT_ATTRIBUTE = 'search_name'
    SEARCH_PARAM = 'search_name'
    CONTEXT_VAR = person_var
    EXIST_PARAMS = ['code', 'cpf']
    DELETE_BUTTON = False
    UPDATE_BUTTON = True
    DETAIL_PROPERTIES = [
        Property('Nome de Registro', 'full_name'),
        Property('Data de Nascimento', 'bdate_format'),
        Property('Idade', 'age_format'),
        Property('Gênero', 'gender_value'),
        Property('CPF', 'cpf_format'),
        Property('Nome social', 'social_name'),
        Property('Transgênero', 'is_transgender'),
        Property('Não Binário', 'is_non_binary'),
    ]
    FORM_FIELDS = [
        Form.Input(name='fname', label='Primeiro Nome', config='required'),
        Form.Input(name='lname', label='Segundo Nome', config='required'),
        Form.Input(name='bdate', label='Nascimento', config='required', type='date'),
        Form.Select(name='gender', label='Gênero', config='required', options=Gender.select_options),
        Form.Input(name='cpf', label='CPF'),
        Form.Checkbox(name='transgender', label='Transgênero', default=False),
        Form.Checkbox(name='non_binary', label='Não Binário', default=False),
        Form.Input(name='name', label='Nome Social')
    ]

    fname: str
    lname: str
    bdate: datetime.date
    gender: Gender
    transgender: bool = False
    non_binary: bool = False
    code: str = None
    name: str = None
    cpf: str = None
    search_name: str = None
    key: str = None

    @property
    def full_name(self):
        return f'{self.fname} {self.lname}'

    @property
    def social_name(self):
        if self.name:
            return self.name
        else:
            return '-'

    def __lt__(self, other):
        return normalize(str(self)) < normalize(str(other))

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f'{self.fname} {self.lname}'

    @property
    def bdate_format(self):
        return LocalDate(self.bdate)

    @property
    def cpf_format(self):
        if self.cpf:
            return f'{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}'
        return '-'

    @property
    def is_transgender(self):
        return 'Sim' if self.transgender else 'Não'

    @property
    def is_non_binary(self):
        return 'Sim' if self.non_binary else 'Não'

    @property
    def gender_value(self):
        return self.gender.value

    @property
    def gender_name(self):
        return self.gender.name

    @property
    def age_format(self):
        return f'{self.age} anos'

    @property
    def age(self):
        return ((datetime.date.today() - self.bdate).days / 365).__round__(2)

    @property
    def person_key(self):
        return self.key

    def make_code(self):
        return ''.join(normalize(''.join(
            [self.gender.name, str(self.bdate).replace('-', ''), self.fname[:2], self.lname.split()[-1][:2]])).upper().split())

    def __post_init__(self):
        self.fname = self.fname.strip()
        self.lname = self.lname.strip()
        if self.name:
            self.search_name = normalize(f'{self.fname} {self.lname}; {self.name}')
        else:
            self.search_name = normalize(f'{self.fname} {self.lname}')
        if isinstance(self.gender, str):
            self.gender = Gender[self.gender]
        if isinstance(self.bdate, str):
            self.bdate = datetime.date.fromisoformat(self.bdate)
        self.code = self.make_code()
        if isinstance(self.cpf, str):
            cpf = ''.join([caracter for caracter in self.cpf if caracter.isdigit()])
            if len(cpf) > 0:
                assert len(cpf) == 11, 'o cpf deve conter 11 dígitos'
                self.cpf = cpf


class SelectOption:
    @classmethod
    async def providers(cls):
        doctor = await Doctor.select_options()
        therapist = (await Therapist.select_options()).replace('<option></option>', '')
        return doctor + therapist

    @classmethod
    async def workers(cls):
        text = ''
        text += await Assistant.select_options()
        text += await Employee.select_options()
        text = text.replace('<option></option>', '')
        return text

    @classmethod
    async def profiles(cls):
        data = list()
        for model in [Patient, Doctor, Therapist, Assistant, Employee]:
            items = await model.items()
            print(items)
            data.extend([Option(f'{model.__name__}.{item.key}', f'{str(item)} ({model.__name__})') for item in items])
        print(data)
        try:
            text = Option().html()
            text += ''.join([item.html() for item in data])
            print(text)
            return text
        except BaseException as e:
            print(e)


@dataclass
class Address(BaseModel):
    person_key: str = None
    street: str = None
    house: str = None  # número, quadra, lote
    district: str = None
    city: str = None
    cep: str = None
    key: str = None

    def __str__(self):
        text = ''
        for item in fields(self):
            if item.name not in ['person_key', 'key']:
                value = getattr(self, item.name)
                if value not in [None, '']:
                    text += f'{value}, '
        return text[:-2]


@dataclass
class CPF(BaseModel):
    person_key: str = None
    value: str = None
    key: str = None

    def __str__(self):
        return self.value

    def __post_init__(self):
        if self.value:
            self.value = ''.join([x for x in self.value if str.isalnum(x)])
            assert len(self.value) == 11
        self.key = self.person_key


@dataclass
class Phone(CPF):
    def __post_init__(self):
        if self.value:
            self.value = ''.join([x for x in self.value if str.isalnum(x)])
            assert len(self.value) in [10, 11, 15]


@dataclass
class Email(CPF):
    def __post_init__(self):
        if self.value:
            assert '@' in self.value
            assert len(self.value.split('@')) == 2
            self.value = self.value.strip()


@dataclass
class BaseProfile(BaseModel):
    SEARCH_PARAM = 'search'
    EXIST_PARAMS = 'person_key'
    CONTEXT_TABLES = ['Person']
    DETAIL_PROPERTIES = [
        Property('Pessoa', 'person_link'),
        Property('Idade', 'age_format'),
        Property('Nascimento', 'bdate_format'),
        Property('Telefone', 'phone'),
        Property('Email', 'email'),
        Property('Endereço', 'address'),
        Property('Cidade', 'city'),
        Property('Observações', 'notes'),
    ]
    FORM_FIELDS = [
        Form.Select(name='person_key', label='Pessoa', options=Person.select_options, config='required ', update=False),
        Form.Input('phone', 'Telefone'),
        Form.Input('email', 'Email'),
        Form.Input('address', 'Endereço'),
        Form.Input('city', 'Cidade'),
        Form.TextArea(name='notes', label='Observações', height=100)
    ]
    DELETE_BUTTON = False

    person_key: Key('Person')
    phone: str = None
    email: str = None
    address: str = None
    city: str = None
    notes: str = None
    search: str = None
    key: str = None

    def __str__(self):
        return str(getattr(self, 'person'))


    def json(self):
        item = super().json()
        item['person'] = self.person.json()
        return item

    @classmethod
    async def person_data_from_database(cls):
        return {item['key']: item for item in await async_deta('Person')}

    async def person_from_database(self):
        return await async_deta('Person', key=self.person_key)

    @property
    def person_link(self):
        return Markup(f'<a href="/person/{self.person_key}">{getattr(self, "person")}</a>')

    @property
    def full_name(self):
        return str(getattr(self, "person"))

    @property
    def bdate(self):
        return self.person.bdate

    @property
    def bdate_format(self):
        return LocalDate(self.person.bdate)

    @property
    def age_format(self):
        return f'{self.age} anos'

    @property
    def gender(self):
        return self.person.gender

    @property
    def gender_value(self):
        return self.person.gender.value

    @property
    def gender_name(self):
        return self.gender.name

    @property
    def age(self):
        return self.person.age

    def __lt__(self, other):
        return normalize(str(self)) < normalize(str(other))


@dataclass
class Patient(BaseProfile):
    SINGULAR = 'Paciente'
    PLURAL = 'Pacientes'

    @property
    def patient_key(self):
        return getattr(self, 'key')


@dataclass
class Facility(BaseModel):
    SINGULAR = 'Empresa'
    PLURAL = 'Empresas'
    SEARCH = 'search'

    FORM_FIELDS = [
        Input('name', 'Nome da Empresa', config='required'),
        Input('phone', 'Telefone', config='required'),
        Input('email', 'Email', config='required'),
        Input('address', 'Endereço', config='required'),
        Input('city', 'Cidade', config='required'),
        Input('cep', 'CEP'),
        TextArea('description', 'Descrição'),
    ]

    name: str
    address: str
    city: str
    cep: str
    phone: str
    email: str = None
    description: str = None
    search: str = None
    key: str = None

    def __str__(self):
        return self.name

    def __post_init__(self):
        self.search = normalize(f'{self.name}; {self.city}; {self.cep}; {self.phone}; {self.email}')

    async def exist(self):
        data = await self.items(query=dict(search=self.search))
        if data:
            return data[0]
        return None

    @property
    def facility_key(self):
        return self.key


@dataclass
class Employee(BaseProfile):
    SINGULAR = 'Funcionário'
    PLURAL = 'Funcionários'
    CONTEXT_TABLES = ['Person', 'Facility']

    DETAIL_PROPERTIES = [
        Property('Escopo', 'scope_format'),
        Property('Assistente Clínico', 'assistant'),
        *BaseProfile.DETAIL_PROPERTIES
    ]

    class Scope(BaseEnum):
        SOC = 'Sócio Proprietário'
        TER = 'Terceirizado'
        EST = 'Estagiário'
        AVU = 'Avulso'
        DIA = 'Diária'
        CLT = 'CLT'

    FORM_FIELDS = [
        *BaseProfile.FORM_FIELDS,
        Form.Select(name='facility_key', label='Empresa', default='pfz7cc10laiu', config='required', options=Facility.select_options),
        Form.Select(name='scope', label='Escopo', config='required', options=Scope.select_options),
        Checkbox('active', 'ativo', default=True),
        Form.Input('base_value', 'Valor Base', type='number', config='min="0" step=".001" required'),
        Form.Checkbox('salary_indexed', 'Indexado ao Salário?'),
        Form.Input('days_month', 'Dias por Mês (referente ao valor base)', type='number', config='min="0" required'),
        Form.Input('hours_day', 'Horas de Atividade por Dia', type='number', config='min="0" required'),
        Form.Checkbox(name='reception', label='Recepção'),
        Form.Checkbox(name='financial', label='Financeiro'),
        Form.Checkbox(name='housekeeping', label='Limpeza'),
        Form.Checkbox(name='management', label='Gerência'),
        Form.Checkbox(name='external', label='Serviços Externos'),
        Form.Checkbox(name='assistant', label='Assistente Clínico'),

    ]
    facility_key: Key('Facility') = field(default='pfz7cc10laiu')
    scope: Scope = None
    active: bool = True
    base_value: float = None
    salary_indexed: bool = True
    days_month: int = None
    hours_day: int = None
    assistant: bool = None
    reception: bool = None
    telephonist: bool = None
    financial: bool = None
    housekeeping: bool = None
    management: bool = None
    external: bool = None

    def __str__(self):
        return f'{self.person} / {self.facility}'

    @property
    def scope_format(self):
        return self.scope.value


@dataclass
class Assistant(Employee):
    SINGULAR = 'Assistente'
    PLURAL = 'Assistentes'
    CONTEXT_TABLES = ['Person', 'Facility']


@dataclass
class Doctor(BaseProfile):
    SINGULAR = 'Médico'
    PLURAL = 'Médicos'
    DETAIL_PROPERTIES = [
        Property('Foto', 'picture_image'),
        Property('CRM', 'register'),
        Property('Universidade', 'university'),
        Property('Formação', 'graduation_field'),
        Property('Ano', 'graduation_year'),
        Property('Especialidades', 'specialties'),
        Property('Empresa', 'facility'),
        Property('Planos de Saúde', 'health_insuances'),
    ]
    CONTEXT_TABLES = ['Person', 'Facility']
    FORM_FIELDS = [
        *Patient.FORM_FIELDS,
        Form.Input(name='register', label='CRM', config='required'),
        Form.Input(name='university', label='Universidade', config='required'),
        Form.Input(name='graduation_field', label='Área de Graduação', config='required', default='Medicina'),
        Form.Input(name='graduation_year', label='Ano de Graduação', config=' max="2025" min="1950"', type='number'),
        Form.TextArea(name='specialties', label='Especialidades', height=100),
        Form.TextArea(name='health_insuances', label='Planos de Saúde', height=100),
        Form.Select(name='facility_key', label='Empresa', config='required disabled', options='<option value="pfz7cc10laiu" selected>Essência</option>'),
        Form.Input(name='picture', label='Foto (link)'),
    ]

    register: str = None
    university: str = None
    graduation_field: str = field(default='Medicina')
    graduation_year: int = None
    specialties: str = None
    health_insuances: str = None
    picture: str = None
    facility_key: Key("Facility") = field(default='pfz7cc10laiu')

    def __str__(self):
        text = ''
        if self.person.gender == Gender.F:
            text += 'Dra. '
        else:
            text += 'Dr. '
        text += f'{self.person.fname.split()[0]} {self.person.lname.split()[-1]}'
        return text

    @property
    def picture_image(self):
        if self.picture:
            return f'\n<img src="{self.picture}" width="250px">'
        return ''

    @property
    def provider_key(self):
        return getattr(self, 'key')


@dataclass
class Therapist(Doctor):
    SINGULAR = 'Terapeuta'
    PLURAL = 'Terapeutas'
    CONTEXT_TABLES = ['Person', 'Facility']

    FORM_FIELDS = [
        *Patient.FORM_FIELDS,
        Form.Input(name='register', label='Registro (CRP, etc) '),
        Form.Input(name='university', label='Universidade'),
        Form.Input(name='graduation_field', label='Área de Graduação',  default='Psicologia'),
        Form.Input(name='graduation_year', label='Ano de Graduação', config=' max="2025" min="1950"', type='number'),
        Form.TextArea(name='specialties', label='Especialidades', height=100),
        Form.TextArea(name='health_insuances', label='Planos de Saúde', height=100),
        Form.Select(name='facility_key', label='Empresa', config='required disabled', options='<option value="pfz7cc10laiu" selected>Essência Psiquiatria</option>'),
        Form.Input(name='picture', label='Foto (link)'),
    ]

    graduation_field: str = field(default='Psicologia')


@dataclass
class Service(BaseModel):
    SINGULAR = 'Serviço'
    PLURAL = 'Serviços'
    DETA_QUERY = dict(active=True)
    EXIST_PARAMS = 'doctor_key therapist_key name price type'
    CONTEXT_TABLES = ['Doctor', 'Therapist', 'Facility', 'Person']
    DETAIL_PROPERTIES = [
        Property('Tipo de Serviço', '_service_type'),
        Property('Escopo', 'service_scope'),
        Property('Preço', 'price_format'),
        Property('Porcentagem da Clínica', 'percentage_format'),
    ]

    FORM_FIELDS = [
        Form.Select(name='facility_key', label='Empresa', config='required',
                    options='<option value="pfz7cc10laiu" selected>Essência Psiquiatria</option>'),
        Form.Select(name='type', label='Tipo de Serviço', config='required', options=ServiceType.select_options),
        Form.Select(name='doctor_key', label='Médico', options=Doctor.select_options),
        Form.Select(name='therapist_key', label='Terapeuta', options=Therapist.select_options),
        Form.Input(name='name', label='Nome do Serviço'),
        Form.Input(name='price', label='Preço', type='number', config='required min="0"'),
        Form.Input(name='percentage', label='Porcentagem', type='number', config='required min="0" max="100"', default='100'),
        Form.Checkbox(name='active', label='Serviço Ativo', config='checked'),
        Form.TextArea(name='description', label='Descrição', height=100),
    ]

    type: ServiceType
    price: float
    name: str = None
    doctor_key: Key('Doctor') = None
    therapist_key: Key('Therapist') = None
    description: str = None
    facility_key: Key('Facility') = field(default='pfz7cc10laiu')
    active: bool = True
    percentage: int = 100
    created: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))))
    search: str = None
    key: str = None

    def __post_init__(self):
        if self.type in ServiceType.medical_service():
            assert self.doctor_key
        if self.type in ServiceType.therapy_session():
            assert self.therapist_key
        super().__post_init__()


    @property
    def _service_type(self):
        return self.type.value

    @property
    def type_for_query(self):
        return self.type.name

    @property
    def price_format(self):
        return f'R$ {self.price}'

    @property
    def name_format(self):
        if self.name:
            return f'{self._name} {self.name}'
        return self._name

    @property
    def _name(self):
        if self.provider_service_type:
            return self.provider_service_type
        elif self.type in ServiceType.payment():
            return f'{self.type.value} para {getattr(self, "provider")}'
        else:
            return f'{self.type.value}'

    @property
    def service_scope(self):
        return self.provider_service_type or self.payment_scope or 'Serviço da Clínica'

    @property
    def percentage_format(self):
        return f'{self.percentage}%'

    @property
    def payment_scope(self):
        if self.type in ServiceType.payment():
            return f'{self.type.value} para {self.provider}'
        return None

    @property
    def provider_service_type(self):
        if self.type in [*ServiceType.medical_service(), *ServiceType.therapy_session()]:
            return f'{getattr(self, "provider")}, {self.type.value}'
        else:
            return None

    @property
    def provider(self):
        return getattr(self, 'doctor') or getattr(self, 'therapist')

    @property
    def _provider(self):
        if self.provider:
            return f'{self.provider}, '
        return ''

    def __str__(self):
        return f'{self.name_format}, R$ {self.price}'


@dataclass
class Concierge(BaseModel):
    SINGULAR = 'Concierge'
    PLURAL = 'Concierges'
    EXIST_PARAMS = 'patient_key provider_key payment_method description payment_date facility_key'
    CONTEXT_TABLES = ['Patient', 'Facility', 'Person', 'Doctor', 'Therapist']
    FORM_FIELDS = [
        Select(name='patient_key', label='Paciente', config='required', options=Patient.select_options),
        Select(name='provider_key', label='Profissional', config='required', options=SelectOption.providers),
        Select(name='facility_key', label='Empresa', config='required', options=Facility.select_options),
        TextArea(name='description', label='Descrição', config='required'),
        Input(name='concierge_value', label='Valor Total', config='required  min="0" step="0.01"', type='number'),
        Select(name='payment_method', label='Método de Pagamento', config='required', options=PaymentMethod.select_options),
        Input(name='payment_value', label='Valor Pago', config='required  min="0" step="0.01"', type='number'),
        Input(name='payment_date', label='Data do Pagamento', config='required', type='date', default=lambda : datetime.date.today()),
    ]
    DETAIL_PROPERTIES = [
        Property('Chave', 'link'),
        Property('Paciente', 'patient'),
        Property('Profissional', 'provider'),
        Property('Empresa', 'facility'),
        Property('Custo', 'price'),
        Property('Descrição', 'description'),
        Property('Pagamento', 'payment'),
    ]

    patient_key: Key('Patient')

    concierge_value: float
    payment_method: PaymentMethod
    payment_value: float
    description: str = None

    provider_key: InitVar[str] = None
    payment_date: datetime.date = field(default_factory=datetime.date.today)
    facility_key: str = field(default='pfz7cc10laiu')
    created: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))))
    creator: str = None
    search: str = None
    key: str = None

    def __str__(self):
        return f'{self.patient}, {self.description}, {self.payment}'

    @property
    def link(self):
        return Anchor(content=self.key, url=self.detail_path(), bootstrap='text-primary')

    @property
    def price(self):
        return Money(self.concierge_value)

    @property
    def payment(self):
        return Payment(date=self.payment_date, method=self.payment_method, value=self.payment_value)

    @property
    def date(self):
        return LocalDate(self.payment_date)

    # @property
    # def patient(self):
    #     return Patient(**ctx.get(patient_var)[self.patient_key])

    # @property
    # def facility(self):
    #     return Facility(**ctx.get(facility_var)[self.facility_key])

    @property
    def provider(self):
        if self.doctor_key:
            return getattr(self, 'doctor')
        elif self.therapist_key:
            return getattr(self, 'therapist')
        # try:
        #     return Doctor(**ctx.get(doctor_var)[self.provider_key])
        # except:
        #     return Therapist(**ctx.get(therapist_var)[self.provider_key])


@dataclass
class Invoice(BaseModel):
    SINGULAR = 'Fatura'
    PLURAL = 'Faturas'
    EXIST_PARAMS = 'patient_key provider_key payment_date facility_key payment_method payment_value'
    CONTEXT_TABLES = ['Facility', 'Doctor', 'Therapist', 'Service', 'Patient', 'Person']
    DETAIL_PROPERTIES = [
        Property('Pagamento', 'payment'),
        Property('Serviço', 'service'),
        Property('Paciente', 'patient_name'),
        Property('Criado Por', 'creator')
    ]
    FORM_FIELDS = [
        Select(name='service_key', label='Serviço', config='required', update=True,
               options=Service.select_options),
        Select(name='patient_key', label='Paciente', options=Patient.select_options),
        Select(name='payment_method', label='Médodo de Pagamento', config='required', update=True, options=PaymentMethod.select_options),
        Input(name='payment_value', label='Valor de Pagamento', config='required min="0" step="0.01"', update=True, type='number'),
        Input(name='payment_date', label='Data do Pagamento', config='required', update=True,
              type='date', default=lambda: datetime.date.today()),
        Input(name='service_date', label='Data da Despesa', config='required', update=True,
              type='date', default=lambda: datetime.date.today()),
        TextArea(name='description', label='Descrição', update=True),
    ]

    service_key: Key('Service')
    payment_method: PaymentMethod
    payment_value: float
    patient_key: Key('Patient') = None
    payment_date: datetime.date = field(default_factory=datetime.date.today)
    service_date: datetime.date = field(default_factory=datetime.date.today)
    provider_key: InitVar[str] = None
    facility_key: InitVar[str] = field(default='pfz7cc10laiu')
    created: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))))
    creator: Key('UserProfileRelation') = None
    description: str = None
    key: str = None
    search: str = None

    def __lt__(self, other):
        return self.payment_date < other.payment_date

    def __post_init__(self, provider_key=None, facility_key=None):
        self.setup_instance()
        if self.service.type not in ServiceType.facility_service():
            if not self.patient_key:
                raise 'Para este serviço é necessáiro cadastrar um paciente.'
        if not self.service_date:
            self.service_date = self.payment_date
        if not self.creator:
            self.creator = 'm1oh63zwz7nq'

    @property
    def payment_date_format(self):
        return LocalDate(self.payment_date, short=True)

    @property
    def payment(self):
        return Payment(self.payment_date, self.payment_value, self.payment_method)

    @property
    def service_type(self):
        return self.service.type.value

    @property
    def service_date_format(self):
        return LocalDate(self.service_date)

    @property
    def value(self):
        return Money(self.payment_value)

    @property
    def provider(self):
        return self.service.provider

    @property
    def provider_fname(self):
        return self.provider.person.fname

    @property
    def provider_link(self):
        return Markup(Anchor(content=self.provider_fname, url=f'/provider/detail/{self.provider.key}', bootstrap='text-primary'))

    @property
    def profile_key(self):
        if self.provider:
            return self.provider.key
        return None

    @property
    def patient_link(self):
        return Markup(Anchor(content=str(self.patient), url=f'/patient/detail/{self.patient_key}', bootstrap='text-primary'))

    @property
    def link(self):
        return Markup(Anchor(content=self.key, url=f'/{self.item_name()}/detail/{self.key}', bootstrap='text-primary'))

    @property
    def patient_name(self):
        if self.patient:
            return str(self.patient)
        return ''

    @property
    def payment_type(self):
        return self.payment_method.value

    @property
    def _provider(self):
        if self.provider:
            return str(self.provider)
        return ''

    @property
    def facility(self):
        return self.service.facility

    def __str__(self):
        patient = f', {self.patient_name}' if self.patient else ''
        return f'{self.payment}, {self.service}{patient}'


@dataclass
class Expense(BaseModel):
    PLURAL = 'Despesas'
    SINGULAR = 'Despesa'
    EXIST_PARAMS = 'cost_type payment_method facility_key expense_date payment_date description'
    DETAIL_PROPERTIES = [
        Property('Mês', 'month'),
        Property('Data de Pagamento', 'payment_date_format'),
        Property('Empresa', 'facility'),
        Property('Tipo de Despesa', 'type_value'),
        Property('Valor', 'payment_value_format'),
        Property('Método', 'payment_method_format'),
        Property('Descrição', 'description'),

    ]
    FORM_FIELDS = [
        Select(name='cost_type', label='Tipo de Custo', config='required', update=True,
               options=CostType.select_options),
        Select(name='employee_key', label='Funcionário/Contratado', update=True,
               options=Employee.select_options),
        Input(name='expense_date', label='Vencimento', config='required', update=True,
              type='date', default=lambda: datetime.date.today()),
        Select(name='facility_key', label='Empresa', update=True, options=Facility.select_options),
        Select(name='payment_method', label='Médodo de Pagamento', config='required', update=True, options=PaymentMethod.select_options),
        Input(name='payment_value', label='Valor de Pagamento', config='required min="0" step="0.01"', update=True, type='number'),
        Input(name='payment_date', label='Data do Pagamento', config='required', update=True,
              type='date', default=lambda: datetime.date.today()),
        TextArea(name='description', label='Descrição', update=True),
    ]
    CONTEXT_TABLES = ['Facility', 'Cost', 'Employee', 'Person']

    cost_type: CostType = None
    employee_key: Key('Employee') = None
    payment_method: PaymentMethod = None
    payment_value: float = None
    facility_key: Key('Facility') = field(default='pfz7cc10laiu')
    expense_date: datetime.date = field(default_factory=datetime.date.today)
    payment_date: datetime.date = field(default_factory=datetime.date.today)
    created: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))))
    creator: Key('UserProfileRelation') = None
    description: str = None
    key: str = None
    search: str = None

    def __post_init__(self, cost_key=None, type=None):
        super().setup_instance()
        if self.cost_type in CostType.employee():
            assert self.employee_key, 'é necessário cadastro de funcionário'
        if self.employee_key:
            self.facility_key = self.employee.facility_key

    @property
    def name(self):
        text = f'{self.facility}, {self.payment}, '
        if self.cost_type:
            text += str(self.cost_type.value)
        if self.employee_key:
            text += f' para {self.employee.full_name}'
        if self.description:
            text += f' ({self.description})'
        return text.replace('  ', " ")

    def __str__(self):
        return f'{self.name}'

    def __lt__(self, other):
        return self.payment_date < other.payment_date

    @property
    def type_name(self):
        return self.cost_type.name

    @property
    def payment_method_format(self):
        return self.payment_method.value

    @property
    def payment_method_name(self):
        return self.payment_method.name

    @property
    def type_value(self):
        return self.cost_type.value

    @property
    def month(self):
        return f'<a href="{self.list_path({"payment_date?contains": f"{self.payment_date.year}-{add_zero_if_len_one(str(self.payment_date.month))}"})}">{Month(self.payment_date.month)}</a>'

    @property
    def payment_date_format(self):
        return LocalDate(self.payment_date)

    @property
    def payment_value_format(self):
        return Money(self.payment_value)

    @property
    def payment(self):
        return Payment(self.payment_date, self.payment_value, self.payment_method)


@dataclass
class User(BaseModel):
    SINGULAR = 'Usuário'
    PLURAL = 'Usuários'

    EXIST_PARAMS = 'model profile_key'

    SEARCH_PARAM = 'username'

    CONTEXT_TABLES = ['Person', 'Doctor', 'Therapist', 'Employee', 'Patient']

    DETAIL_PROPERTIES = [
        Property('Username', 'username'),
        Property('Perfil', 'profile'),
        Property('Tipo de Perfil', 'profile_model')
    ]
    FORM_SCRIPT = f"""
    const password = document.getElementById("password");
    const passwordRepeat = document.getElementById("password_repeat");
    password.value = "";
    passwordRepeat.value = ""
    """

    FORM_FIELDS = [
        Form.Select('profile_key', 'Perfil', config='required', options=Profile.select_options, update=False),
        Form.Input('username', 'Username (email)', config='required', update=False),
        Form.Input('password', 'Senha', config='required', type='password', default=''),
        Form.Input('password_repeat', 'Repetir Senha', config='required', type='password', default='')
    ]

    username: str
    password: str
    profile_key: str
    password_repeat: InitVar[str] = None
    is_admin: bool = field(default=False)
    created: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))))
    key: str = None

    def __post_init__(self, password_repeat: str = None):
        self.username = self.username.strip()
        if password_repeat:
            assert self.password == password_repeat
            self.password = bytes_to_string(get_hash(self.password))
        super().setup_instance()

    def json(self):
        item = self.export()
        del item['password']
        return item

    def __str__(self):
        return self.username

    @property
    def profile(self):
        model, profile_key = self.profile_key.split('.')
        return MODEL_MAP[model](**templates.env.globals[model][profile_key])

    @property
    def profile_model_format(self):
        return Profile.Table(self.profile_key.split(".")[0])

    @property
    def profile_model(self):
        return self.profile_key.split(".")[0]

    @property
    def profile_key_value(self):
        return self.profile_key.split(".")[1]


@dataclass
class UserProfileRelation(BaseModel):
    SINGULAR = 'Perfil de Usuário'
    PLURAL = 'Perfis de Usuários'
    ITEM_NAME = 'user_profile_relation'
    KEY_NAME = 'creator'
    CONTEXT_TABLES = ['Patient', 'Doctor', 'Therapist', 'Assistant', 'Employee', 'Person']
    EXIST_PARAMS = 'profile_key user_key'

    FORM_FIELDS = [
        Select(name='user_key', label='Usuário', config='required', options=User.select_options),
        Select(name='profile_key', label='Perfil', config='required', options=SelectOption.profiles)
    ]
    profile_key: str
    user_key: str
    created: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))))
    model: str = None
    key: str = None

    def __post_init__(self):
        if '.' in self.profile_key:
            model, profile_key = self.profile_key.split('.')
            self.model = model
            self.profile_key = profile_key
        self.setup_instance()


@dataclass
class Deposit(BaseModel):
    value: float
    account: BankAccount
    method: DepositMethod
    date: datetime.date = field(default_factory=datetime.date.today)
    worker_key: str = None
    search: str = None
    key: str = None

    CONTEXT_TABLES = ['Employee', 'Person', 'Facility']

    SINGULAR = 'Depósito Bancário'
    PLURAL = 'Depósitos Bancários'

    EXIST_PARAMS = 'value account method date'

    DETAIL_PROPERTIES = [
        Property('Data', 'date_format'),
        Property('Valor', 'value_format'),
        Property('Conta', 'account_format'),
        Property('Depositante', 'worker'),
    ]

    FORM_FIELDS = [
        Input(name='value', label='Valor', type='number', config='required step="0.01" min="0"'),
        Select(name='account', label='Conta', config='required', options=BankAccount.select_options),
        Select(name='method', label='Método', config='required', options=DepositMethod.select_options),
        Input(name='date', label='Data', type='date', config='required', default=datetime.date.today),
        Select(name='worker_key', label='Funcionário', config='required', options=SelectOption.workers),
    ]

    def __lt__(self, other):
        return self.date < other.date

    def __str__(self):
        return f'{self.value_format} {self.account.value}, {self.date_format}, {self.worker}'

    @property
    def value_format(self):
        return Money(self.value)

    @property
    def account_format(self):
        return self.account.value

    @property
    def date_format(self):
        return LocalDate(self.date)

    @property
    def worker(self):
        try:
            return Assistant(**ctx.get(assistant_var)[self.worker_key])
        except:
            return Employee(**ctx.get(employee_var)[self.worker_key])


@dataclass
class MedicalVisit(BaseModel):
    patient_key: str
    creator: str = field(default='zjhm79ltaw87')
    type: VisitType = field(default='Seguimento')
    main_complaint: str = None
    intro: str = None
    date: datetime.date = None
    start: datetime.datetime = None
    subjective: list[str] = None
    objective: list[str] = None
    treatment: list[str] = None
    response: list[str] = None
    complement: list[str] = None
    context: list[str] = None
    cids: list[str] = None
    assessment: list[str] = None
    plan: list[str] = None
    end: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-2))))
    next: int = None
    key: str = None

    SINGULAR = 'Visita Médica'
    PLURAL = 'Visitas Médicas'

    CONTEXT_TABLES = ['Person', 'Patient', 'Doctor', 'Facility']
    EXIST_PARAMS = 'patient_key creator type date'

    FORM_FIELDS = [
        Select(name='patient_key', label='Paciente', config='required', options=Patient.select_options),
        Input(name='date', label='Data da Visita', type='date', default=datetime.date.today),
        Input(name='start', label='Início da Visita', type='datetime-local', default=lambda: datetime.datetime.now(datetime.timezone(offset=datetime.timedelta(hours=-3)))),
        Hidden(name='creator', config='required', default='zjhm79ltaw87'),
        Select(name='type', label='Tipo de Visita', options=VisitType.select_options),
        Input(name='main_complaint', label='Queixa Principal'),
        TextArea(name='intro', label='Introdução'),
        TextArea(name='subjective', label='Sintomas Atuais'),
        TextArea(name='context', label='Contexto de Vida Relacionado'),
        TextArea(name='treatment', label='Medicações Atuais'),
        TextArea(name='response', label='Resposta Terapêutica'),
        TextArea(name='objective', label='Exame Médico'),
        TextArea(name='complement', label='Dados Complementares'),
        TextArea(name='assessment', label='Análise'),
        TextArea(name='cids', label='CID'),
        TextArea(name='plan', label='Plano Terapêutico'),
        Input(name='next', label='Dias Para Próxima Visita', type='number', config='min="0"'),
        Input(name='end', label='Fim da Visita', type='datetime-local'),
    ]

    def __gt__(self, other):
        return self.date > other.date

    def __le__(self, other):
        return self.date < other.date

    def __post_init__(self):
        super(MedicalVisit, self).__post_init__()

        for item in ['subjective', 'objective', 'context', 'treatment', 'response', 'complement', 'assessment', 'cids', 'plan']:
            value = getattr(self, item)
            if isinstance(value, str):
                setattr(self, item, clean_list_of_strings(split_lines(value)))

        if self.main_complaint:
            self.main_complaint = self.main_complaint.strip()

        if isinstance(self.start, str):
            self.start = datetime.datetime.fromisoformat(self.start)
            if self.start.tzinfo is None or self.start.tzinfo.utcoffset(self.start) is None:
                self.start = convert_or_coerce_timestamp_to_utc(self.start)

        if self.end:
            if isinstance(self.end, str):
                self.end = datetime.datetime.fromisoformat(self.end)
                if self.end.tzinfo is None or self.end.tzinfo.utcoffset(self.end) is None:
                    self.end = convert_or_coerce_timestamp_to_utc(self.end)
        else:
            self.end = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-2)))

        if self.end - self.start > datetime.timedelta(hours=2):
            self.end = self.start + datetime.timedelta(hours=1)

        if self.date:
            if isinstance(self.date, str):
                self.date = datetime.date.fromisoformat(self.date)
        else:
            self.date = datetime.date(year=self.start.year, month=self.start.month, day=self.start.day)

        if self.next:
            self.next = int(self.next)

    @property
    def duration(self):
        return ((self.end - self.start).seconds/60).__int__()


@dataclass
class Event(BaseModel):
    patient_key: str
    name: str
    age: float = None
    key: str = None
    creator: str = field(default='zjhm79ltaw87')
    bdate: InitVar[str] = None

    def __post_init__(self, bdate: str = None):
        if self.age not in ['', None]:
            if isinstance(self.age, str):
                when = self.age.strip()
                if len(when) == 4 and ',' not in when and '.' not in when:
                    birthdate = datetime.date.fromisoformat(bdate)
                    year = int(when)
                    self.age = year_age(birthdate,
                                             datetime.date(year, birthdate.month, 1)).__round__(0)
                elif len(when) in [6, 7] and '/' in when:
                    birthdate = datetime.date.fromisoformat(bdate)
                    month, year = [int(x) for x in when.split('/')]
                    self.age = year_age(birthdate,
                                             datetime.date(year, month, 1)).__round__(1)
                elif len(when) in [8, 9, 10] and '/' in when:
                    birthdate = datetime.date.fromisoformat(bdate)
                    day, month, year = [int(x) for x in when.split('/')]
                    self.age = year_age(birthdate,
                                             datetime.date(year, month, day)).__round__(1)
                else:
                    self.age = float(when.replace(',', '.'))

    def __lt__(self, other):
        return True if self.age < other.age else False

    def __str__(self):
        return f'{self.age} anos: {self.name}'

