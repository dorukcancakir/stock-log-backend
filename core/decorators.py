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
            def raise_error(code):
                raise Error(dumps({'code': code}))

            context = (
                info.context.get('connection_params')
                or info.context['request'].headers
            )

            token = context.get('authorization')
            if not token:
                raise_error('ERR001')

            try:
                decoded_token = decode(
                    token,
                    settings.JWT_SECRET,
                    algorithms=[settings.JWT_ALGORITHM]
                )
            except DecodeError:
                raise_error('ERR002')
            except ExpiredSignatureError:
                raise_error('ERR003')

            user_email = decoded_token.get('email')
            if not user_email:
                raise_error('ERR004')

            try:
                user = await User.objects.aget(email=user_email)
            except User.DoesNotExist:
                raise_error('ERR010')

            if not user.is_active:
                raise_error('ERR005')

            if role and user.role != role:
                raise_error('ERR006')

            info.context['user'] = user

            func_instance = func(root, info, **kwargs)
            if isinstance(func_instance, AsyncGenerator):
                return func_instance
            return await func_instance
        return wrapped
    return wrapper
