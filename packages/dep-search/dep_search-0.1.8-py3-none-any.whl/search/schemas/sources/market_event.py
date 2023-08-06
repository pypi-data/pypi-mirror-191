"""Source market event."""

from typing import Dict, List, Union

from service.ext import fn

from ..common_types import (
    IdNameSchema,
    HallLayout,
    QNA,
    Restriction,
    ShortEventPlace,
    ShortPersonSchema,
    SizedSourceMarketImage,
    TypeSchema,
    builtins,
)


class SourceEventMarketCategory(IdNameSchema):
    """Event market category."""

    breadcrumbs: List[Dict]


class Children(TypeSchema):
    """Children event."""

    id: int
    parent_id: int

    date_start: str
    time_start: str
    date_finish: str
    time_finish: str

    top: Union[bool, None] = False
    is_top: Union[bool, None] = False
    is_global: Union[bool, None] = False
    is_premiere: Union[bool, None] = False
    is_rejected: Union[bool, None] = False
    is_star_cast: Union[bool, None] = False
    has_open_date: Union[bool, None] = False
    is_full_house: Union[bool, None] = False
    is_rescheduled: Union[bool, None] = False


class SourceMarketEvent(builtins.TypeSource):
    """Source market event."""

    id: int

    slug: str
    title: str
    is_periodical: bool

    date: Union[str, None]
    description: Union[str, None]

    date_start: Union[str, None]
    time_start: Union[str, None]
    date_finish: Union[str, None]
    time_finish: Union[str, None]

    top: bool
    has_open_date: bool
    is_global: bool
    is_rejected: bool
    is_rescheduled: bool
    is_premiere: bool
    is_full_house: bool
    is_top: bool
    is_fan_id: bool
    is_pushkin: bool

    is_filled: bool
    is_star_cast: bool
    is_show_hint: bool
    is_certificate_event: bool
    fill_by_template: bool

    restriction: Restriction

    hint_text: Union[str, None]

    children: Union[List[Children], None]
    event_category: Union[SourceEventMarketCategory, None]
    hall_layout: Union[HallLayout, None]
    persons: Union[List[ShortPersonSchema], None]
    place: Union[ShortEventPlace, None]

    location: Union[IdNameSchema, None]
    country: Union[IdNameSchema, None]
    tags: Union[List[IdNameSchema], None]

    qna: Union[List[QNA], None]

    cover: Union[SizedSourceMarketImage, None]
    preview: Union[SizedSourceMarketImage, None]

    manager: Union[Dict, None]

    ticket_cover: Union[str, None]
    seo_place: Union[str, None]
    seo_dates: Union[str, None]
    seo_duration: Union[str, None]
    seo_base_names: Union[str, None]
    seo_place_accusative: Union[str, None]
    seo_place_prepositional: Union[str, None]
    seo_categories_with_preposition: Union[str, None]
    seo_short_name_with_preposition: Union[str, None]
    seo_event_name_with_preposition: Union[str, None]

    def _read_start(self) -> Union[int, None]:
        """Read start stamp."""

        if self.date_start and self.time_start:
            return fn.timestamp(fn.dt_join(self.date_start, self.time_start))

    def _read_finish(self) -> Union[int, None]:
        """Read finish stamp."""

        if self.date_start and self.time_start:
            return fn.timestamp(fn.dt_join(self.date_start, self.time_start))

    def _read_persons(self) -> Union[List[int], None]:
        """Read persons."""

        return [_p.id for _p in self.persons] if self.persons else None

    def _read_tags(self) -> Union[List[int], None]:
        """Read tags."""

        return [_t.id for _t in self.tags] if self.tags else None

    def _read_properties(self) -> Dict:
        """Read source properties."""

        return {
            'is_periodical': self.is_periodical,
            'is_global': self.is_global,
            'is_top': any([self.top, self.is_top]),
            'is_premiere': self.is_premiere,
            'is_star_cast': self.is_star_cast,
            'is_rejected': self.is_rejected,
            'is_rescheduled': self.is_rescheduled,
            'is_full_house': self.is_full_house,
            'is_open_date': self.has_open_date,
        }

    def _read_media(self) -> Dict:
        """Read source media cover and preview."""

        return {
            'cover': {
                'src': self.cover.src_market,
                'src_webp': self.cover.src_webp_market,
                'md': self.cover.md_market,
                'md_webp': self.cover.md_webp_market,
                'sm': self.cover.sm_market,
                'sm_webp': self.cover.sm_webp_market,
                'lg': self.cover.lg_market,
                'lg_webp': self.cover.lg_webp_market,
            } if self.cover else None,
            'preview': {
                'src': self.preview.src_market,
                'src_webp': self.preview.src_webp_market,
                'md': self.preview.md_market,
                'md_webp': self.preview.md_webp_market,
                'sm': self.preview.sm_market,
                'sm_webp': self.preview.sm_webp_market,
                'lg': self.preview.lg_market,
                'lg_webp': self.preview.lg_webp_market,
            } if self.preview else None,
        }

    def _read_children_item(self, item: Children) -> Dict:
        """Read children item."""

        _start, _finish = None, None

        _properties = {
            'is_periodical': self.is_periodical,
            'is_top': any([item.is_top, item.top]),
            'is_global': item.is_global,
            'is_rejected': item.is_rejected,
            'is_rescheduled': item.is_rescheduled,
            'is_open_date': item.has_open_date,
            'is_premiere': item.is_premiere,
            'is_star_cast': item.is_star_cast,
            'is_full_house': item.is_full_house,
        }

        if item.date_start and item.time_start:
            _start = fn.timestamp(
                fn.dt_join(item.date_start, item.time_start),
            )

        if item.date_finish and item.time_finish:
            _finish = fn.timestamp(
                fn.dt_join(item.date_finish, item.time_finish),
            )

        return {
            'pk': item.id,
            'properties': _properties,
            'start': _start,
            'finish': _finish,
        }

    def _read_children(self) -> Union[List[Dict], None]:
        """Read children."""

        if not self.children or len(self.children) <= 0:
            return

        buff = list()
        for _child in self.children:
            buff.append(self._read_children_item(item=_child))

        return buff

    def _read_max_date(self) -> Union[int, None]:
        """Max timestamp include children or empty."""

        if not self.is_periodical:
            return self._read_finish()

        if self.children and len(self.children) > 0:

            buff = list()
            for _e in self.children:
                _ts = fn.timestamp(fn.dt_join(_e.date_finish, _e.time_finish))
                if _ts:
                    buff.append(_ts)

            return max(buff)

    def clean(self) -> Dict:
        """Overrides."""

        location_pk = self.location.id if self.location else None
        layout_pk = self.hall_layout.id if self.hall_layout else None
        category_pk = self.event_category.id if self.event_category else None
        place_pk = self.place.id if self.place else None
        restriction = Restriction(self.restriction)

        return {
            'title': self.title,
            'description': self.description,
            'slug': self.slug,
            'restriction': restriction,
            'place_pk': place_pk,
            'location_pk': location_pk,
            'layout_pk': layout_pk,
            'category_pk': category_pk,
            'start': self._read_start(),
            'finish': self._read_finish(),
            'children': self._read_children(),
            'persons': self._read_persons(),
            'tags': self._read_tags(),
            'properties': self._read_properties(),
            'media': self._read_media(),
            'max_date': self._read_max_date(),
        }
