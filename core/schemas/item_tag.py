import strawberry as sb
from typing import List, Optional
from strawberry_django.filters import apply
from core.decorators import permission_required
from core.models import ItemTag
import core.types as types
from core.utils import paginate, set_attributes
import core.inputs as inputs


manager = ItemTag.objects


@sb.type
class Query:
    @sb.field
    @permission_required()
    async def item_tag(root, info, id: Optional[sb.ID] = None) -> types.ItemTagType:
        item_tag = await manager.aget(pk=id)
        return item_tag

    @sb.field
    @permission_required()
    async def item_tags(
        root, info,
        filters: Optional[types.ItemTagFilter] = None,
        skip: Optional[int] = None,
        first: Optional[int] = None
    ) -> List[types.ItemTagType]:
        company_id = info.context['user'].company_id
        item_tags = manager.filter(company_id=company_id)
        if filters:
            item_tags = apply(filters, item_tags)
        item_tags = paginate(item_tags, skip, first)
        item_tags = [item async for item in item_tags]
        return item_tags

    @sb.field
    @permission_required()
    async def item_tag_count(
        root, info,
        filters: Optional[types.ItemTagFilter] = None,
    ) -> int:
        company_id = info.context['user'].company_id
        item_tags = manager.filter(company_id=company_id)
        if filters:
            item_tags = apply(filters, item_tags)
        count = await item_tags.acount()
        return count


@sb.type
class Mutation:
    @sb.mutation
    async def create_item_tag(
        root, info,
        data: inputs.CreateItemTagInput
    ) -> types.ItemTagType:
        company_id = info.context['user'].company_id
        item_tag = ItemTag()
        set_attributes(item_tag, data)
        item_tag.company_id = company_id
        await item_tag.asave()
        return item_tag

    @sb.mutation
    async def update_item_tag(
        root, info,
        data: inputs.UpdateItemTagInput
    ) -> types.ItemTagType:
        item_tag = await manager.aget(pk=data.id)
        set_attributes(item_tag, data)
        await item_tag.asave()
        return item_tag

    @sb.mutation
    async def delete_item_tag(
        root, info,
        id: sb.ID
    ) -> types.SuccessResponse:
        await manager.filter(pk=id).adelete()
        return types.SuccessResponse(success=True)
