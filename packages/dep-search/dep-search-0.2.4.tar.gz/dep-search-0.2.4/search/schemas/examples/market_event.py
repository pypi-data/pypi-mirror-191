"""Event examples."""

from typing import Dict, Tuple, List
from datetime import timedelta
from uuid import uuid4

from service.ext import fn
from service.ext.testing import faker

from ..raws.market_event import TypeMarketEvent
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources import SourceMarketEvent
from ...shared.shared_func import digest_dict
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)


def example_i18n_event(
    pk: int,
    title: str,
    slug: str,
    date_start: str = None,
    date_finish: str = None,
    time_start: str = None,
    time_finish: str = None,
    description: str = '',
    is_periodical: bool = False,
    is_show_hint: bool = False,
    is_global: bool = False,
    is_rescheduled: bool = False,
    is_rejected: bool = False,
    is_premiere: bool = False,
    is_full_house: bool = False,
    is_top: bool = False,
    is_pushkin: bool = False,
    is_fan_id: bool = False,
    restriction: int = 4,
    is_star_cast: bool = False,
    is_open_date: bool = False,
    is_certificate_event: bool = False,
    widget: Dict = None,
    children: List[Dict] = None,
    date: str = None,
) -> Type18nDoc:
    """I18n tag."""

    default_field = {
        'date': date,
        'slug': slug,
        'date_start': date_start,
        'date_finish': date_finish,
        'time_start': time_start,
        'time_finish': time_finish,
        'description': description,
        'is_periodical': is_periodical,
        'is_top': is_top,
        'top': is_top,
        'is_global': is_global,
        'is_rejected': is_rejected,
        'is_rescheduled': is_rescheduled,
        'is_premiere': is_premiere,
        'is_full_house': is_full_house,
        'is_show_hint': is_show_hint,
        'has_open_date': is_open_date,
        'is_star_cast': is_star_cast,
        'is_pushkin': is_pushkin,
        'is_fan_id': is_fan_id,
        'restriction': restriction,
        'is_certificate_event': is_certificate_event,
        'hint_text': 'Text annotation',
        'seo_short_name_with_preposition': '...',
        'is_filled': True,
        'fill_by_template': True,
        'widget': widget,
    }

    i18n_doc = {
        lang_base: SourceMarketEvent(
            id=pk,
            title=title,
            children=children,
            event_category={
                'id': 1,
                'name': 'stub',
                'breadcrumbs': []
            },
            **default_field,
        )
    }

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourceMarketEvent(
                id=pk,
                title=f'{title} - {foreign}',
                children=children,

                event_category={
                    'id': faker.any_int_pos(),
                    'name': 'Лучшая схема',
                    'hall_id': faker.any_int_pos(),
                    'breadcrumbs': [],
                },
                **default_field,
            ),
        })

    return i18n_doc


def event_freak_fest() -> Tuple[int, Type18nDoc]:
    """Event freak fest."""

    pk = 1

    pk1_start = faker.any_dt_future_day()
    pk1_finish = pk1_start + timedelta(hours=2)

    pk1_start_date, pk1_start_time = fn.dt_split(pk1_start)
    pk1_finish_date, pk1_finish_time = fn.dt_split(pk1_finish)

    return pk, example_i18n_event(
        pk=pk,
        title='Фрик фест',
        slug='freak_fest',
        is_periodical=False,
        date_start=str(pk1_start_date),
        date_finish=str(pk1_finish_date),
        time_start=str(pk1_start_time),
        time_finish=str(pk1_finish_time),
        children=None,
    )


def event_panin_cinema() -> Tuple[int, Type18nDoc]:
    """Event panin cinema."""

    pk = 2

    pk3_start = faker.any_dt_future_day()
    pk3_finish = pk3_start + timedelta(hours=2)

    pk3_start_date, pk3_start_time = fn.dt_split(pk3_start)
    pk3_finish_date, pk3_finish_time = fn.dt_split(pk3_finish)

    pk4_start = pk3_start + timedelta(days=10)
    pk4_finish = pk4_start + timedelta(hours=2)
    pk4_start_date, pk4_start_time = fn.dt_split(pk4_start)
    pk4_finish_date, pk4_finish_time = fn.dt_split(pk4_finish)

    children = [
        {
            'id': 3,
            'top': True,
            'is_top': True,
            'widget': str(uuid4()),
            'is_global': False,
            'is_hidden': False,
            'parent_id': 2,
            'date_start': str(pk3_start_date),
            'time_start': str(pk3_start_time),
            'date_finish': str(pk3_finish_date),
            'time_finish': str(pk3_finish_time),
            'is_premiere': False,
            'is_rejected': False,
            'display_type': 10,
            'is_star_cast': False,
            'has_open_date': False,
            'is_full_house': False,
            'is_rescheduled': False
        },
        {
            'id': 4,
            'top': True,
            'is_top': True,
            'widget': str(uuid4()),
            'is_global': False,
            'is_hidden': False,
            'parent_id': 2,
            'date_start': str(pk4_start_date),
            'time_start': str(pk4_start_time),
            'date_finish': str(pk4_finish_date),
            'time_finish': str(pk4_finish_time),
            'is_premiere': False,
            'is_rejected': False,
            'display_type': 20,
            'is_star_cast': False,
            'has_open_date': False,
            'is_full_house': False,
            'is_rescheduled': False
        },
    ]

    return pk, example_i18n_event(
        pk=pk,
        title='Лучшее от Панина на большом экране',
        slug='panin_cinema',
        is_periodical=True,
        children=children,
        date=None,
    )


all_market_events = [
    event_freak_fest(),
    event_panin_cinema(),
]


def src_market_events():
    """Src events."""

    return {event[0]: event[1] for event in all_market_events}


def raw_market_events(lang: TypeLang) -> List[TypeMarketEvent]:
    """Raw market events."""

    buff = list()

    for event in all_market_events:
        pk, i18n = event
        canonical = i18n[lang].clean()
        obj = TypeMarketEvent.create_with_meta(
            normalized_doc=canonical,
            meta=Meta(
                pk=str(pk),
                lang=lang,
                checksum=digest_dict(canonical),
                commit=fallback_digest,
                branch=branch_digest,
            ),
        )
        buff.append(obj)

    return buff
