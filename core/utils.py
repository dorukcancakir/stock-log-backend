import strawberry as sb
from core.models import InventoryTransactionLog, User
from channels.layers import get_channel_layer
from datetime import datetime

channel_layer = get_channel_layer()


def paginate(qs, skip, first, ordering=None):
    qs = qs.order_by(ordering or 'id')
    if skip is not None:
        qs = qs[skip:]
    if first is not None:
        qs = qs[:first]
    return qs


def set_attributes(instance, data, ignored=[]):
    data = sb.asdict(data)
    for attribute, value in data.items():
        if attribute in ignored or value is sb.UNSET:
            continue
        if attribute[-3:] == '_id' and value is None:
            setattr(instance, attribute[:-3], value)
        else:
            setattr(instance, attribute, value)


async def set_m2m(instance, data, m2m_fields, is_update=False):
    data = sb.asdict(data)
    for m2m_field in m2m_fields:
        if m2m_field[-3:] == 'ies':
            m2m_input = m2m_field[:-3] + 'y_ids'
        else:
            m2m_input = m2m_field[:-1] + '_ids'
        if m2m_input not in data:
            continue
        if data[m2m_input] is sb.UNSET:
            continue
        m2m = getattr(instance, m2m_field)
        if is_update:
            await m2m.aset(data.get(m2m_input, []), clear=True)
        else:
            await m2m.aadd(*data.get(m2m_input, []))


def get_fields(data):
    data = sb.asdict(data)
    fields = {}
    for key in data:
        if key == 'id':
            continue
        value = data.get(key)
        if value is sb.UNSET:
            continue
        fields[key] = value
    return fields


async def create_inventory_transaction_log(company_id, user_id, inventory_item_id, transaction_type, quantity, previous_quantity):
    data = {
        'company_id': company_id,
        'user_id': user_id,
        'inventory_item_id': inventory_item_id,
        'transaction_type': transaction_type,
        'quantity': quantity,
        'previous_quantity': previous_quantity
    }
    inventory_transaction_log = InventoryTransactionLog(**data)
    await inventory_transaction_log.asave()
    user_ids = list(User.objects.filter(
        company_id=company_id).values_list('id', flat=True))
    await broadcast_log(inventory_transaction_log.id, [user_ids])


async def broadcast_log(id, receiver_ids):
    message = {
        'id': id,
        'timestamp': int(datetime.now().timestamp())
    }
    payload = {'type': 'subscription', 'message': message}
    for receiver_id in receiver_ids:
        group_id = str(receiver_id)
        await channel_layer.group_send(group_id, payload)
