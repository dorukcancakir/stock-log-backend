import strawberry as sb
from strawberry.file_uploads import Upload
from typing import Optional
import core.enums as enums


def required(description=None):
    return sb.field(description=description)


def optional(description=None):
    return sb.field(description=description, default=sb.UNSET)


@sb.input
class CreateItemCategoryInput:
    company_id: sb.ID = required()
    name: str = required('50 chars max')


@sb.input
class UpdateItemCategoryInput:
    id: sb.ID = required()
    name: Optional[str] = optional('50 chars max')


@sb.input
class CreateItemTagInput:
    company_id: sb.ID = required()
    name: str = required('50 chars max')


@sb.input
class UpdateItemTagInput:
    id: sb.ID = required()
    name: Optional[str] = optional('50 chars max')


@sb.input
class CreateItemInput:
    company_id: sb.ID = required()
    category_id: sb.ID = required()
    tag_id: sb.ID = required()
    name: str = required('50 chars max')
    quantity: Optional[int] = optional('Default 1')
    min_quantity: Optional[int] = optional('Default 0')
    image: Upload = required()
    unit_of_measurement: Optional[enums.Measurement] = optional(
        'Default PIECE')


@sb.input
class UpdateItemInput:
    id: sb.ID = required()
    company_id: Optional[sb.ID] = optional()
    category_id: Optional[sb.ID] = optional()
    tag_id: Optional[sb.ID] = optional()
    name: Optional[str] = optional('50 chars max')
    quantity: Optional[int] = optional('Default 1')
    min_quantity: Optional[int] = optional('Default 0')
    image: Optional[Upload] = optional()
    unit_of_measurement: Optional[enums.Measurement] = optional(
        'Default PIECE')


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
