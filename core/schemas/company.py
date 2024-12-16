import strawberry as sb
from core.decorators import permission_required
from core.models import Company
import core.types as types


manager = Company.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def company(root, info) -> types.CompanyType:
        company_id = info.context['user'].company_id
        company = await manager.aget(pk=company_id)
        return company
