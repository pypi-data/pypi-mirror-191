"""Raw place."""

from typing import Union

from ..common_types import (
    builtins,
    TypeSchema,
    TypeOptionalImage,
    TypeOptionalListImages,
    SizedCloudImage,
)


class PlaceMedia(TypeSchema):
    """Place media."""

    cover: Union[SizedCloudImage, None]
    preview: Union[SizedCloudImage, None]

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    schema_url: TypeOptionalImage
    schemas_urls: TypeOptionalListImages
    schemas_webp: TypeOptionalListImages
    schema_webp: TypeOptionalImage


class PlaceInfo(TypeSchema):
    """Place info."""

    name: str
    description: str
    address: str

    count: int
    popularity: int

    url: TypeOptionalImage

    schema_title: Union[str, None]
    how_to_get: Union[str, None]


class PlaceType(TypeSchema):
    """Place type."""

    pk: int
    name: str


class TypePlace(builtins.TypeRaw):
    """Raw type place."""

    slug: str

    location_pk: int

    place_type: PlaceType
    info: PlaceInfo
    media: PlaceMedia
