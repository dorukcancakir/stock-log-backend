from django.conf import settings
from json import dumps
from jwt import decode, DecodeError, ExpiredSignatureError
from functools import wraps
from strawberry.exceptions import StrawberryGraphQLError as Error
from typing import Any, AsyncGenerator, Optional
from core.enums import Role
from core.models import User


def permission_required(role: Optional[Role] = None):
    def wrapper(func):
        @wraps(func)
        async def wrapped(root, info, **kwargs: Any):
            if 'connection_params' in info.context:
                context = info.context['connection_params']
            else:
                context = info.context['request'].headers
            if 'authorization' not in context:
                raise Error(dumps({'code': 'ERR001'}))
            token = context['authorization']
            secret, algorithm = settings.JWT_SECRET, settings.JWT_ALGORITHM
            try:
                decoded_token = decode(token, secret, algorithms=[algorithm])
            except DecodeError:
                raise Error(dumps({'code': 'ERR002'}))
            except ExpiredSignatureError:
                raise Error(dumps({'code': 'ERR003'}))
            try:
                user = await User.objects.aget(email=decoded_token['email'])
            except User.DoesNotExist:
                raise Error(dumps({'code': 'ERR010'}))
            if not user.is_active:
                raise Error(dumps({'code': 'ERR002'}))
            if role is not None and user.role != role:
                raise Error(dumps({'code': 'ERR001'}))
            info.context['user'] = user
            func_instance = func(root, info, **kwargs)
            if isinstance(func_instance, AsyncGenerator):
                return func_instance
            return await func_instance
        return wrapped
    return wrapper
