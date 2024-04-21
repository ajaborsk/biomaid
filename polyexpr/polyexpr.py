"""
"""

from _ast import Name
import ast
from copy import deepcopy
from typing import Any, Self


class ExpressionNames(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        self.names = set()
        super().__init__(*args, **kwargs)

    def visit_Name(self, node: Name) -> Any:
        self.names.add(node.id)
        return super().generic_visit(node)


class PolyExpr:
    """A polyexpression is a expression that can be created with a string and converted to
    some language expressions (including python).
    It can be safe since available names (aka "builtins") have to be explicitly given
    """

    def __init__(self, expression: str | Self | ast.Expression, names=None):
        self.names = names or {}

        if isinstance(expression, PolyExpr):
            self.tree = deepcopy(expression.tree)
        elif isinstance(expression, ast.Expression):
            self.tree = expression
        else:
            self.tree = ast.parse(expression, mode='eval')

    def used_names(self) -> set:
        visitor = ExpressionNames()
        visitor.visit(self.tree)
        return visitor.names

    def transform(self, transformer: ast.NodeTransformer):
        tree = deepcopy(self.tree)
        tree = ast.fix_missing_locations(transformer.visit(tree))
        return PolyExpr(tree)

    def as_string(self):
        return ast.unparse(self.tree)

    def as_function(self, names: tuple[str] | None = None, builtins: dict | None = None):
        """
        Returns a function that takes some variables as named parameters and returns the computed value
        (which can be any python object, not necesserally a litteral)
        """
        builtins = builtins or dict()
        names = names or tuple()

        if not (set(builtins.keys()) | set(names)).issuperset(self.used_names()):
            raise RuntimeError(
                (
                    "Expression '{}' can't be converted to python function"
                    " since not all used names are provided ({} not provided)"
                ).format(repr(self), self.used_names().difference(set(builtins) | set(names)))
            )

        node = ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=name) for name in names],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=self.tree.body,
            lineno=0,
            col_offset=1,
        )
        node = ast.fix_missing_locations(node)
        return eval(compile(ast.Expression(node), filename='<polyexpr>', mode='eval'), {'__builtins__': builtins}, {})

    def as_value(self):
        raise NotImplementedError()

    def __add__(self, other):
        return NotImplemented

    def __sub__(self, other):
        return NotImplemented

    def __mul__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    def __repr__(self):
        return "PolyExpr<'" + ast.unparse(self.tree) + "'>"


# =================================================================================================================================

from django.db.models import Q, F, Value  # noqa


class PolyExprTransformer(ast.NodeTransformer):
    def __init__(self, fieldnames, builtins, mode='django'):
        self.fielnames = fieldnames
        self.builtins = builtins
        self.mode = mode
        super().__init__()

    def visit_Name(self, node: Name) -> Any:
        if node.id in self.builtins:
            # The name is a builtins => do nothing
            return node
        elif node.id == node.id.upper():
            # The name is uppercase => it's a constant => treat as a Value()
            return ast.Call(ast.Name('__value', ctx=ast.Load()), [node], [], ctx=node.ctx)
        else:
            # self._dependencies.add(node.id)
            return ast.Call(
                ast.Name('__f', ctx=node.ctx),
                [ast.Constant(node.id, ctx=node.ctx)],
                [],
                ctx=node.ctx,
            )


def django_orm_expression(polyexpr: PolyExpr, builtins: dict, values: dict, fieldnames: set):

    orm_expr = polyexpr.transform(
        PolyExprTransformer(fieldnames, builtins=set(values.keys()) | set(polyexpr.names), mode='django')
    ).as_function(
        names={
            'USER',
        },
        builtins=builtins,
    )
    # print(f"  {orm_expr=}")

    return orm_expr
