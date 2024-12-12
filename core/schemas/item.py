import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.models import Item
import core.types as types
from core.utils import paginate, set_attributes
import core.inputs as inputs


manager = Item.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def item(root, info, id: Optional[sb.ID] = None) -> types.ItemType:
        item = await manager.aget(pk=id)
        return item

    @sb.field
    @permission_required()
    async def items(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.ItemFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.ItemType]:
        company_id = info.context['user'].company_id
        items = manager.filter(company_id=company_id)
        if id is not None:
            items = items.filter(pk=id)
        if filters:
            items = apply(filters, items)
        items = paginate(items, skip, first)
        items = [item async for item in items]
        return items

    @sb.field
    @permission_required()
    async def item_count(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.ItemFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        items = manager.filter(company_id=company_id)
        if id is not None:
            items = items.filter(pk=id)
        if filters:
            items = apply(filters, items)
        count = await items.acount()
        return count


@sb.type
class Mutation:
    @sb.mutation
    async def create_item(
        root, info,
        data: inputs.CreateItemInput
    ) -> types.ItemType:
        item = Item()
        set_attributes(item, data)
        await item.asave()
        return item

    @sb.mutation
    async def update_item(
        root, info,
        data: inputs.UpdateItemInput
    ) -> types.ItemType:
        item = await manager.aget(pk=data.id)
        set_attributes(item, data)
        await item.asave()
        return item

    @sb.mutation
    async def delete_item(
        root, info,
        id: sb.ID
    ) -> types.SuccessResponse:
        await manager.filter(pk=id).adelete()
        return types.SuccessResponse(success=True)
