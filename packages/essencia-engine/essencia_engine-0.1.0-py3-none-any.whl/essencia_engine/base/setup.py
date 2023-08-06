__all__ = [
    'config',
    'static',
    'templates',
    'MICRO_NAME',
    'MICRO_TYPE',
    'DETA_API_KEY',
    'DETA_PROJECT_KEY',
    'DETA_SPACE_APP_HOSTNAME',
    'CSRF_TOKEN'
]

import os
from os import getcwd, path
from starlette.config import Config
from starlette.datastructures import Secret
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


config = Config(path.join(getcwd(), '.env'))

MICRO_NAME = os.getenv('DETA_SPACE_APP_MICRO_NAME', None)
MICRO_TYPE = os.getenv('DETA_SPACE_APP_MICRO_TYPE', 'normal')
DETA_API_KEY = config.get('ESSENCIA_API_KEY', cast=Secret)
DETA_PROJECT_KEY = config.get('ESSENCIA_PROJECT_KEY', cast=Secret)
DETA_SPACE_APP_HOSTNAME = config.get('ESSENCIA_SPACE_APP_HOSTNAME', cast=str)
CSRF_TOKEN = config.get('CSRF_SECRET', cast=Secret)

static: StaticFiles = StaticFiles(directory=os.path.join(os.getcwd(), 'static'))
templates: Jinja2Templates = Jinja2Templates(directory=os.path.join(os.getcwd(), 'templates'))




