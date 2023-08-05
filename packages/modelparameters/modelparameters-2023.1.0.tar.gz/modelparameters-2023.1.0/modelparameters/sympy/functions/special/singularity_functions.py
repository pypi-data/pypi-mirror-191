from __future__ import print_function, division

from ...core.function import Function, ArgumentIndexError
from ...core import S, sympify, oo, diff
from ...core.logic import fuzzy_not
from ...core.relational import Eq
from ..elementary.complexes import im
from ..elementary.piecewise import Piecewise
from .delta_functions import DiracDelta, Heaviside

###############################################################################
############################# SINGULARITY FUNCTION ############################
###############################################################################


class SingularityFunction(Function):
    r"""
    The Singularity functions are a class of discontinuous functions. They take a
    variable, an offset and an exponent as arguments. These functions are
    represented using Macaulay brackets as :

    SingularityFunction(x, a, n) := <x - a>^n

    The singularity function will automatically evaluate to
    ``Derivative(DiracDelta(x - a), x, -n - 1)`` if ``n < 0``
    and ``(x - a)**n*Heaviside(x - a)`` if ``n >= 0``.


    Examples
    ========

    >>> from ... import SingularityFunction, diff, Piecewise, DiracDelta, Heaviside, Symbol
    >>> from ...abc import x, a, n
    >>> SingularityFunction(x, a, n)
    SingularityFunction(x, a, n)
    >>> y = Symbol('y', positive=True)
    >>> n = Symbol('n', nonnegative=True)
    >>> SingularityFunction(y, -10, n)
    (y + 10)**n
    >>> y = Symbol('y', negative=True)
    >>> SingularityFunction(y, 10, n)
    0
    >>> SingularityFunction(x, 4, -1).subs(x, 4)
    oo
    >>> SingularityFunction(x, 10, -2).subs(x, 10)
    oo
    >>> SingularityFunction(4, 1, 5)
    243
    >>> diff(SingularityFunction(x, 1, 5) + SingularityFunction(x, 1, 4), x)
    4*SingularityFunction(x, 1, 3) + 5*SingularityFunction(x, 1, 4)
    >>> diff(SingularityFunction(x, 4, 0), x, 2)
    SingularityFunction(x, 4, -2)
    >>> SingularityFunction(x, 4, 5).rewrite(Piecewise)
    Piecewise(((x - 4)**5, x - 4 > 0), (0, True))
    >>> expr = SingularityFunction(x, a, n)
    >>> y = Symbol('y', positive=True)
    >>> n = Symbol('n', nonnegative=True)
    >>> expr.subs({x: y, a: -10, n: n})
    (y + 10)**n

    The methods ``rewrite(DiracDelta)``, ``rewrite(Heaviside)`` and ``rewrite('HeavisideDiracDelta')``
    returns the same output. One can use any of these methods according to their choice.

    >>> expr = SingularityFunction(x, 4, 5) + SingularityFunction(x, -3, -1) - SingularityFunction(x, 0, -2)
    >>> expr.rewrite(Heaviside)
    (x - 4)**5*Heaviside(x - 4) + DiracDelta(x + 3) - DiracDelta(x, 1)
    >>> expr.rewrite(DiracDelta)
    (x - 4)**5*Heaviside(x - 4) + DiracDelta(x + 3) - DiracDelta(x, 1)
    >>> expr.rewrite('HeavisideDiracDelta')
    (x - 4)**5*Heaviside(x - 4) + DiracDelta(x + 3) - DiracDelta(x, 1)

    See Also
    ========

    DiracDelta, Heaviside

    Reference
    =========

    .. [1] https://en.wikipedia.org/wiki/Singularity_function
    """

    is_real = True

    def fdiff(self, argindex=1):
        '''
        Returns the first derivative of a DiracDelta Function.

        The difference between ``diff()`` and ``fdiff()`` is:-
        ``diff()`` is the user-level function and ``fdiff()`` is an object method.
        ``fdiff()`` is just a convenience method available in the ``Function`` class.
        It returns the derivative of the function without considering the chain rule.
        ``diff(function, x)`` calls ``Function._eval_derivative`` which in turn calls
        ``fdiff()`` internally to compute the derivative of the function.

        '''
        if argindex == 1:
            x = sympify(self.args[0])
            a = sympify(self.args[1])
            n = sympify(self.args[2])
            if n == 0 or n == -1:
                return self.func(x, a, n-1)
            elif n.is_positive:
                return n*self.func(x, a, n-1)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def eval(cls, variable, offset, exponent):
        """
        Returns a simplified form or a value of Singularity Function depending on the
        argument passed by the object.

        The ``eval()`` method is automatically called when the ``SingularityFunction`` class
        is about to be instantiated and it returns either some simplified instance
        or the unevaluated instance depending on the argument passed. In other words,
        ``eval()`` method is not needed to be called explicitly, it is being called
        and evaluated once the object is called.

        Examples
        ========
        >>> from ... import SingularityFunction, Symbol, nan
        >>> from ...abc import x, a, n
        >>> SingularityFunction(x, a, n)
        SingularityFunction(x, a, n)
        >>> SingularityFunction(5, 3, 2)
        4
        >>> SingularityFunction(x, a, nan)
        nan
        >>> SingularityFunction(x, 3, 0).subs(x, 3)
        1
        >>> SingularityFunction(x, a, n).eval(3, 5, 1)
        0
        >>> SingularityFunction(x, a, n).eval(4, 1, 5)
        243
        >>> x = Symbol('x', positive = True)
        >>> a = Symbol('a', negative = True)
        >>> n = Symbol('n', nonnegative = True)
        >>> SingularityFunction(x, a, n)
        (-a + x)**n
        >>> x = Symbol('x', negative = True)
        >>> a = Symbol('a', positive = True)
        >>> SingularityFunction(x, a, n)
        0

        """

        x = sympify(variable)
        a = sympify(offset)
        n = sympify(exponent)
        shift = (x - a)

        if fuzzy_not(im(shift).is_zero):
            raise ValueError("Singularity Functions are defined only for Real Numbers.")
        if fuzzy_not(im(n).is_zero):
            raise ValueError("Singularity Functions are not defined for imaginary exponents.")
        if shift is S.NaN or n is S.NaN:
            return S.NaN
        if (n + 2).is_negative:
            raise ValueError("Singularity Functions are not defined for exponents less than -2.")
        if shift.is_negative:
            return S.Zero
        if n.is_nonnegative and shift.is_nonnegative:
            return (x - a)**n
        if n == -1 or n == -2:
            if shift.is_negative or shift.is_positive:
                return S.Zero
            if shift.is_zero:
                return S.Infinity

    def _eval_rewrite_as_Piecewise(self, *args):
        '''
        Converts a Singularity Function expression into its Piecewise form.

        '''
        x = self.args[0]
        a = self.args[1]
        n = sympify(self.args[2])

        if n == -1 or n == -2:
            return Piecewise((oo, Eq((x - a), 0)), (0, True))
        elif n.is_nonnegative:
            return Piecewise(((x - a)**n, (x - a) > 0), (0, True))

    def _eval_rewrite_as_Heaviside(self, *args):
        '''
        Rewrites a Singularity Function expression using Heavisides and DiracDeltas.

        '''
        x = self.args[0]
        a = self.args[1]
        n = sympify(self.args[2])

        if n == -2:
            return diff(Heaviside(x - a), x.free_symbols.pop(), 2)
        if n == -1:
            return diff(Heaviside(x - a), x.free_symbols.pop(), 1)
        if n.is_nonnegative:
            return (x - a)**n*Heaviside(x - a)

    _eval_rewrite_as_DiracDelta = _eval_rewrite_as_Heaviside
    _eval_rewrite_as_HeavisideDiracDelta = _eval_rewrite_as_Heaviside
