"""Raw tag."""

from typing import Union

from ..common_types import builtins


class TypeTag(builtins.TypeRaw):
    """Raw type tag."""

    name: str
    slug: str

    category_pk: Union[int, None]
