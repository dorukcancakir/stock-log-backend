from datetime import datetime
from decimal import Decimal
import strawberry as sb
from strawberry.file_uploads import Upload
from typing import List, Optional
import core.enums as enums


def required(description=None):
    return sb.field(description=description)


def optional(description=None):
    return sb.field(description=description, default=sb.UNSET)


@sb.input
class GetTokenInput:
    email: str = required('100 chars max')
    password: str = required('128 chars max')


@sb.input
class CreateUserInput:
    email: str = required('100 chars max')
    password: str = required('128 chars max')
    first_name: str = required('50 chars max')
    last_name: str = required('50 chars max')


@sb.input
class UpdateUserInput:
    id: sb.ID = required()
    password: Optional[str] = optional('128 chars max')
    first_name: Optional[str] = optional('50 chars max')
    last_name: Optional[str] = optional('50 chars max')
    is_active: Optional[bool] = optional('True / False')
