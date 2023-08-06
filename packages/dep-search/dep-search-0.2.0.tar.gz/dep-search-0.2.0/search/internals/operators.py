"""Query operators."""

from typing import Union

from .types import (  # noqa type imports
    Expression,
    ComparisonExpression,
    ComparisonListExpression,
    ConditionalExpression,
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
)


class Eq(ComparisonExpression):
    """Eq expression, syntax: {field: {$eq: <value>}}."""

    __type__ = TypeOpEq


class Ne(ComparisonExpression):
    """Ne expression, syntax: {field: {$ne: value}}."""

    __type__ = TypeOpNe


class Gt(ComparisonExpression):
    """Gt expression, syntax: {field: {$gt: value}}."""

    __type__ = TypeOpGt


class Gte(ComparisonExpression):
    """Gte expression, syntax: {field: {$gte: value}}."""

    __type__ = TypeOpGte


class Lt(ComparisonExpression):
    """Lt expression, syntax: {field: {$lt: value}}."""

    __type__ = TypeOpLt


class Lte(ComparisonExpression):
    """Gte expression, syntax: {field: {$lte: value}}."""

    __type__ = TypeOpLte


class In(ComparisonListExpression):
    """In expression, syntax: {field: {$in: [<value1>, ... <valueN>]}}."""

    __type__ = TypeOpIn


class NotIn(ComparisonListExpression):
    """NotIn expression, syntax: {field: {$nin: [<value1>, ... <valueN>]}}."""

    __type__ = TypeOpNotIn


class And(ConditionalExpression):
    """And expression, syntax: {$and: [{ <expr1> }, ... , {<exprN>}]}."""

    __type__ = TypeOpAnd


class Or(ConditionalExpression):
    """Or expression, syntax: {$or: [{ <expr1> }, ... , {<exprN>}]}."""

    __type__ = TypeOpOr


TypeExpression = Union[Eq, Ne, Gt, Gte, Lt, Lte, In, NotIn, And, Or]


__all__ = (
    'TypeExpression',
    'Expression',
    'ComparisonExpression',
    'ComparisonListExpression',
    'ConditionalExpression',
    'TypeOpEq',
    'TypeOpNe',
    'TypeOpGt',
    'TypeOpGte',
    'TypeOpLt',
    'TypeOpLte',
    'TypeOpIn',
    'TypeOpNotIn',
    'TypeOpAnd',
    'TypeOpOr',
    'Eq',
    'Ne',
    'Gt',
    'Gte',
    'Lt',
    'Lte',
    'In',
    'NotIn',
    'And',
    'Or',
)
