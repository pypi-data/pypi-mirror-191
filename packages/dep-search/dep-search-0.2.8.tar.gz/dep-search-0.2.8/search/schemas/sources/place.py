"""Source tag."""

from typing import Any, Dict, Union

from ..common_types import (
    IdNameSchema,
    LocationSchema,
    SchemaField,
    SizedSourceMarketImage,
    TypeOptionalImage,
    TypeOptionalListImages,
    builtins,
)


class SourcePlace(builtins.TypeSource):
    """Source place."""

    id: int
    slug: str
    name: str
    description: str
    address: str

    location: LocationSchema
    place_type: IdNameSchema

    popularity: Union[int, None]
    count: Union[int, None]
    how_to_get: Union[str, None]

    parent: Union[Any, None]

    url: TypeOptionalImage

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    schema_title: Union[str, None]
    schema_webp: TypeOptionalImage
    schemas_webp: TypeOptionalListImages

    schema_url: TypeOptionalImage = SchemaField(
        alias='schema',
        default=None,
    )
    schemas_urls: TypeOptionalListImages = SchemaField(
        alias='schemas',
        default=None,
    )

    cover: Union[SizedSourceMarketImage, None]
    preview: Union[SizedSourceMarketImage, None]

    updated: Union[str, None]
    created: Union[str, None]

    def clean(self) -> Dict:
        """Overrides."""

        info = {
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'count': self.count,
            'popularity': self.popularity,
            'url': self.url,
            'schema_title': self.schema_title,
            'how_to_get': self.how_to_get,
        }

        media = {
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
            'gallery': self.gallery,
            'gallery_webp': self.gallery_webp,
            'schema_url': self.schema_url,
            'schemas_urls': self.schemas_urls,
            'schema_webp': self.schema_webp,
            'schemas_webp': self.schemas_webp,
        }

        cleaned = {
            'slug': self.slug,
            'location_pk': self.location.id,
            'info': info,
            'media': media,
            'place_type': {
                'pk': self.place_type.id,
                'name': self.place_type.name,
            },
        }

        return cleaned
