"""Raw category."""

from typing import List, Union

from ..common_types import (
    TypeSchema,
    BreadCrumbs,
    SizedCloudImage,
    VisibleType,
    builtins,
)


class CategoryMedia(TypeSchema):
    """Category media."""

    cover: SizedCloudImage
    preview: SizedCloudImage


class TypeCategory(builtins.TypeRaw):
    """Raw type category."""

    name: str
    slug: str
    old_slug: Union[str, None]

    is_actual: bool
    visible_type: VisibleType
    breadcrumbs: Union[List[BreadCrumbs], None]

    media: CategoryMedia
