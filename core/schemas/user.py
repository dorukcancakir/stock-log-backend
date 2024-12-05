from django.contrib.auth import get_user_model
from json import dumps
import strawberry as sb
from typing import List, Optional
from core.decorators import permission_required
import core.types as types
from core.utils import paginate


User = get_user_model()
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
    async def users(
        root, info,
        id: Optional[sb.ID] = None,
        name: Optional[str] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.UserType]:
        users = manager.all()
        if id is not None:
            users = users.filter(pk=id)
        if name is not None:
            users = search_name(users, name)
        users = paginate(users, skip, first)
        users = [item async for item in users]
        return users

    @sb.field
    @permission_required('ADMIN')
    async def user_count(
        root, info,
        id: Optional[sb.ID] = None,
        name: Optional[str] = None,
    ) -> int:
        users = manager.all()
        if id is not None:
            users = users.filter(pk=id)
        if name is not None:
            users = search_name(users, name)
        count = await users.acount()
        return count
