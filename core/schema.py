from strawberry import Schema
from strawberry.tools import merge_types
from core.schemas.user import Query as user_query
# from core.schemas.user import Mutation as user_mutation


queries = (
    user_query,
)

# mutations = (
#     user_mutation,
# )


Query = merge_types('Query', queries)
# Mutation = merge_types('Mutation', mutations)


schema = Schema(query=Query)
# schema = Schema(query=Query, mutation=Mutation)
