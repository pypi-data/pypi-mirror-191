__all__ = [
    'JsonPrimitive',
    'JsonSequence',
    'JsonDict',
    'Jsonable',
    'DetaQuery',
    'Text',
    'SelectKey',
    'InputKey',
    'Union',
    'Optional',
    'ClassVar',
    'Literal',
    'Any',
    'Url',
    'NamedTuple',
    'dataclass',
    'field',
    'fields',
    'InitVar',
    'datetime',
    'Markup',
    'Callable',
    'Coroutine',
    'asdict',
    'Request',
    'HTMLResponse',
    'RedirectResponse',
    'JSONResponse',
    'Starlette',
    'Mount',
    'Route',
    'namedtuple',
    'TemplateResponse',
    'Response',
    'List'
]

import datetime
from typing import Union, NewType, Optional, ClassVar, Literal, Any, NamedTuple, Callable, Coroutine, List
from collections import namedtuple
from dataclasses import dataclass, field, fields, InitVar, asdict
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse, Response
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.templating import Response as TemplateResponse
from markupsafe import Markup


JsonPrimitive = Union[str, float, int, bool, None]
JsonSequence = list[JsonPrimitive]
JsonDict = dict[str, Union[JsonSequence, JsonPrimitive]]
Jsonable = Union[JsonDict, JsonSequence, JsonPrimitive]
DetaQuery = Union[dict[str, JsonPrimitive], list[dict[str, JsonPrimitive]]]
Text = NewType('Text', str)
SelectKey = NewType('SelectKey', str)
InputKey = NewType('InputKey', str)
Url = NewType('Url', str)
