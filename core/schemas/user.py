from json import dumps
import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.models import User
import core.types as types
from core.utils import paginate, set_attributes
from strawberry.exceptions import StrawberryGraphQLError as Error
from django.conf import settings
from datetime import datetime, timedelta, UTC
from jwt import encode
import core.inputs as inputs

manager = User.objects


def search_name(users, name):
    names = name.split()
    last_name = names[-1]
    first_name = ' '.join(names[:-1])
    kwargs = {'first_name__iexact': first_name, 'last_name__iexact': last_name}
    users = users.filter(**kwargs)
    return users


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def user(root, info, id: Optional[sb.ID] = None) -> types.UserType:
        user = info.context['user']
        if id is not None:
            assert user.role == 'ADMIN', dumps({'code': 'ERR001'})
            user = await manager.aget(pk=id)
        return user

    @sb.field
    @permission_required()
    async def users(
        root, info,
        id: Optional[sb.ID] = None,
        name: Optional[str] = None,
        filters: Optional[types.UserFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.UserType]:
        users = manager.all()
        if id is not None:
            users = users.filter(pk=id)
        if name is not None:
            users = search_name(users, name)
        if filters:
            users = apply(filters, users)
        users = paginate(users, skip, first)
        users = [item async for item in users]
        return users

    @sb.field
    @permission_required()
    async def user_count(
        root, info,
        id: Optional[sb.ID] = None,
        name: Optional[str] = None,
        filters: Optional[types.UserFilter] = None,
    ) -> int:
        users = manager.all()
        if id is not None:
            users = users.filter(pk=id)
        if name is not None:
            users = search_name(users, name)
        if filters:
            users = apply(filters, users)
        count = await users.acount()
        return count


def create_token(email):
    secret, algorithm = settings.JWT_SECRET, settings.JWT_ALGORITHM
    exp = datetime.now(UTC) + timedelta(days=14)
    payload = {'email': email, 'exp': exp}
    token = encode(payload, secret, algorithm)
    return token


@sb.type
class Mutation:
    @sb.mutation
    async def get_token(
        root, info,
        data: inputs.GetTokenInput
    ) -> types.GetTokenResponse:
        try:
            user = await manager.aget(email=data.email)
        except User.DoesNotExist:
            raise Error(dumps({'code': 'ERR010'}))
        if not user.is_active:
            raise Error(dumps({'code': 'ERR010'}))
        password_valid = await user.acheck_password(data.password)
        if not password_valid:
            raise Error(dumps({'code': 'ERR010'}))
        token = create_token(data.email)
        return types.GetTokenResponse(user=user, token=token)

    @sb.mutation
    @permission_required()
    async def create_user(
        root, info,
        data: inputs.CreateUserInput
    ) -> types.UserType:
        company_id = info.context['user'].company_id
        user = User()
        set_attributes(user, data)
        user.company_id = company_id
        await user.set_password(data.password)
        await user.asave()
        return user

    @sb.mutation
    @permission_required()
    async def update_user(
        root, info,
        data: inputs.UpdateUserInput
    ) -> types.UserType:
        user = await manager.aget(pk=data.id)
        set_attributes(user, data)
        if data.password:
            await user.set_password(data.password)
        await user.asave()
        return user

    @sb.mutation
    @permission_required()
    async def delete_user(
        root, info,
        id: sb.ID,
        delete_permanent: Optional[bool] = False
    ) -> types.SuccessResponse:
        if delete_permanent:
            await manager.filter(pk=id).adelete()
            return types.SuccessResponse(success=True)
        await manager.filter(pk=id).aupdate(is_active=False)
        return types.SuccessResponse(success=True)
