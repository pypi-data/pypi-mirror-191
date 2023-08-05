""" Helpers for randomized testing """

from __future__ import print_function, division

from random import uniform
import random

from ..core.numbers import I
from ..simplify.simplify import nsimplify
from ..core.containers import Tuple
from ..core.numbers import comp
from ..core.symbol import Symbol
from ..core.compatibility import is_sequence, as_int


def random_complex_number(a=2, b=-1, c=3, d=1, rational=False):
    """
    Return a random complex number.

    To reduce chance of hitting branch cuts or anything, we guarantee
    b <= Im z <= d, a <= Re z <= c
    """
    A, B = uniform(a, c), uniform(b, d)
    if not rational:
        return A + I*B
    return nsimplify(A, rational=True) + I*nsimplify(B, rational=True)


def verify_numerically(f, g, z=None, tol=1.0e-6, a=2, b=-1, c=3, d=1):
    """
    Test numerically that f and g agree when evaluated in the argument z.

    If z is None, all symbols will be tested. This routine does not test
    whether there are Floats present with precision higher than 15 digits
    so if there are, your results may not be what you expect due to round-
    off errors.

    Examples
    ========

    >>> from .. import sin, cos
    >>> from ..abc import x
    >>> from .randtest import verify_numerically as tn
    >>> tn(sin(x)**2 + cos(x)**2, 1, x)
    True
    """
    f, g, z = Tuple(f, g, z)
    z = [z] if isinstance(z, Symbol) else (f.free_symbols | g.free_symbols)
    reps = list(zip(z, [random_complex_number(a, b, c, d) for zi in z]))
    z1 = f.subs(reps).n()
    z2 = g.subs(reps).n()
    return comp(z1, z2, tol)


def test_derivative_numerically(f, z, tol=1.0e-6, a=2, b=-1, c=3, d=1):
    """
    Test numerically that the symbolically computed derivative of f
    with respect to z is correct.

    This routine does not test whether there are Floats present with
    precision higher than 15 digits so if there are, your results may
    not be what you expect due to round-off errors.

    Examples
    ========

    >>> from .. import sin
    >>> from ..abc import x
    >>> from .randtest import test_derivative_numerically as td
    >>> td(sin(x), x)
    True
    """
    from ..core.function import Derivative
    z0 = random_complex_number(a, b, c, d)
    f1 = f.diff(z).subs(z, z0)
    f2 = Derivative(f, z).doit_numerically(z0)
    return comp(f1.n(), f2.n(), tol)


def _randrange(seed=None):
    """Return a randrange generator. ``seed`` can be
        o None - return randomly seeded generator
        o int - return a generator seeded with the int
        o list - the values to be returned will be taken from the list
          in the order given; the provided list is not modified.

    Examples
    ========

    >>> from .randtest import _randrange
    >>> rr = _randrange()
    >>> rr(1000) # doctest: +SKIP
    999
    >>> rr = _randrange(3)
    >>> rr(1000) # doctest: +SKIP
    238
    >>> rr = _randrange([0, 5, 1, 3, 4])
    >>> rr(3), rr(3)
    (0, 1)
    """
    if seed is None:
        return random.randrange
    elif isinstance(seed, int):
        return random.Random(seed).randrange
    elif is_sequence(seed):
        seed = list(seed)  # make a copy
        seed.reverse()

        def give(a, b=None, seq=seed):
            if b is None:
                a, b = 0, a
            a, b = as_int(a), as_int(b)
            w = b - a
            if w < 1:
                raise ValueError('_randrange got empty range')
            try:
                x = seq.pop()
            except AttributeError:
                raise ValueError('_randrange expects a list-like sequence')
            except IndexError:
                raise ValueError('_randrange sequence was too short')
            if a <= x < b:
                return x
            else:
                return give(a, b, seq)
        return give
    else:
        raise ValueError('_randrange got an unexpected seed')


def _randint(seed=None):
    """Return a randint generator. ``seed`` can be
        o None - return randomly seeded generator
        o int - return a generator seeded with the int
        o list - the values to be returned will be taken from the list
          in the order given; the provided list is not modified.

    Examples
    ========

    >>> from .randtest import _randint
    >>> ri = _randint()
    >>> ri(1, 1000) # doctest: +SKIP
    999
    >>> ri = _randint(3)
    >>> ri(1, 1000) # doctest: +SKIP
    238
    >>> ri = _randint([0, 5, 1, 2, 4])
    >>> ri(1, 3), ri(1, 3)
    (1, 2)
    """
    if seed is None:
        return random.randint
    elif isinstance(seed, int):
        return random.Random(seed).randint
    elif is_sequence(seed):
        seed = list(seed)  # make a copy
        seed.reverse()

        def give(a, b, seq=seed):
            a, b = as_int(a), as_int(b)
            w = b - a
            if w < 0:
                raise ValueError('_randint got empty range')
            try:
                x = seq.pop()
            except AttributeError:
                raise ValueError('_randint expects a list-like sequence')
            except IndexError:
                raise ValueError('_randint sequence was too short')
            if a <= x <= b:
                return x
            else:
                return give(a, b, seq)
        return give
    else:
        raise ValueError('_randint got an unexpected seed')
