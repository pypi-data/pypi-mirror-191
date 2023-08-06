"""Raw domain."""

from typing import List, Union

from ..common_types import builtins


class TypeDomain(builtins.TypeRaw):
    """Raw type domain."""

    name: str
    domain: str

    ordering: int

    category_pk: Union[int, None]
    locations: Union[List[int], None] = None

    country: Union[str, None] = None
    sub_divisions: Union[List[str], None]

    is_active: Union[bool, None] = False
    is_visible: Union[bool, None] = False
