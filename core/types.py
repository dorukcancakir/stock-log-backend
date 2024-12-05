from django.contrib.auth import get_user_model
import strawberry as sb
import strawberry_django as sb_django

User = get_user_model()


def description(string):
    return sb.field(description=string)


def resolve(string):
    def resolver(root):
        attribute = getattr(root, string)
        try:
            return getattr(attribute, 'url')
        except (AttributeError, ValueError):
            return attribute

    return sb.field(resolver=resolver)


@sb.type
class SuccessResponse:
    success: bool


@sb_django.type(User)
class UserType:
    id: sb.auto
    email: sb.auto
    first_name: sb.auto
    last_name: sb.auto
