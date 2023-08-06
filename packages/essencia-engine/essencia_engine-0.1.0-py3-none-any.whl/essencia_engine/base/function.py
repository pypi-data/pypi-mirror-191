__all__ = [
    'pack_only_fields',
    'normalize_white_spaces',
    'parse_digit',
    'find_digits',
    'convert_or_coerce_timestamp_to_utc',
    'clean_list_of_strings',
    'semicolon_to_line',
    'split_lines',
    'year_age',
    'normalize',
    'slugfy',
    'form_data',
    'parse_json',
    'add_zero_if_len_one',
    'range_name',
    'get_data_and_key',
    'get_attribute'
]

import datetime
import re
import pytz
import enum
from unidecode import unidecode
from typing import Union, Any
from dataclasses import fields
from starlette.requests import Request


def get_attribute(instance: Any, key: str):
    keys = key.split('.')
    value = instance

    def get(key_name: str):
        nonlocal value
        return getattr(value, key_name)

    for item in keys:
        value = get(item)

    return value


def get_data_and_key(v: Any) -> tuple:
    print(f'entering get_data_and_key() with value = {v}')
    if v:
        if isinstance(v, dict):
            key = v.pop('key', None)
            if key in ['', None]:
                return v, None
            else:
                return v, key
        return v
    raise 'v has to be a dict'


def add_zero_if_len_one(string: str) -> str:
    if isinstance(string, (int, float)):
        string = str(int(string))
    if len(string) == 1:
        return f'0{string}'
    else:
        return string


def range_name(interger):
    if interger < 0:
        return f'{interger}'.replace('-', 'M')
    elif interger == 0:
        return 'ZE'
    else:
        return f'P{interger}'


def parse_json(cls, value):
    if isinstance(value, (datetime.datetime, datetime.date)):
        result = value.isoformat()
    elif isinstance(value, enum.Enum):
        result = value.name
    elif isinstance(value, cls):
        result = value.export()
    elif isinstance(value, dict):
        new = dict()
        for key, val in value.items():
            new[key] = parse_json(cls, val)
        result = new
    else:
        result = value
    if isinstance(result, list):
        if len(result) == 0:
            return result
        else:
            return [parse_json(cls, item) for item in result]
    if result in [None]:
        return ''
    if result == 'on':
        return True
    return result


def pack_only_fields(dataclass_model, data: dict) -> dict:
    result = dict()
    for field in fields(dataclass_model):
        result[field.name] = data.get(field.name)
    return result


def normalize_white_spaces(string: str) -> str:
    """
    Normalize to only one whitespace between words and strip the string at start and end.
    :param string:
    :return: string with normalized whitespaces
    """
    return " ".join(re.split(r"\s+", string)).strip()


def parse_digit(value: str) -> Union[float, int, None]:
    """
    Parse a string to float or int.
    :param value:
    :return: float or int or None
    """
    try:
        cleaned = value.replace(".", "").replace(",", ".")
        if cleaned.__contains__("."):
            return float(cleaned)
        return int(cleaned)
    except BaseException as e:
        print(e)
        return None


def find_digits(string: str) -> list[float, int]:
    """
    Find digits in a string and parse them to float or int inside a list
    :param string:
    :return: list of float or int
    """
    values = re.findall(r"[\b]?(?P<n>[\d]+[,\.][\d]+|[\d]+)[\b]?", string)
    return [parse_digit(item) for item in values]


def convert_or_coerce_timestamp_to_utc(timeobj):
    if isinstance(timeobj, str):
        timeobj = datetime.datetime.fromisoformat(timeobj)
    try:
        out = timeobj.astimezone(pytz.timezone('America/Sao_Paulo'))  # aware object can be in any timezone
    except (ValueError, TypeError) as exc:  # naive
        out = timeobj.replace(tzinfo=pytz.timezone('America/Sao_Paulo'))
    return out


def clean_list_of_strings(data: list[str]) -> list[str]:
    """
    Accept a list of strings if string is not empty.
    :param data:
    :return: list of cleaned strings
    """
    return [x.strip() for x in data if x not in [None, '']]


def semicolon_to_line(string: str) -> str:
    """
    Accept a string and replace all semicolon by a new line.
    :param string:
    :return: a string without semicolon, replaced by new line
    """
    return string.replace(';', '\n')


def split_lines(string: str) -> list[str]:
    """
    Accept a string and split making new strings on every semicolon or new line.
    :param string:
    :return: list of strings
    """
    return clean_list_of_strings(semicolon_to_line(string).splitlines())


def year_age(start: datetime.date, end: datetime.date = None) -> float:
    """
    Subctract datetime start to end to get age in years.
    :param start:
    :param end:
    :return: float
    """
    return (((end or datetime.date.today()) - start).days / 365).__round__(1)


def normalize(string: str, lower: bool = True):
    if lower:
        return unidecode(string.strip()).lower()
    else:
        return unidecode(string.strip())


def slugfy(string: str):
    norm = normalize(string, lower=True)
    result = '_'.join(norm.split())
    print(result)
    return result


async def form_data(request: Request) -> dict:
    """
    Get form data from request and remove csrftoken if exist.
    :param request:
    :return: dict
    """
    data = {** await request.form()}
    data.pop('csrftoken', None)
    return data
