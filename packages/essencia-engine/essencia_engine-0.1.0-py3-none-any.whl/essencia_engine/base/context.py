__all__ = [
    'service_var',
    'facility_var',
    'profile_var',
    'person_var',
    'user_var',
    'provider_info_var',
    'patient_var',
    'doctor_var',
    'therapist_var',
    'assistant_var',
    'employee_var',
    'ctx',
    'ContextVar',
    'copy_context',
    'ctx_user',
    'ctx_patient',
    'ctx_doctor',
    'ctx_update',
    'ctx_service',
    'ctx_assistant',
    'ctx_therapist',
    'ctx_employee',
    'ctx_facility',
    'ctx_person',
    'CONTEXT_DATA',
    'CONTEXT_VAR_MAP',
    'MODEL_CONTEXT_MAP',
    'ModelContext',
    'MODEL_MAP',
    'PROFILE_DATA',
    'instance_var'
]

from dataclasses import dataclass, field
from collections import ChainMap
from typing import Callable, Any
from contextvars import ContextVar, copy_context
from anyio import create_task_group

from .database import *
from .setup import *


profile_var = ContextVar('profile_var', default=dict())
person_var = ContextVar('person_var', default=dict())
patient_var = ContextVar('patient_var', default=dict())
therapist_var = ContextVar('therapist_var', default=dict())
assistant_var = ContextVar('assistant_var', default=dict())
employee_var = ContextVar('employee_var', default=dict())
doctor_var = ContextVar('doctor_var', default=dict())
service_var = ContextVar('service_var', default=dict())
facility_var = ContextVar('facility_var', default=dict())
provider_info_var = ContextVar('provider_info_var', default=dict())
user_var = ContextVar('user_var', default=dict())
invoice_var = ContextVar('invoice_var', default=dict())
expense_var = ContextVar('expense_var', default=dict())
concierge_var = ContextVar('concierge_var', default=dict())
instance_var = ContextVar('instance_car', default=dict())

CONTEXT_VAR_MAP: ChainMap[str, ContextVar] = ChainMap()
MODEL_CONTEXT_MAP: ChainMap[str, 'ModelContext'] = ChainMap()
CONTEXT_DATA: ChainMap[str, dict[str, Any]] = ChainMap()
PROFILE_DATA: ChainMap[str, dict[str, Any]] = ChainMap()
MODEL_MAP: ChainMap[str, 'BaseModel'] = ChainMap()


ctx = copy_context()

@dataclass
class ModelContext:
    """ModelContext accept table name, context_var and populates data updating context"""
    table: str
    var: ContextVar
    data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        CONTEXT_VAR_MAP[self.table] = self.var
        MODEL_CONTEXT_MAP[self.table] = self

    async def get(self):
        """
        Get data from database and convert list to dict of keys and values.
        After fun the set function in context.
        """
        self.data = {item['key']: item for item in await async_deta(self.table)}
        CONTEXT_DATA[self.table] = self.data
        templates.env.globals[self.table] = self.data
        ctx.run(self.set)

    def set(self):
        # CONTEXT_VAR_MAP[self.table].set(self.data)
        self.var.set(self.data)

    async def update(self):
        await self.get()

    @property
    def database(self):
        return ctx.get(self.var)

    def key(self, key: str):
        return self.database.get(key)

    @classmethod
    def key_from_table(cls, table: str, key: str):
        return CONTEXT_DATA.get(table, {}).get(key, None)

    @classmethod
    def profile_tables(cls):
        return ['Patient', 'Doctor', 'Therapist', 'Assistant', 'Employee']

    @classmethod
    async def update_profiles(cls):
        async with create_task_group() as tks:
            for item in cls.profile_tables():
                tks.start_soon(MODEL_CONTEXT_MAP[item].update)

    @classmethod
    def compile_profiles(cls):
        for item in cls.profile_tables():
            PROFILE_DATA.new_child({data['key']: {**data, 'model': item} for data in CONTEXT_DATA[item].values()})

    @classmethod
    def profile_key(cls, key: str):
        cls.compile_profiles()
        return PROFILE_DATA.get(key)

    @classmethod
    async def update_all(cls):
        async with create_task_group() as tks:
            for table in MODEL_CONTEXT_MAP.keys():
                tks.start_soon(MODEL_CONTEXT_MAP[table].update)


ctx_user = ModelContext('User', user_var)
ctx_person = ModelContext('Person', person_var)
ctx_patient = ModelContext('Patient', patient_var)
ctx_doctor = ModelContext('Doctor', doctor_var)
ctx_assistant = ModelContext('Assistant', assistant_var)
ctx_therapist = ModelContext('Therapist', therapist_var)
ctx_employee = ModelContext('Employee', employee_var)
ctx_facility = ModelContext('Facility', facility_var)
ctx_service = ModelContext('Service', service_var)
ctx_invoice = ModelContext('Invoice', invoice_var)
ctx_expense = ModelContext('Expense', expense_var)
# ctx_cost = ModelContext('Cost', cost_var)

ctx_concierge = ModelContext('Concierge', concierge_var)


def model_key_map():
    return {model.key_name(): model.__name__ for model in MODEL_MAP.values()}


async def ctx_update(table_list: list[str] = None):
    if table_list:
        context_list = [MODEL_CONTEXT_MAP.get(item) for item in table_list]
    else:
        context_list = MODEL_CONTEXT_MAP.values()
    context_list = list(filter(lambda x: x is not None, context_list))
    async with create_task_group() as tks:
        for item in context_list:
            tks.start_soon(item.update)


