"""Category examples."""

from typing import Tuple, List

from service.ext.testing import faker

from ..raws.category import TypeCategory
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.category import SourceCategory
from ...shared.shared_func import digest_dict
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)


def example_i18n_category(
    pk: int,
    name: str,
    slug: str,
    is_actual: bool = True,
    visible_type: str = 'simple',
) -> Type18nDoc:
    """I18n category."""

    params = {
        'slug': slug,
        'old_slug': f'{slug}_old',
        'is_actual': is_actual,
        'visible_type': visible_type,
        'breadcrumbs': [{'slug': 'category_slug', 'title': 'category_title'}],
        'cover': {
            'src_market': faker.any_image_url(),
            'src_webp_market': faker.any_image_url(),
            'sm_webp_market': faker.any_image_url(),
            'md_market': faker.any_image_url(),
            'md_webp_market': faker.any_image_url(),
            'lg_market': faker.any_image_url(),
            'lg_webp_market': faker.any_image_url(),
        },
        'preview': {
            'src_market': faker.any_image_url(),
            'src_webp_market': faker.any_image_url(),
            'sm_webp_market': faker.any_image_url(),
            'md_market': faker.any_image_url(),
            'md_webp_market': faker.any_image_url(),
            'lg_market': faker.any_image_url(),
            'lg_webp_market': faker.any_image_url(),
        },
        'updated': str(faker.any_dt_day_ago()),
        'created': str(faker.any_dt_day_ago()),
    }

    i18n_doc = {lang_base: SourceCategory(id=pk, name=name, **params)}

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourceCategory(
                id=pk,
                name=f'{name} - {foreign}',
                **params,
            ),
        })

    return i18n_doc


def category_shows() -> Tuple[int, Type18nDoc]:
    """Category_shows."""

    pk = 1
    return pk, example_i18n_category(
        pk=pk,
        name='Шоу',
        slug='shows',
    )


def category_concert() -> Tuple[int, Type18nDoc]:
    """Category concert."""

    pk = 2
    return pk, example_i18n_category(
        pk=pk,
        name='Концерты',
        slug='concerts',
    )


all_categories = [
    category_shows(),
    category_concert(),
]


def src_categories():
    """Src categories."""

    return {c[0]: c[1] for c in all_categories}


def raw_categories(lang: TypeLang) -> List[TypeCategory]:
    """Raw categories."""

    buff = list()

    for category in all_categories:
        pk, i18n = category
        canonical = i18n[lang].clean()
        obj = TypeCategory.create_with_meta(
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
