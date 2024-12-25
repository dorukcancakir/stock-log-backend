import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.enums import TransactionType
from core.models import InventoryItem, Item
import core.types as types
from core.utils import create_inventory_transaction_log, paginate, set_attributes
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
        filters: Optional[types.ItemFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.ItemType]:
        company_id = info.context['user'].company_id
        items = manager.filter(company_id=company_id)
        if filters:
            items = apply(filters, items)
        items = paginate(items, skip, first)
        items = [item async for item in items]
        return items

    @sb.field
    @permission_required()
    async def item_count(
        root, info,
        filters: Optional[types.ItemFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        items = manager.filter(company_id=company_id)
        if filters:
            items = apply(filters, items)
        count = await items.acount()
        return count


@sb.type
class Mutation:
    @sb.mutation
    @permission_required()
    async def create_item(
        root, info,
        data: inputs.CreateItemInput
    ) -> types.ItemType:
        user_id = info.context['user'].id
        company_id = info.context['user'].company_id
        item = Item()
        set_attributes(item, data, ['quantity', 'min_quantity'])
        item.company_id = company_id
        await item.asave()
        inventory_item = InventoryItem()
        inventory_item.company_id = company_id
        inventory_item.item = item
        inventory_item.quantity = data.quantity
        inventory_item.min_quantity = data.min_quantity
        await inventory_item.asave()
        await create_inventory_transaction_log(company_id, user_id, inventory_item.id, TransactionType.NEW_ITEM, data.quantity, 0)
        return item

    @sb.mutation
    @permission_required()
    async def update_item(
        root, info,
        data: inputs.UpdateItemInput
    ) -> types.ItemType:
        item = await manager.aget(pk=data.id)
        set_attributes(item, data)
        await item.asave()
        return item

    @sb.mutation
    @permission_required()
    async def delete_item(
        root, info,
        id: sb.ID
    ) -> types.SuccessResponse:
        await manager.filter(pk=id).adelete()
        return types.SuccessResponse(success=True)
