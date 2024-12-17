import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.enums import TransactionType
from core.models import InventoryItem
import core.types as types
from core.utils import create_inventory_transaction_log, paginate, set_attributes
import core.inputs as inputs

manager = InventoryItem.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def inventory_item(root, info, id: Optional[sb.ID] = None) -> types.InventoryItemType:
        inventory_item = await manager.aget(pk=id)
        return inventory_item

    @sb.field
    @permission_required()
    async def inventory_items(
        root, info,
        filters: Optional[types.InventoryItemFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.InventoryItemType]:
        company_id = info.context['user'].company_id
        inventory_items = manager.filter(company_id=company_id)
        if filters:
            inventory_items = apply(filters, inventory_items)
        inventory_items = paginate(inventory_items, skip, first)
        inventory_items = [item async for item in inventory_items]
        return inventory_items

    @sb.field
    @permission_required()
    async def inventory_item_count(
        root, info,
        filters: Optional[types.InventoryItemFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        inventory_items = manager.filter(company_id=company_id)
        if filters:
            inventory_items = apply(filters, inventory_items)
        count = await inventory_items.acount()
        return count


@sb.type
class Mutation:
    @sb.mutation
    @permission_required()
    async def create_inventory_item(
        root, info,
        data: inputs.CreateInventoryItemInput
    ) -> types.InventoryItemType:
        user_id = info.context['user'].id
        company_id = info.context['user'].company_id
        inventory_item = InventoryItem()
        set_attributes(inventory_item, data)
        inventory_item.company_id = company_id
        await inventory_item.asave()
        await create_inventory_transaction_log(company_id, user_id, inventory_item.id, TransactionType.NEW_ITEM, data.quantity, 0)
        return inventory_item

    @sb.mutation
    @permission_required()
    async def update_inventory_item(
        root, info,
        data: inputs.UpdateInventoryItemInput
    ) -> types.InventoryItemType:
        user_id = info.context['user'].id
        inventory_item = await manager.aget(data.id)
        if inventory_item.quantity < data.quantity:
            await create_inventory_transaction_log(inventory_item.company_id, user_id, inventory_item.id, TransactionType.INCREASE, data.quantity, inventory_item.quantity)
        else:
            await create_inventory_transaction_log(inventory_item.company_id, user_id, inventory_item.id, TransactionType.DECREASE, data.quantity, inventory_item.quantity)
        set_attributes(inventory_item, data)
        await inventory_item.asave()
        return inventory_item
