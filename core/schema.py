from strawberry import Schema
from strawberry.tools import merge_types
from core.schemas.company import Query as company_query
from core.schemas.inventory_item import Query as inventory_item_query
from core.schemas.inventory import Query as inventory_query
from core.schemas.item_category import Query as item_category_query
from core.schemas.item_category import Mutation as item_category_mutation
from core.schemas.item_tag import Query as item_tag_query
from core.schemas.item_tag import Mutation as item_tag_mutation
from core.schemas.item import Query as item_query
from core.schemas.item import Mutation as item_mutation
from core.schemas.user import Query as user_query
from core.schemas.user import Mutation as user_mutation


queries = (
    company_query,
    inventory_item_query,
    inventory_query,
    item_category_query,
    item_tag_query,
    item_query,
    user_query,
)

mutations = (
    item_category_mutation,
    item_tag_mutation,
    item_mutation,
    user_mutation,
)


Query = merge_types('Query', queries)
Mutation = merge_types('Mutation', mutations)


schema = Schema(query=Query, mutation=Mutation)
