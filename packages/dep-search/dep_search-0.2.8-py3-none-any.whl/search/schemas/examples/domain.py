"""Domain examples."""

from typing import List, Tuple

from ..raws.domain import TypeDomain
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...shared.shared_func import digest_dict
from ...schemas.sources.domain import SourceDomain
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)


def example_i18n_domain(
    pk: int,
    name: str,
    sub_domain: str,
    is_active: bool = True,
    country_code: str = 'ru',
    sort_order: int = 1,
    display_in_cities_list: bool = True,
    subdivision_codes: str = 'mos, mow',
) -> Type18nDoc:
    """I18n domain."""

    if not subdivision_codes:
        subdivision_codes = []

    params = {
        'subdivision_codes': subdivision_codes,
        'locations': [{'id': 1, 'name': '$location_name'}],
        'sort_order': sort_order,
        'sub_domain': sub_domain,
        'display_in_cities_list': display_in_cities_list,
        'is_active': is_active,
        'country_code': country_code,
    }

    i18n_doc = {
        lang_base: SourceDomain(id=pk, name=name, **params)
    }

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourceDomain(
                id=pk,
                name=f'{name} - {foreign}',
                **params,
            ),
        })

    return i18n_doc


def domain_spb() -> Tuple[int, Type18nDoc]:
    """Domain spb."""

    pk = 1
    return pk, example_i18n_domain(
        pk=pk,
        name='Питер',
        sub_domain='spb',
    )


def domain_msk() -> Tuple[int, Type18nDoc]:
    """Domain msk."""

    pk = 2
    return pk, example_i18n_domain(
        pk=pk,
        name='Москва',
        sub_domain='msk',
    )


all_domains = [
    domain_spb(),
    domain_msk(),
]


def src_domains():
    """Src domains."""

    return {d[0]: d[1] for d in all_domains}


def raw_domains(lang: TypeLang) -> List[TypeDomain]:
    """Raw domains."""

    buff = list()

    for domain in all_domains:
        pk, i18n = domain
        canonical = i18n[lang].clean()
        obj = TypeDomain.create_with_meta(
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
