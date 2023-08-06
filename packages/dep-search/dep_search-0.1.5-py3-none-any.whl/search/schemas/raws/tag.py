"""Raw tag."""

from typing import Union

from ..common_types import TypeRaw


class TypeTag(TypeRaw):
    """Raw type tag."""

    name: str
    slug: str

    category_pk: Union[int, None]
