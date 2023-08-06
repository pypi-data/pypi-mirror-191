import uuid
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware


MIDDLEWARE = [
    Middleware(CORSMiddleware,
               allow_origins=['*'],
               allow_origin_regex='https://.*\.deta\.app',
               allow_methods=['GET', 'POST'],
               allow_credentials=True),
    Middleware(SessionMiddleware, secret_key='secret', session_cookie='session', max_age=60 * 60 * 24, same_site='lax'),
    # Middleware(TrustedHostMiddleware, allowed_hosts=['deta.dev', '*.deta.dev', '127.0.0.1', '*.memed.com.br', '*.deta.app']),
]
