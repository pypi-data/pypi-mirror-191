"""Search unit."""

from typing import List, Union

from .internals.types import ExpressionError  # noqa
from .internals.search import Search  # noqa
from .internals import operators as op  # noqas
from .internals.operators import (  # noqa
    TypeOpEq,
    TypeOpNe,
    TypeOpGt,
    TypeOpGte,
    TypeOpLt,
    TypeOpLte,
    TypeOpIn,
    TypeOpNotIn,
    TypeOpAnd,
    TypeOpOr,
    TypeExpression,
    Expression,
    ComparisonExpression,
    ComparisonListExpression,
    ConditionalExpression,
    Eq,
    Ne,
    Gt,
    Gte,
    Lt,
    Lte,
    In,
    NotIn,
    And,
    Or,
)


def match_query(
    expressions: List[TypeExpression],
) -> Union[TypeExpression, None]:
    """Match query expression."""

    if not bool(expressions) or len(expressions) == 0:
        return None
    elif len(expressions) == 1:
        return expressions[0]

    return And(expressions)
