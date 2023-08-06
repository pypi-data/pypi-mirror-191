"""Query lookup operators."""

from __future__ import annotations

from typing import Any, Dict, List, Union

# Comparison query operators

TypeOpEq = '$eq'
TypeOpNe = '$ne'
TypeOpGt = '$gt'
TypeOpGte = '$gte'
TypeOpLt = '$lt'
TypeOpLte = '$lte'
TypeOpIn = '$in'
TypeOpNotIn = '$nin'

# Logical query operators

TypeOpAnd = '$and'
TypeOpOr = '$or'

# Regex
TypeOpRegex = '$regex'

TypeComparisonOperators = (
    TypeOpEq,
    TypeOpNe,
    TypeOpGt,
    TypeOpGte,
    TypeOpLt,
    TypeOpLte,
    TypeOpIn,
    TypeOpNotIn,
    TypeOpRegex,
)

TypeLogicalOperators = (TypeOpAnd, TypeOpOr, )

TypeOperators = (*TypeComparisonOperators, *TypeLogicalOperators, )

SchemaDataType = {'string': str, 'boolean': bool, 'integer': int}


class ExpressionError(RuntimeError):
    """Expression error."""

    pass


class Expression(object):
    """Expression."""

    __type__: str = None

    @classmethod
    def _nested_level(cls, field_name) -> int:
        """Nested level of field."""
        return str(field_name).count('.')

    @classmethod
    def real_verbose_type(cls, prop_definition) -> Any:
        """Verbose type property to real type."""

        verbose = prop_definition.get('type')
        try:
            return SchemaDataType[verbose]
        except Exception:  # noqa
            raise ExpressionError(f'Unknown type: {verbose}')

    def eval(self) -> Dict:
        """Eval as raw typed dict."""

        raise NotImplementedError()

    @classmethod
    def raise_fail(cls, msg: str, details: str = None):
        """Raise fail validation."""

        if bool(help):
            raise ExpressionError(f'{msg}, {details}')
        else:
            raise ExpressionError(msg)

    def validate(self, schema: Dict) -> None:
        """Validate."""

        raise NotImplementedError()


class ComparisonExpression(Expression):
    """Comparison expression."""

    def __init__(self, field: str, value: Union[None, bool, int, str]):
        """Init."""

        self.field = field
        self.value = value

    def eval(self) -> Dict:
        """Raw repr."""

        return {self.field: {self.__type__: self.value}}

    def validate(self, schema: Dict) -> None:
        """Validate."""

        _defs: Dict = schema.get('definitions')
        _props: Dict = schema.get('properties')

        level = self._nested_level(self.field)

        if level > 1:
            self.raise_fail(msg='Nesting level exceeded')

        if level == 0:

            if self.field not in _props.keys():
                self.raise_fail(
                    msg=f'Unknown field name `{self.field}`',
                    details=f'use {list(_props.keys())} instead',
                )

            schema_type = self.real_verbose_type(_props[self.field])
            if type(self.value) != schema_type:
                self.raise_fail(
                    msg=f'Invalid type value `{self.value}`',
                    details=f'use, {schema_type} type',
                )

            return

        base_name, nested_name = self.field.split('.')

        try:
            _ref: str = _props[base_name]['$ref']
        except Exception:  # noqa
            self.raise_fail(
                msg=f'Unknown field name `{base_name}`',
                details=f'use {list(_props.keys())}',
            )
            return

        _alias = _ref.split('/')[-1]
        _schema = _defs[_alias]['properties']

        if nested_name not in _schema.keys():
            self.raise_fail(
                msg=f'Unknown nested field name `{nested_name}`',
                details=f'use {base_name}.{list(_schema.keys())}',
            )

        _nested_schema_type = self.real_verbose_type(_schema[nested_name])
        if type(self.value) != _nested_schema_type:
            self.raise_fail(
                msg=f'Invalid type value `{self.value}`',
                details=f'use, {_nested_schema_type} type instead',
            )


class ComparisonListExpression(Expression):
    """Comparison list expression - for $in and $nin."""

    def __init__(self, field: str, values: List[Union[None, bool, int, str]]):
        """Init."""

        self.field = field
        self.values = values

    def eval(self) -> Dict:
        """Raw repr."""

        return {self.field: {self.__type__: self.values}}

    def validate(self, schema: Dict) -> None:
        """Validate."""

        _defs: Dict = schema.get('definitions')
        _props: Dict = schema.get('properties')

        if not isinstance(self.values, list):
            self.raise_fail(
                msg=f'{self.__type__} accepts list values',
                details=f'use list of values instead {type(self.values)}',
            )

        level = self._nested_level(self.field)

        if level > 1:
            self.raise_fail(msg='Nesting level exceeded')

        if level == 0:

            if self.field not in _props.keys():
                self.raise_fail(
                    msg=f'Unknown field name `{self.field}`',
                    details=f'use {list(_props.keys())} instead',
                )

            schema_type = self.real_verbose_type(_props[self.field])
            if not all([type(_v) == schema_type for _v in self.values]):
                self.raise_fail(
                    msg=f'Invalid type values `{self.values}`',
                    details=f'use, {schema_type} type',
                )

            return

        base_name, nested_name = self.field.split('.')

        try:
            _ref: str = _props[base_name]['$ref']
        except Exception:  # noqa
            self.raise_fail(
                msg=f'Unknown field name `{base_name}`',
                details=f'use {list(_props.keys())}',
            )
            return

        _alias = _ref.split('/')[-1]
        _schema = _defs[_alias]['properties']

        if nested_name not in _schema.keys():
            self.raise_fail(
                msg=f'Unknown nested field name `{nested_name}`',
                details=f'use {base_name}.{list(_schema.keys())}',
            )

        _nested_schema_type = self.real_verbose_type(_schema[nested_name])
        if not all([type(_v) == _nested_schema_type for _v in self.values]):
            self.raise_fail(
                msg=f'Invalid type values `{self.values}`',
                details=f'use, {_nested_schema_type} type',
            )


class ConditionalExpression(Expression):
    """Conditional expression for $and and $or."""

    def __init__(self, expressions: List[Expression]) -> None:
        """Init."""

        self.expressions = expressions

    def eval(self) -> Dict:
        """Raw repr."""

        return {
            self.__type__: [
                expr.eval()
                for expr in self.expressions
                if hasattr(expr, 'eval') and callable(expr.eval)
            ]
        }

    def validate(self, schema: Dict) -> None:
        """Validate."""

        if not bool(self.expressions):
            self.raise_fail(
                msg=f'Conditions for {self.__type__} not passed',
            )

        if not isinstance(self.expressions, list):
            self.raise_fail(
                msg=f'Conditions for {self.__type__} is not iterable',
            )

        if not all([isinstance(_ex, Expression) for _ex in self.expressions]):
            self.raise_fail(
                msg=f'Invalid condition types for {self.__type__}',
                details='use Expression types instead',
            )

        for expr in self.expressions:
            expr.validate(schema=schema)
