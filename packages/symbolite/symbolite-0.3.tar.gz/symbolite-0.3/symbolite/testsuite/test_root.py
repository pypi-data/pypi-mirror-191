import pytest

from symbolite.core.operands import Function
from symbolite.core.translators import find_libs_in_stack
from symbolite.symbol.abstract import Symbol

x, y, z = map(Symbol, "x y z".split())

F = Function("F", "", 1)
G = Function("G", "lib", 1)


def test_forward_reverse():
    expr = x + 1
    assert expr.func.name == "__add__"
    assert expr.args == (x, 1)

    expr = 1 + x
    assert expr.func.name == "__radd__"
    assert expr.args == (x, 1)


@pytest.mark.parametrize(
    "expr,result",
    [
        (x < y, "(x < y)"),
        (x <= y, "(x <= y)"),
        (x > y, "(x > y)"),
        (x >= y, "(x >= y)"),
        (x[1], "x[1]"),
        (x[z], "x[z]"),
        (x + y, "(x + y)"),
        (x - y, "(x - y)"),
        (x * y, "(x * y)"),
        (x @ y, "(x @ y)"),
        (x / y, "(x / y)"),
        (x // y, "(x // y)"),
        (x % y, "(x % y)"),
        (x**y, "(x ** y)"),
        (x**y % z, "((x ** y) % z)"),
        (pow(x, y, z), "pow(x, y, z)"),
        (x << y, "(x << y)"),
        (x >> y, "(x >> y)"),
        (x & y, "(x & y)"),
        (x ^ y, "(x ^ y)"),
        (x | y, "(x | y)"),
        # Reverse
        (1 + y, "(1 + y)"),
        (1 - y, "(1 - y)"),
        (1 * y, "(1 * y)"),
        (1 @ y, "(1 @ y)"),
        (1 / y, "(1 / y)"),
        (1 // y, "(1 // y)"),
        (1 % y, "(1 % y)"),
        (1**y, "(1 ** y)"),
        (1 << y, "(1 << y)"),
        (1 >> y, "(1 >> y)"),
        (1 & y, "(1 & y)"),
        (1 ^ y, "(1 ^ y)"),
        (1 | y, "(1 | y)"),
        (-x, "(-x)"),
        (+x, "(+x)"),
        (~x, "(~x)"),
        (F(x), "F(x)"),
        (G(x), "lib.G(x)"),
    ],
)
def test_str(expr, result):
    assert str(expr) == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + 2 * y, x + 2 * z),
        (x + 2 * F(y), x + 2 * F(z)),
    ],
)
def test_subs(expr, result):
    assert expr.subs({y: z}) == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + 2 * y, x + 2 * z),
        (x + 2 * F(y), x + 2 * F(z)),
    ],
)
def test_subs_by_name(expr, result):
    assert expr.subs_by_name(y=z) == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + y, {"x", "y"}),
        (x[z], {"x", "z"}),
        (F(x), {"F", "x"}),
        (G(x), {"x"}),
    ],
)
def test_symbol_names(expr, result):
    assert expr.symbol_names() == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + y, {"x", "y", "libsymbol.__add__"}),
        (x[z], {"x", "z", "libsymbol.__getitem__"}),
        (F(x), {"F", "x"}),
        (G(x), {"x", "lib.G"}),
    ],
)
def test_symbol_names_ops(expr, result):
    assert expr.symbol_names(None) == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + y, set()),
        (x[z], set()),
        (F(x), set()),
        (
            G(x),
            {
                "lib.G",
            },
        ),
    ],
)
def test_symbol_names_namespace(expr, result):
    assert expr.symbol_names(namespace="lib") == result


class Scalar(Symbol):
    pass


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + 2 * y, 1 + 2 * 3),
        # (x + 2 * F(y), x + 2 * F(z)),
    ],
)
def test_eval_str(expr, result):
    assert eval(str(expr.subs_by_name(x=1, y=3))) == result


@pytest.mark.parametrize(
    "expr,result",
    [
        (x + 2 * y, 1 + 2 * 3),
        # (x + 2 * F(y), x + 2 * F(z)),
    ],
)
def test_eval(expr, result):
    assert expr.subs_by_name(x=1, y=3).eval() == result


def test_find_libs_in_stack():
    assert "libsymbol" not in find_libs_in_stack()
    assert "libsymbol" not in find_libs_in_stack(x + y)
    from symbolite.symbol import default as libsymbol  # noqa: F401

    assert "libsymbol" in find_libs_in_stack()
    assert "libsymbol" in find_libs_in_stack(x + y)
