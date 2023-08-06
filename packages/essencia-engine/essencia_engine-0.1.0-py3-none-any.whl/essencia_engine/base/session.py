__all__ = [
    'login_user'
]

from starlette.responses import HTMLResponse
from starlette.requests import Request
from .types import *
from .security import *
from .database import *
from .context import *
from .setup import *


async def login_user(request: Request, username: str, password: str):
    User = MODEL_MAP['User']
    await ctx_update()

    async def get_user() -> Optional[User]:
        try:
            return (await User.from_database(query=dict(username=username)))[0]
        except BaseException as e:
            print(e)
            return None

    def check_user() -> tuple[Optional[User], bool]:
        return check_password(password, user.password)

    # async def user_profile_relation_data(user_key: str) -> dict[str, Jsonable]:
    #     result = await async_deta('UserProfileRelation', query={'user_key': user_key})
    #     if result:
    #         return result[0]

    user = await get_user()
    if user:
        check = check_user()
        if check:
            # relation = MODEL_MAP['UserProfileRelation'](** await user_profile_relation_data(user_key=user.key))
            if user:
                # profile = MODEL_MAP[relation.model](
                #     **await async_deta(relation.model, key=relation.profile_key)
                # )
                profile = user.profile
                data = {
                    'username': user.username,
                    'key': user.key,
                    'is_admin': user.is_admin,
                    'fullname': str(profile.person),
                    'profile_model': user.profile_model,
                    'profile_key': profile.key,
                    'age': profile.age,
                    'bdate': profile.person.bdate.isoformat(),
                    'gender': profile.gender_value,
                    'person_key': profile.person.key,
                    'start': datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))).isoformat()
                }
                request.session['user'] = data
                templates.env.globals['user'] = data
                return RedirectResponse('/logged', 303)
        else:
            return HTMLResponse('Usuário e senha não conferem. Por favor tentar novamente <a href="/login">login</a> novamente.')
    return HTMLResponse('Este usuário não foi encontrado. Por favor <a href="/register">registrar</a> usuário.')









