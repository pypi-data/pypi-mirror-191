"""Raw tag."""

from typing import Union

from ..common_types import builtins


class TypeTag(builtins.TypeRaw):
    """Raw type tag."""

    name: str
    slug: str

    old_slug: Union[str, None]
    category_pk: Union[int, None]

    created: int
    updated: int
