"""
"""
from _ast import Name
import ast
from copy import deepcopy
from typing import Any


class ExpressionNames(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        self.names = set()
        super().__init__(*args, **kwargs)

    def visit_Name(self, node: Name) -> Any:
        self.names.add(node.id)
        return super().generic_visit(node)


class PolyExpr:
    def __init__(self, expression: str, builtins=None):
        self.builtins = builtins or {}
        try:
            self.tree = ast.parse(expression, mode='eval')
        except SyntaxError:
            self.tree = None
        except ValueError:
            self.tree = None

    def names(self):
        visitor = ExpressionNames()
        visitor.visit(self.tree)
        return visitor.names

    # def as_django_orm_expr(self, **kwargs):
    #     compiled = compile(tree, '<string>', 'eval')
    #     return eval(compiled, all_vars)
    #     # return ~Q(pk__in=[])


# =================================================================================================================================

from django.db.models import Q, F, Value


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
                [ast.Str(node.id, ctx=node.ctx)],
                [],
                ctx=node.ctx,
            )


def django_orm_expression(polyexpr: PolyExpr, values: dict, fieldnames: set):
    tree = deepcopy(polyexpr.tree)
    tree = ast.fix_missing_locations(
        PolyExprTransformer([], builtins=set(values.keys()) | set(polyexpr.builtins), mode='django').visit(tree)
    )

    # Specific builtins
    all_vars = {'__f': F, '__value': Value}
    # The builtins
    all_vars.update({name: value.get('django') for name, value in polyexpr.builtins.items()})
    # Add query/view parameters
    all_vars.update(values)
    # print(f"  {ast.unparse(tree)=} {all_vars=}")

    compiled = compile(tree, '<string>', 'eval')
    orm_expr = eval(compiled, all_vars)
    # print(f"  {orm_expr=}")
    if isinstance(orm_expr, bool):
        if orm_expr:
            return ~Q(pk__in=[])
        else:
            return Q(pk__in=[])
    return orm_expr
