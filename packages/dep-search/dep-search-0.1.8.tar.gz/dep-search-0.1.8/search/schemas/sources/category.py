"""Source category."""

from typing import Dict, List, Union

from ..common_types import (
    BreadCrumbs,
    VisibleType,
    SizedSourceMarketImage,
    builtins,
)


class SourceCategory(builtins.TypeSource):
    """Source category."""

    id: int
    name: str

    is_actual: bool
    visible_type: VisibleType

    slug: str
    old_slug: Union[str, None]

    breadcrumbs: Union[List[BreadCrumbs], None]

    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage

    updated: str
    created: str

    def clean(self) -> Dict:
        """Overrides."""

        return {
            'name': self.name,
            'slug': self.slug,
            'old_slug': self.old_slug,
            'is_actual': self.is_actual,
            'visible_type': self.visible_type,
            'breadcrumbs': self.breadcrumbs,
            'media': {
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
            },
        }
