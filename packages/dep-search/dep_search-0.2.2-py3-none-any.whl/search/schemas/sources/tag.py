"""Source tag."""

from typing import Dict, List, Union

from ..common_types import IdNameSchema, builtins


class SourceEventCategory(IdNameSchema):
    """Tag event category."""

    breadcrumbs: List[Dict]


class SourceTag(builtins.TypeSource):
    """Source tag."""

    id: int
    name: str
    slug: str

    event_category: Union[SourceEventCategory, None]

    def clean(self) -> Dict:
        """Overrides."""

        cleaned = {'name': self.name, 'slug': self.slug}
        if self.event_category and self.event_category.id:
            cleaned.update({'category_pk': self.event_category.id})

        return cleaned
