"""Common index types."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import namedtuple
from typing import Any, Dict, Optional, List, Type, Union, Set

from pydantic import AnyUrl, BaseModel, Field

TypePK = int
TypeLang = str

TypeDigest = str
TypeName = str
TypeReason = str

TypeTranslate = str
TypeI18Field = Dict[TypeLang, TypeTranslate]

TypeDoc = Type[Union[Any, BaseModel]]
Type18nDoc = Dict[TypeLang, TypeDoc]
TypeLookup = Dict[TypePK, Type18nDoc]

TypeRequestID = Union[str, int, None]
TypeRequestParams = Union[Dict[str, Any], None]
TypeSorting = Dict[str, int]

TypeRawName = str
TypeSchemaRaw = Dict
TypeSchemaSrc = Dict

TypeGist = namedtuple(
    'TypeGist',
    ['name', 'raw', 'src', 'method', 'model', 'parser'],
)

TypeIndexSchema = Dict[TypeRawName, TypeGist]


class QuerySchema(BaseModel):
    """Base query schema."""

    page: Optional[int] = 1
    limit: Optional[int] = 25

    lang: Optional[str] = 'ru'

    expression: Optional[Dict] = None
    sorting: TypeSorting = None


class StrictSecureQuerySchema(QuerySchema):
    """Strict secure query schema."""

    token: str
    version: TypeDigest


class ImportQuerySecureSchema(BaseModel):
    """Strict secure query schema."""

    token: str
    version: TypeDigest


class SecureQuery(BaseModel):
    """Query schema."""

    token: str


class PaginatedResponse(BaseModel):
    """Paginated response - overload your results."""

    page: int = Field(example=1)
    limit: int = Field(example=25)
    count: int = Field(example=25)
    last_page: int = Field(example=5)
    total: int = Field(example=125)

    results: List[Dict]


class SizedImages(BaseModel):
    """Sizes images schema."""

    src: Optional[AnyUrl] = None
    sm: Optional[AnyUrl] = None
    md: Optional[AnyUrl] = None
    lg: Optional[AnyUrl] = None

    src_market: Optional[AnyUrl] = None
    sm_market: Optional[AnyUrl] = None
    md_market: Optional[AnyUrl] = None
    lg_market: Optional[AnyUrl] = None


class Meta(BaseModel):
    """Meta schema."""

    pk: str
    lang: str

    checksum: TypeDigest

    commit: Optional[TypeDigest]
    branch: Optional[TypeDigest]

    unwanted: bool = False


class BaseSource(BaseModel):
    """Any removable type source."""

    delete: Optional[bool] = False
    hidden: Optional[bool] = False
    is_hidden: Optional[bool] = False
    is_delete: Optional[bool] = False


class TypeSource(BaseSource):
    """Type source."""

    def exclude_fields(self) -> Set[str]:  # noqa
        """Not used fields."""

        return {
            'id',
            'delete',
            'is_delete',
            'is_deleted',
            'hidden',
            'is_hidden',
        }

    def clean(self) -> Dict:
        """Normalize source data.  Override in child model if needed.

        Accepts validated source.
        Returns a normalized dict for raw model constructor, except meta.
        """

        normalized = self.dict(exclude=self.exclude_fields())
        return normalized


class TypeRaw(BaseModel):
    """Base raw schema."""

    meta: Optional[Meta]

    @classmethod
    def create_unsigned(cls, raw_doc: Dict):
        """Create unsigned."""

        return cls(**raw_doc)

    @classmethod
    def create_with_meta(cls, normalized_doc: Dict, meta: Meta):
        """Raw doc normalizer.  Override in child model if needed.

        Accepts clean and normalized for raw model dict, except meta.
        Returns raw model instance from raw doc.
        """

        normalized_doc.update({'meta': meta})

        return cls(**normalized_doc)


@dataclass(frozen=True)
class DataRequest:
    """Request data."""

    method: TypeName
    params: TypeRequestParams = field(default_factory=dict)

    id: TypeRequestID = 'unnamed'

    __rpc_version__ = '2.0'

    def as_dict(self) -> Dict:
        """Request obj as dict."""

        return {
            'id': self.id,
            'jsonrpc': self.__rpc_version__,
            'method': self.method,
            'params': self.params,
        }


@dataclass(frozen=True)
class DataResponse:
    """Response data."""

    request: DataRequest
    execution_time_sec: int
    status: int

    result: Optional[Dict] = None
