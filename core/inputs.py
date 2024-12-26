import strawberry as sb
from strawberry.file_uploads import Upload
from typing import Optional
import core.enums as enums


def required(description=None):
    return sb.field(description=description)


def optional(description=None):
    return sb.field(description=description, default=sb.UNSET)


@sb.input
class CreateInventoryItemInput:
    inventory_id: sb.ID = required()
    item_id: sb.ID = required()
    quantity: Optional[int] = optional('Default 0')
    min_quantity: Optional[int] = optional('Default 0')


@sb.input
class UpdateInventoryItemInput:
    id: sb.ID = required()
    quantity: Optional[int] = optional('Default 0')
    min_quantity: Optional[int] = optional('Default 0')


@sb.input
class CreateItemCategoryInput:
    name: str = required('50 chars max')


@sb.input
class UpdateItemCategoryInput:
    id: sb.ID = required()
    name: Optional[str] = optional('50 chars max')


@sb.input
class CreateItemTagInput:
    name: str = required('50 chars max')


@sb.input
class UpdateItemTagInput:
    id: sb.ID = required()
    name: Optional[str] = optional('50 chars max')


@sb.input
class CreateItemInput:
    category_id: sb.ID = required()
    tag_id: sb.ID = required()
    name: str = required('50 chars max')
    image: Optional[Upload] = optional()
    quantity: int = required('Default 0')
    min_quantity: int = required('Default 0')
    unit_of_measurement: Optional[enums.Measurement] = optional(
        'Default PIECE')


@sb.input
class UpdateItemInput:
    id: sb.ID = required()
    category_id: Optional[sb.ID] = optional()
    tag_id: Optional[sb.ID] = optional()
    name: Optional[str] = optional('50 chars max')
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
