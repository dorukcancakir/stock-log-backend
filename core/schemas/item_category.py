import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.models import ItemCategory
import core.types as types
from core.utils import paginate, set_attributes
import core.inputs as inputs


manager = ItemCategory.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def item_category(root, info, id: Optional[sb.ID] = None) -> types.ItemCategoryType:
        item_category = await manager.aget(pk=id)
        return item_category

    @sb.field
    @permission_required()
    async def item_categories(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.ItemCategoryFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.ItemCategoryType]:
        company_id = info.context['user'].company_id
        item_categories = manager.filter(company_id=company_id)
        if id is not None:
            item_categories = item_categories.filter(pk=id)
        if filters:
            item_categories = apply(filters, item_categories)
        item_categories = paginate(item_categories, skip, first)
        item_categories = [item async for item in item_categories]
        return item_categories

    @sb.field
    @permission_required()
    async def item_category_count(
        root, info,
        id: Optional[sb.ID] = None,
        filters: Optional[types.ItemCategoryFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        item_categories = manager.filter(company_id=company_id)
        if id is not None:
            item_categories = item_categories.filter(pk=id)
        if filters:
            item_categories = apply(filters, item_categories)
        count = await item_categories.acount()
        return count


@sb.type
class Mutation:
    @sb.mutation
    async def create_item_category(
        root, info,
        data: inputs.CreateItemCategoryInput
    ) -> types.ItemCategoryType:
        item_category = ItemCategory()
        set_attributes(item_category, data)
        await item_category.asave()
        return item_category

    @sb.mutation
    async def update_item_category(
        root, info,
        data: inputs.UpdateItemCategoryInput
    ) -> types.ItemCategoryType:
        item_category = await manager.aget(pk=data.id)
        set_attributes(item_category, data)
        await item_category.asave()
        return item_category

    @sb.mutation
    async def delete_item_category(
        root, info,
        id: sb.ID
    ) -> types.SuccessResponse:
        await manager.filter(pk=id).adelete()
        return types.SuccessResponse(success=True)
