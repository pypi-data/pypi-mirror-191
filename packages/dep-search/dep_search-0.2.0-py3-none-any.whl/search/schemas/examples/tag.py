"""Tag examples."""

from typing import Tuple, List

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


def example_i18n_tag(
    pk: int,
    name: str,
    slug: str,
) -> Type18nDoc:
    """I18n tag."""

    stub_category = {'id': 1, 'name': 'foo', 'breadcrumbs': []}

    i18n_doc = {
        lang_base: SourceTag(
            id=pk,
            name=name,
            slug=slug,
            event_category=stub_category,
        )
    }

    for foreign in lang_foreign_only:
        i18n_doc.update({
            foreign: SourceTag(
                id=pk,
                name=f'{name} - {foreign}',
                slug=slug,
                event_category=stub_category,
            )
        })

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
    )


all_tags = [
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
