"""Tag examples."""

from typing import Tuple, List
from service.ext.testing import faker

from ..raws.tag import TypeTag
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...shared.shared_func import digest_dict
from ...schemas.sources.tag import SourceTag
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)

from .category import category_concert

pk_concert, i18n_concert = category_concert()


def example_i18n_tag(
    pk: int,
    name: str,
    slug: str,
    with_category: bool = True,
) -> Type18nDoc:
    """I18n tag."""

    created = str(faker.any_dt_day_ago(days=5))
    updated = str(faker.any_dt_day_ago(days=3))

    params = {
        'name': name,
        'slug': slug,
        'old_slug': f'{slug}_old',
        'created': created,
        'updated': updated,
        'event_category': None,
    }

    if with_category:
        params.update({'event_category': i18n_concert[lang_base]})

    i18n_doc = {lang_base: SourceTag(id=pk, **params)}

    for foreign in lang_foreign_only:

        foreign_params = dict(params)
        foreign_params['name'] = '{name} - {lang}'.format(
            name=params['name'],
            lang=foreign,
        )

        if with_category:
            foreign_params['event_category'] = i18n_concert[foreign]

        i18n_doc.update({foreign: SourceTag(id=pk, **foreign_params)})

    return i18n_doc


def tag_theatre() -> Tuple[int, Type18nDoc]:
    """Tag theatre."""

    pk = 1
    return pk, example_i18n_tag(
        pk=pk,
        name='Театр',
        slug='theatre',
    )


def tag_concert() -> Tuple[int, Type18nDoc]:
    """Tag concert."""

    pk = 2
    return pk, example_i18n_tag(
        pk=pk,
        name='Концерты',
        slug='concert',
        with_category=False,
    )


all_tags = [  # noqa
    tag_theatre(),
    tag_concert(),
]


def src_tags():
    """Src tags."""

    return {tag[0]: tag[1] for tag in all_tags}


def raw_tags(lang: TypeLang) -> List[TypeTag]:
    """Raw tags."""

    buff = list()

    for domain in all_tags:
        pk, i18n = domain
        canonical = i18n[lang].clean()
        obj = TypeTag.create_with_meta(
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
