"""Place examples."""

from typing import Tuple, List

from service.ext.testing import faker

from ..raws.place import TypePlace
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.place import SourcePlace
from ...shared.shared_func import digest_dict
from ...shared.shared_definitions import (
    lang_base,
    lang_foreign_only,
    branch_digest,
    fallback_digest,
)


def example_i18n_place(
    pk: int,
    name: str,
    description: str,
    how_to_get: str,
    schema_title: str,
    address: str,
    slug: str,
) -> Type18nDoc:
    """I18n place."""

    images_cover_preview = {
        'src_market': faker.any_image_url(),
        'src_webp_market': faker.any_image_url(),
        'sm_webp_market': faker.any_image_url(),
        'md_webp_market': faker.any_image_url(),
        'lg_webp_market': faker.any_image_url(),
    }

    gallery = [faker.any_image_url(), faker.any_image_url()]
    gallery_webp = [faker.any_image_url(), faker.any_image_url()]
    schema_url = faker.any_image_url()
    schema_webp = faker.any_image_url()
    schemas_urls = [faker.any_image_url(), faker.any_image_url()]
    schemas_webp = [faker.any_image_url(), faker.any_image_url()]

    params = {
        'slug': slug,
        'parent': None,
        'popularity': faker.any_int_pos(),
        'count': 0,
        'url': faker.any_image_url(),
        'location': {'id': 1, 'name': '$location_name'},
        'place_type': {'id': 1, 'name': '$place_type'},
        'gallery': gallery,
        'gallery_webp': gallery_webp,
        'schema': schema_url,
        'schema_webp': schema_webp,
        'schemas': schemas_urls,
        'schemas_webp': schemas_webp,
        'cover': images_cover_preview,
        'preview': images_cover_preview,
    }

    i18n_doc = {
        lang_base: SourcePlace(
            id=pk,
            name=name,
            description=description,
            address=address,
            how_to_get=how_to_get,
            schema_title=schema_title,
            **params,
        )
    }

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourcePlace(
                id=pk,
                name=f'{name} - {foreign}',
                address=f'{address} - {foreign}',
                description=f'{description} - {foreign}',
                how_to_get=f'{how_to_get} - {foreign}',
                schema_title=f'{schema_title} - {foreign}',
                **params,
            ),
        })

    return i18n_doc


def place_msk() -> Tuple[int, Type18nDoc]:
    """Place msk."""

    pk = 1
    return pk, example_i18n_place(
        pk=pk,
        slug='msk_luxury_appartments',
        name='Москоу Лухари Аппартменс',
        description='Очень мажорное место',
        how_to_get='Вас должен привезти свой водитель, не парьтесь',
        schema_title='Сказано, не парьтесь',
        address='В москве для своих',
    )


def place_spb() -> Tuple[int, Type18nDoc]:
    """Domain spb."""

    pk = 2
    return pk, example_i18n_place(
        pk=pk,
        slug='spb_looounge',
        name='Чилим в Питере',
        description='Не для вас роза цвела',
        how_to_get='Обходите сосули и не поцарапайте тачку владельца',
        schema_title='От рубика рукой подать',
        address='Ну рядом же',
    )


all_places = [place_msk(), place_spb()]


def src_places():
    """Src places."""

    return {p[0]: p[1] for p in all_places}


def raw_places(lang: TypeLang) -> List[TypePlace]:
    """Raw places."""

    buff = list()

    for place in all_places:
        pk, i18n = place
        canonical = i18n[lang].clean()
        obj = TypePlace.create_with_meta(
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
