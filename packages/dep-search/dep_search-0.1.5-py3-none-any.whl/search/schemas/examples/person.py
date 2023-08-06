"""Person examples."""

from typing import Tuple, List

from service.ext.testing import faker

from ..raws.person import TypePerson
from ...internals.builtins import Type18nDoc, Meta, TypeLang
from ...shared.shared_func import digest_dict
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)
from ...schemas.sources.person import SourcePerson


def example_i18n_person(
    pk: int,
    name: str,
    slug: str,
    description: str,
    position: str,
    person_type: int = 10,
) -> Type18nDoc:
    """I18n person."""

    sized_image = {
        'src_market': faker.any_image_url(),
        'src_webp_market': faker.any_image_url(),
        'sm_webp_market': faker.any_image_url(),
        'md_webp_market': faker.any_image_url(),
        'lg_webp_market': faker.any_image_url(),
    }

    list_images = [faker.any_image_url(), faker.any_image_url()]

    params = {
        'slug': slug,
        'description': description,
        'person_type': person_type,
        'position': position,
        'updated': str(faker.any_dt_day_ago()),
        'created': str(faker.any_dt_day_ago()),
        'main_image': sized_image,
        'cover': sized_image,
        'gallery': list_images,
        'gallery_webp': list_images,
        'tags': [{'id': 1, 'name': 'tag_one'}],
    }

    i18n_doc = {
        lang_base: SourcePerson(id=pk, name=name, **params)
    }

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourcePerson(
                id=pk,
                name=f'{name} - {foreign}',
                **params,
            ),
        })

    return i18n_doc


def person_vcoy() -> Tuple[int, Type18nDoc]:
    """Person vcoy."""

    pk = 1

    return pk, example_i18n_person(
        pk=pk,
        name='Виктор Цой',
        slug='vcoy',
        description='Лучшее от Виктора Цоя',
        position='Позийшан!? Я турист',
        person_type=10,
    )


def person_aria() -> Tuple[int, Type18nDoc]:
    """Person aria."""

    pk = 3
    return pk, example_i18n_person(
        pk=pk,
        name='Ария',
        slug='aria',
        description='Норм тема!',
        position='Лучшая позиайшана!',
        person_type=10,
    )


all_persons = [
    person_aria(),
    person_vcoy(),
]


def src_persons():
    """Src persons."""

    return {p[0]: p[1] for p in all_persons}


def raw_persons(lang: TypeLang) -> List[TypePerson]:
    """Raw persons."""

    buff = list()

    for person in all_persons:
        pk, i18n = person
        canonical = i18n[lang].clean()
        obj = TypePerson.create_with_meta(
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
