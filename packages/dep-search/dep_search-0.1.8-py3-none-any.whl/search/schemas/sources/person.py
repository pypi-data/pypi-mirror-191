"""Source market event."""

from typing import Dict, List, Union

from ..common_types import (
    PersonType,
    PersonTypeSource,
    TypeOptionalListImages,
    SizedSourceMarketImage,
    builtins,
)


class SourcePerson(builtins.TypeSource):
    """Source person."""

    id: int
    slug: str
    name: str
    description: str
    position: str

    person_type: PersonTypeSource

    main_image: Union[SizedSourceMarketImage, None]
    cover: Union[SizedSourceMarketImage, None]
    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    tags: Union[List[Dict], None]

    updated: Union[str, None]
    created: Union[str, None]

    def _read_person_type(self) -> PersonType:
        """Read person type."""

        _ptypes = {
            PersonTypeSource.ARTIST: PersonType.artist,
            PersonTypeSource.SPORTSMAN: PersonType.sportsman,
        }

        return _ptypes[self.person_type]

    def _read_tags(self) -> Union[List[int], None]:
        """Read person tags."""
        if bool(self.tags) and len(self.tags) > 0:
            return [_t['id'] for _t in self.tags if _t.get('id')]

    def _read_media(self) -> Dict:
        """Read media."""

        main = {  # noqa
            'src': self.main_image.src_market,
            'src_webp': self.main_image.src_webp_market,
            'md': self.main_image.md_market,
            'md_webp': self.main_image.md_webp_market,
            'sm': self.main_image.sm_market,
            'sm_webp': self.main_image.sm_webp_market,
            'lg': self.main_image.lg_market,
            'lg_webp': self.main_image.lg_webp_market,
        } if self.main_image else None

        cover = {
            'src': self.cover.src_market,
            'src_webp': self.cover.src_webp_market,
            'md': self.cover.md_market,
            'md_webp': self.cover.md_webp_market,
            'sm': self.cover.sm_market,
            'sm_webp': self.cover.sm_webp_market,
            'lg': self.cover.lg_market,
            'lg_webp': self.cover.lg_webp_market,
        } if self.cover else None

        return {
            'main': main,
            'cover': cover,
            'gallery': self.gallery if self.gallery else list(),
            'gallery_webp': self.gallery_webp if self.gallery_webp else list(),
        }

    def clean(self) -> Dict:
        """Clean person source."""

        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'position': self.position,
            'person_type': self._read_person_type(),
            'media': self._read_media(),
            'tags': self._read_tags(),
        }
