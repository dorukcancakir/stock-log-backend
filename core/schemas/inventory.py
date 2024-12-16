import strawberry as sb
from typing import Optional
from core.decorators import permission_required
from core.models import Inventory
import core.types as types


manager = Inventory.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def inventory(root, info, id: Optional[sb.ID] = None) -> types.InventoryType:
        company_id = info.context['user'].company_id
        inventory = await manager.aget(company_id=company_id)
        return inventory
