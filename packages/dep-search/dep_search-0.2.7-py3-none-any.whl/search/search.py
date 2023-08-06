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
    TypeOpRegex,
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
    Contains,
    IContains,
    In,
    NotIn,
    And,
    Or,
)


def match_query(
    expressions: List[TypeExpression],
) -> Union[TypeExpression, None]:
    """Match query expression."""

    expr_arr = [  # not empty only
        _expr
        for _expr in expressions
        if _expr.value is not None
    ]

    if not bool(expr_arr) or len(expr_arr) == 0:
        return None
    elif len(expr_arr) == 1:
        if expr_arr[0].value is None:
            return None
        return expr_arr[0]
    else:
        return And(expr_arr)
