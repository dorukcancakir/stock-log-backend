import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.models import Company
import core.types as types
from core.utils import paginate


manager = Company.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def company(root, info, id: Optional[sb.ID] = None) -> types.CompanyType:
        company = await manager.aget(pk=id)
        return company

    @sb.field
    @permission_required('ADMIN')
    async def companies(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.CompanyFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.CompanyType]:
        companies = manager.all()
        if id is not None:
            companies = companies.filter(pk=id)
        if filters:
            companies = apply(filters, companies)
        companies = paginate(companies, skip, first)
        companies = [item async for item in companies]
        return companies

    @sb.field
    @permission_required('ADMIN')
    async def company_count(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.CompanyFilter] = None,
    ) -> int:
        companies = manager.all()
        if id is not None:
            companies = companies.filter(pk=id)
        if filters:
            companies = apply(filters, companies)
        count = await companies.acount()
        return count
