"""Search types."""

from typing import Any, Dict, List, Union

from dataclasses import dataclass
from logging import getLogger
from httpx import AsyncClient
from collections import namedtuple
from pydantic import BaseModel

from .types import Expression
from .fn import SafeEncoder  # noqa

from ..schemas.raws import (
    TypeTag,
    TypeMarketEvent,
    TypeCategory,
    TypeDomain,
    TypePlace,
    TypePerson,
)

from ..shared.shared_definitions import (
    lang_base,
    branch_digest,
    IndexNameCategory,
    IndexNameTag,
    IndexNameMarketEvent,
    IndexNameDomain,
    IndexNamePlace,
    IndexNamePerson,
    MethodRawCategory,
    MethodRawDomain,
    MethodRawTag,
    MethodRawMarketEvent,
    MethodRawPlace,
    MethodRawPerson,
)

TypeDomains = Union[None, List[TypeDomain]]
TypeCategories = Union[None, List[TypeCategory]]
TypeTags = Union[None, List[TypeTag]]
TypePlaces = Union[None, List[TypePlace]]
TypePersons = Union[None, List[TypePerson]]
TypeMarketEvents = Union[None, List[TypeMarketEvent]]

TypeProxyResult = namedtuple('TypeProxyResult', ['items', 'count', 'total'])
TypeProxyIndex = namedtuple('TypeProxyIndex', ['method', 'serializer'])

_msg_query_success = 'Query for {name} successfully executed'


log = getLogger(__name__)


@dataclass(frozen=True)
class TagResults:
    """Tag results."""

    items: TypeTags
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass(frozen=True)
class MarketEventResults:
    """Tag results."""

    items: TypeMarketEvents
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass(frozen=True)
class DomainResults:
    """Domain results."""

    items: TypeDomains
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass(frozen=True)
class PlaceResults:
    """Place results."""

    items: TypePlaces
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass(frozen=True)
class PersonResults:
    """Person results."""

    items: TypePersons
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass(frozen=True)
class CategoryResults:
    """Category results."""

    items: TypeCategories
    exists: bool
    count: int
    total: int

    details: Union[None, str]


@dataclass
class Search:
    """Async search."""

    url: str
    token: str
    client: AsyncClient

    __config__ = {
        IndexNameCategory: TypeProxyIndex(
            method=MethodRawCategory,
            serializer=TypeCategory,
        ),
        IndexNameDomain: TypeProxyIndex(
            method=MethodRawDomain,
            serializer=TypeDomain,
        ),
        IndexNameTag: TypeProxyIndex(
            method=MethodRawTag,
            serializer=TypeTag,
        ),
        IndexNameMarketEvent: TypeProxyIndex(
            method=MethodRawMarketEvent,
            serializer=TypeMarketEvent,
        ),
        IndexNamePlace: TypeProxyIndex(
            method=MethodRawPlace,
            serializer=TypePlace,
        ),
        IndexNamePerson: TypeProxyIndex(
            method=MethodRawPerson,
            serializer=TypePerson,
        ),
    }

    # Internals ---------------------------------------------------------------

    def _create_message(
        self,
        method: str,
        expression: Dict[str, Any],
        sorting: Dict[str, int],
        lang: str,
        page: int,
        limit: int,
    ) -> Dict:
        """Create message payload."""

        return {
            'jsonrpc': '2.0',
            'id': 0,
            'method': method,
            'params': {
                'query': {
                    'token': str(self.token),
                    'version': branch_digest,
                    'lang': str(lang),
                    'sorting': sorting,
                    'expression': expression,
                    'page': page,
                    'limit': limit,
                },
            },
        }

    def _read_items(self, response: Dict) -> List[Dict]:  # noqa
        """Read items from response."""
        try:
            return response['result']['data']['results']
        except Exception as _any:
            print(f'Error read response items: {_any}')
            return list()

    def _read_count(self, response: Dict) -> int:  # noqa
        """Read count from response."""
        try:
            return int(response['result']['data']['count'])
        except Exception as _any:
            print(f'Error read response count: {_any}')
            return 0

    def _read_total(self, response: Dict) -> int:  # noqa
        """Read total from response."""
        try:
            return int(response['result']['data']['total'])
        except Exception as _any:
            print(f'Error read response total: {_any}')
            return 0

    async def _lookup(
        self,
        name: str,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[TypeProxyResult, None]:

        items, count, total, raw_expr = (list(), 0, 0, None)

        if expression:
            raw_expr = expression.eval()

        message = self._create_message(
            method=self.__config__[name].method,
            expression=raw_expr,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        response = await self.client.post(url=self.url, json=message)

        if response.status_code == 200:

            body = response.json()

            total = self._read_total(body)
            count = self._read_count(body)

            raw_items = self._read_items(body)
            if len(raw_items) >= 1:
                items = self._serialize(name=name, items=raw_items)

            return TypeProxyResult(items=items, count=count, total=total)

    def _serialize(self, name: str, items: List[Union[BaseModel, Any]]):
        """Serialize items."""

        try:
            raw_class = self.__config__[name].serializer
            return [raw_class(**item) for item in items]
        except Exception as _any_exc:
            log.error(f'Serialize error: {_any_exc}')
            return list()

    async def _results_or_empty(
        self,
        name: str,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[TypeProxyResult, None]:
        """Results or empty."""

        try:
            return await self._lookup(
                name=name,
                expression=expression,
                sorting=sorting,
                lang=lang,
                limit=limit,
                page=page,
            )
        except Exception as _query_exc:  # noqa
            log.error(
                f'{name} query: {_query_exc}',
                extra={
                    'expression': expression,
                    'sorting': sorting,
                    'limit': limit,
                    'page': page,
                    'lang': lang,
                },
            )
            return

    # Exports -----------------------------------------------------------------

    async def market_events(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> MarketEventResults:
        """Market event results."""

        results = await self._results_or_empty(
            name=IndexNameMarketEvent,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return MarketEventResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return MarketEventResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNameMarketEvent),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )

    async def tags(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> TagResults:
        """Search tags."""

        results = await self._results_or_empty(
            name=IndexNameTag,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return TagResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return TagResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNameTag),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )

    async def domains(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> DomainResults:
        """Search domains."""

        results = await self._results_or_empty(
            name=IndexNameDomain,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return DomainResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return DomainResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNameDomain),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )

    async def places(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> PlaceResults:
        """Search domains."""

        results = await self._results_or_empty(
            name=IndexNamePlace,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return PlaceResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return PlaceResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNamePlace),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )

    async def persons(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> PersonResults:
        """Search persons."""

        results = await self._results_or_empty(
            name=IndexNamePerson,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return PersonResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return PersonResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNamePerson),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )

    async def categories(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> CategoryResults:
        """Search categories."""

        results = await self._results_or_empty(
            name=IndexNameCategory,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        skip_conditions = (
            not results,
            (results.count and not bool(results.count)),
            (not bool(results.items)),
        )

        if any(skip_conditions):

            return CategoryResults(
                items=list(),
                details='No results',
                exists=False,
                count=0,
                total=0,
            )

        return CategoryResults(
            items=results.items,
            details=_msg_query_success.format(name=IndexNameCategory),
            exists=True,
            count=int(results.count),  # noqa
            total=int(results.total),  # noqa
        )
