import strawberry as sb


def paginate(qs, skip, first, ordering=None):
    qs = qs.order_by(ordering or 'id')
    if skip is not None:
        qs = qs[skip:]
    if first is not None:
        qs = qs[:first]
    return qs


def set_attributes(instance, data, ignored=None):
    data = sb.asdict(data)
    for attribute, value in data.items():
        if attribute == ignored or value is sb.UNSET:
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
