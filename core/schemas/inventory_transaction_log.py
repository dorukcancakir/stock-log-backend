from typing import AsyncGenerator, List, Optional
import strawberry as sb
from core.decorators import permission_required
from core.models import InventoryTransactionLog
import core.types as types
from strawberry_django.filters import apply
from core.utils import paginate


manager = InventoryTransactionLog.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def inventory_transaction_logs(
        root, info,
        filters: Optional[types.InventoryTransactionLogFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.InventoryTransactionLogType]:
        company_id = info.context['user'].company_id
        inventory_transaction_logs = manager.filter(company_id=company_id)
        if filters:
            inventory_transaction_logs = apply(
                filters, inventory_transaction_logs)
        inventory_transaction_logs = paginate(
            inventory_transaction_logs, skip, first)
        inventory_transaction_logs = [item async for item in inventory_transaction_logs]
        return inventory_transaction_logs

    @sb.field
    @permission_required()
    async def inventory_transaction_log_count(
        root, info,
        filters: Optional[types.InventoryTransactionLogFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        inventory_transaction_logs = manager.filter(company_id=company_id)
        if filters:
            inventory_transaction_logs = apply(
                filters, inventory_transaction_logs)
        count = await inventory_transaction_logs.acount()
        return count


@sb.type
class Subscription:
    @sb.subscription
    @permission_required()
    async def subscribe_logs(
        root, info
    ) -> AsyncGenerator[types.InventoryTransactionLogSubscriptionType, None]:
        user = info.context['user']
        ws = info.context['ws']
        channel_layer = ws.channel_layer
        group_id = str(user.id)
        await channel_layer.group_add(group_id, ws.channel_name)
        ws_consumer = ws.listen_to_channel('subscription', groups=[group_id])
        async with ws_consumer as consumer:
            async for data in consumer:
                inventory_transaction_log = await manager.aget(pk=data['message']['id'])
                yield types.InventoryTransactionLogSubscriptionType(inventory_transaction_log=inventory_transaction_log, timestamp=data['message']['timestamp'])
