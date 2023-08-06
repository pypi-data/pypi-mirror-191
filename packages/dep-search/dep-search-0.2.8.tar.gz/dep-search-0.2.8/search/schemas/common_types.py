"""Common types."""

from typing import Dict, List, Union
from enum import IntEnum, unique

from fastapi_utils.enums import StrEnum
from pydantic import AnyUrl, BaseModel, Field as SchemaField  # noqa

from ..internals import builtins  # noqa

TypeOptionalImage = Union[str, None]
TypeOptionalListImages = Union[List[str], None]


@unique
class PersonTypeSource(IntEnum):
    """Person type for source."""

    ARTIST = 10
    SPORTSMAN = 20


@unique
class PersonType(StrEnum):
    """Person types."""

    artist = 'artist'
    sportsman = 'sportsman'


@unique
class Restriction(IntEnum):
    """List of restrictions for visiting the event."""

    SIX = 1
    TWELVE = 2
    EIGHTEEN = 3
    TWENTY_ONE = 4
    NONE = 5
    SEXTEEN = 6


@unique
class SourceDisplayTypes(IntEnum):
    """Widget source display types."""

    SEATS = 10
    CATEGORIES = 20
    SEATS_AND_CATEGORIES = 30


@unique
class DisplayType(StrEnum):
    """Display widget types."""

    default = 'default'
    categories = 'categories'
    announcements = 'announcements'


@unique
class VisibleType(StrEnum):
    """Category visible types."""

    simple = 'simple'
    table = 'table'
    hockey_table = 'hockey_table'
    football_table = 'football_table'


class TypeSchema(BaseModel):
    """Source part schema."""

    pass


class IdNameSchema(TypeSchema):
    """Schema with id and name."""

    id: int
    name: Union[str, None]


class LocationSchema(IdNameSchema):
    """Location schema."""

    country: Union[Dict, None]


class QNA(TypeSchema):
    """QNA schema."""

    id: int
    answer: Union[str, None]
    question: Union[str, None]


class HallLayout(IdNameSchema):
    """Hall layout schema."""

    hall_id: int


class ShortEventPlace(IdNameSchema):
    """Short event place."""

    address: Union[str, None]


class SizedCloudImage(TypeSchema):
    """Sized cloud image."""

    src: TypeOptionalImage
    src_webp: TypeOptionalImage

    sm: TypeOptionalImage
    sm_webp: TypeOptionalImage

    md: TypeOptionalImage
    md_webp: TypeOptionalImage

    lg: TypeOptionalImage
    lg_webp: TypeOptionalImage


class SizedSourceMarketImage(TypeSchema):
    """Sized source market image."""

    src_market: TypeOptionalImage
    src_webp_market: TypeOptionalImage

    sm_market: TypeOptionalImage
    sm_webp_market: TypeOptionalImage

    md_market: TypeOptionalImage
    md_webp_market: TypeOptionalImage

    lg_market: TypeOptionalImage
    lg_webp_market: TypeOptionalImage


class ShortPersonSchema(IdNameSchema):
    """Short person schema."""

    parent_id: Union[int, None]
    children: Union[List[Dict], None]
    position: Union[str, None]

    cover: Union[SizedSourceMarketImage, None]


class BreadCrumbs(TypeSchema):
    """Breadcrumbs."""

    slug: str
    title: str
