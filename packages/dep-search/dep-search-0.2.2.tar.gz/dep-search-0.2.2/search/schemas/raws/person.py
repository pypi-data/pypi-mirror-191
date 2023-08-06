"""Raw person."""

from typing import List, Union

from ..common_types import (
    builtins,
    TypeSchema,
    TypeOptionalListImages,
    PersonType,
    SizedCloudImage,
)


class PersonMedia(TypeSchema):
    """Person media."""

    main: Union[SizedCloudImage, None]
    cover: Union[SizedCloudImage, None]

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages


class TypePerson(builtins.TypeRaw):
    """Type person."""

    slug: str
    name: str
    description: str
    position: str
    person_type: PersonType

    tags: Union[List[int], None]

    media: PersonMedia
