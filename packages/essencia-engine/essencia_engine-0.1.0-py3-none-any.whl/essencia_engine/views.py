from starlette.responses import JSONResponse
from markupsafe import Markup

from .base.setup import templates
from essencia_engine.base.data import *
from .models import *


async def json_object_from_key(request: Request):
    path = request.url.path
    table = None
    if '/person' in path:
        table = 'Person'
        return JSONResponse(await object_from_key(table, request.path_params['key']))
    elif '/patient' in path:
        table = 'Patient'
    elif '/doctor' in path:
        table = 'Doctor'
    elif '/therapist' in path:
        table = 'Therapist'
    elif '/assistant' in path:
        table = 'Assistant'
    elif '/employee' in path:
        table = 'Employee'
    return JSONResponse(await profile_from_key(table, request.path_params['key']))


async def json_assistant_detail(request: Request):
    return await profile_from_key('Assistant', request.path_params['key'])


async def json_patient_list(request: Request):
    items = (item for item in await profile_list('Patient', request))
    return JSONResponse(await add_person_to_profile_data(items))


async def json_doctor_list(request: Request):
    items = (item for item in await profile_list('Doctor', request))
    return JSONResponse(await add_person_to_profile_data(items))


async def json_therapist_list(request: Request):
    items = (item for item in await profile_list('Therapist', request))
    return JSONResponse(await add_person_to_profile_data(items))


async def json_assistant_list(request: Request):
    items = (item for item in await profile_list('Assistant', request))
    return JSONResponse(await add_person_to_profile_data(items))


async def json_employee_list(request: Request):
    items = (item for item in await profile_list('Employee', request))
    return JSONResponse(await add_person_to_profile_data(items))


async def json_person_list(request: Request):
    return JSONResponse(await partial_person_list(request))


async def partial_person_list(request: Request):
    return templates.TemplateResponse('model/partial/list.jj', {
        'request': request,
        'model': Person,
        'instances': await Person.items()
    })


async def partial_person_detail(request: Request):
    instance = await Person.item(request.path_params['key'])
    return templates.TemplateResponse('model/partial/detail.jj', {
        'request': request,
        'model': Person,
        'detail': Markup(instance.detail_html()),
        'instance': instance
    })

async def person_list(request: Request):
    return templates.TemplateResponse('model/list.jj', {
        'request': request,
        'model': Person,
        'instances': await Person.items()
    })


async def person_detail(request: Request):
    instance = await Person.item(request.path_params['key'])
    return templates.TemplateResponse('model/detail.jj', {
        'request': request,
        'model': Person,
        'detail': Markup(instance.detail_html()),
        'instance': instance
    })


async def home(request: Request):
    return templates.TemplateResponse('index.jj', {
        'request': request,
    })