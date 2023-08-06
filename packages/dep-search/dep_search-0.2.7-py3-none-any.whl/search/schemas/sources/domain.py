"""Source tag."""

from typing import Dict, List, Union

from ..common_types import IdNameSchema, builtins


class SourceDomain(builtins.TypeSource):
    """Source domain."""

    id: int
    name: str

    subdivision_codes: Union[str, None] = None
    locations: Union[List[IdNameSchema], None] = None

    sort_order: Union[int, None] = 1
    sub_domain: Union[str, None]

    display_in_cities_list: Union[bool, None] = False
    is_active: Union[bool, None] = False
    country_code: Union[str, None] = None

    def clean(self) -> Dict:
        """Overrides."""

        locations = list()
        if self.locations:
            for location in self.locations:
                locations.append(location.id)

        sub_divisions = None
        if self.subdivision_codes:
            sub_divisions = str(self.subdivision_codes).split(',')

        return {
            'name': self.name,
            'domain': self.sub_domain,
            'ordering': self.sort_order,
            'is_active': self.is_active,
            'is_visible': self.display_in_cities_list,
            'sub_divisions': sub_divisions,
            'country': self.country_code,
            'locations': locations,
        }
