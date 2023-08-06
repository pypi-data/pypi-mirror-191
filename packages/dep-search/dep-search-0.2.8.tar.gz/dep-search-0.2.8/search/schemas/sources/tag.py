"""Source tag."""

from typing import Dict, List, Union
from service.ext import fn

from ..common_types import IdNameSchema, builtins


class SourceEventCategory(IdNameSchema):
    """Tag event category."""

    breadcrumbs: List[Dict]


class SourceTag(builtins.TypeSource):
    """Source tag."""

    id: int
    name: str
    slug: str
    old_slug: Union[str, None]

    event_category: Union[SourceEventCategory, None]

    created: str
    updated: str

    def clean(self) -> Dict:
        """Overrides."""

        cleaned = {
            'name': self.name,
            'slug': self.slug,
            'old_slug': self.old_slug,
            'created': fn.date_str_to_timestamp(self.created),
            'updated': fn.date_str_to_timestamp(self.updated),
        }

        if self.event_category and self.event_category.id:
            cleaned.update({'category_pk': self.event_category.id})

        return cleaned
