from ..simplify import simplify as simp, trigsimp as tsimp
from ..core.decorators import call_highest_priority, _sympifyit
from ..core.assumptions import StdFactKB
from .. import factor as fctr, diff as df, Integral
from ..core import S, Add, Mul, count_ops
from ..core.expr import Expr


class BasisDependent(Expr):
    """
    Super class containing functionality common to vectors and
    dyadics.
    Named so because the representation of these quantities in
    sympy.vector is dependent on the basis they are expressed in.
    """

    @call_highest_priority('__radd__')
    def __add__(self, other):
        return self._add_func(self, other)

    @call_highest_priority('__add__')
    def __radd__(self, other):
        return self._add_func(other, self)

    @call_highest_priority('__rsub__')
    def __sub__(self, other):
        return self._add_func(self, -other)

    @call_highest_priority('__sub__')
    def __rsub__(self, other):
        return self._add_func(other, -self)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rmul__')
    def __mul__(self, other):
        return self._mul_func(self, other)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__mul__')
    def __rmul__(self, other):
        return self._mul_func(other, self)

    def __neg__(self):
        return self._mul_func(S(-1), self)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rdiv__')
    def __div__(self, other):
        return self._div_helper(other)

    @call_highest_priority('__div__')
    def __rdiv__(self, other):
        return TypeError("Invalid divisor for division")

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def evalf(self, prec=None, **options):
        """
        Implements the SymPy evalf routine for this quantity.

        evalf's documentation
        =====================

        """
        vec = self.zero
        for k, v in self.components.items():
            vec += v.evalf(prec, **options) * k
        return vec

    evalf.__doc__ += Expr.evalf.__doc__

    n = evalf

    def simplify(self, ratio=1.7, measure=count_ops):
        """
        Implements the SymPy simplify routine for this quantity.

        simplify's documentation
        ========================

        """
        simp_components = [simp(v, ratio, measure) * k for
                           k, v in self.components.items()]
        return self._add_func(*simp_components)

    simplify.__doc__ += simp.__doc__

    def trigsimp(self, **opts):
        """
        Implements the SymPy trigsimp routine, for this quantity.

        trigsimp's documentation
        ========================

        """
        trig_components = [tsimp(v, **opts) * k for
                           k, v in self.components.items()]
        return self._add_func(*trig_components)

    trigsimp.__doc__ += tsimp.__doc__

    def _eval_simplify(self, ratio, measure):
        return self.simplify(ratio, measure)

    def _eval_trigsimp(self, **opts):
        return self.trigsimp(**opts)

    def _eval_derivative(self, wrt):
        return self.diff(wrt)

    def _eval_Integral(self, *symbols, **assumptions):
        integral_components = [Integral(v, *symbols, **assumptions) * k
                               for k, v in self.components.items()]
        return self._add_func(*integral_components)

    def _eval_diff(self, *args, **kwargs):
        return self.diff(*args, **kwargs)

    def as_numer_denom(self):
        """
        Returns the expression as a tuple wrt the following
        transformation -

        expression -> a/b -> a, b

        """
        return self, 1

    def factor(self, *args, **kwargs):
        """
        Implements the SymPy factor routine, on the scalar parts
        of a basis-dependent expression.

        factor's documentation
        ========================

        """
        fctr_components = [fctr(v, *args, **kwargs) * k for
                           k, v in self.components.items()]
        return self._add_func(*fctr_components)

    factor.__doc__ += fctr.__doc__

    def as_coeff_Mul(self, rational=False):
        """Efficiently extract the coefficient of a product. """
        return (S(1), self)

    def as_coeff_add(self, *deps):
        """Efficiently extract the coefficient of a summation. """
        l = [x * self.components[x] for x in self.components]
        return 0, tuple(l)

    def diff(self, *args, **kwargs):
        """
        Implements the SymPy diff routine, for vectors.

        diff's documentation
        ========================

        """
        for x in args:
            if isinstance(x, BasisDependent):
                raise TypeError("Invalid arg for differentiation")
        diff_components = [df(v, *args, **kwargs) * k for
                           k, v in self.components.items()]
        return self._add_func(*diff_components)

    diff.__doc__ += df.__doc__

    def doit(self, **hints):
        """Calls .doit() on each term in the Dyadic"""
        doit_components = [self.components[x].doit(**hints) * x
                           for x in self.components]
        return self._add_func(*doit_components)


class BasisDependentAdd(BasisDependent, Add):
    """
    Denotes sum of basis dependent quantities such that they cannot
    be expressed as base or Mul instances.
    """

    def __new__(cls, *args, **options):
        components = {}

        # Check each arg and simultaneously learn the components
        for i, arg in enumerate(args):
            if not isinstance(arg, cls._expr_type):
                if isinstance(arg, Mul):
                    arg = cls._mul_func(*(arg.args))
                elif isinstance(arg, Add):
                    arg = cls._add_func(*(arg.args))
                else:
                    raise TypeError(str(arg) +
                                    " cannot be interpreted correctly")
            # If argument is zero, ignore
            if arg == cls.zero:
                continue
            # Else, update components accordingly
            for x in arg.components:
                components[x] = components.get(x, 0) + arg.components[x]

        temp = list(components.keys())
        for x in temp:
            if components[x] == 0:
                del components[x]

        # Handle case of zero vector
        if len(components) == 0:
            return cls.zero

        # Build object
        newargs = [x * components[x] for x in components]
        obj = super(BasisDependentAdd, cls).__new__(cls,
                                                    *newargs, **options)
        if isinstance(obj, Mul):
            return cls._mul_func(*obj.args)
        assumptions = {'commutative': True}
        obj._assumptions = StdFactKB(assumptions)
        obj._components = components
        obj._sys = (list(components.keys()))[0]._sys

        return obj

    __init__ = Add.__init__


class BasisDependentMul(BasisDependent, Mul):
    """
    Denotes product of base- basis dependent quantity with a scalar.
    """

    def __new__(cls, *args, **options):
        count = 0
        measure_number = S(1)
        zeroflag = False

        # Determine the component and check arguments
        # Also keep a count to ensure two vectors aren't
        # being multiplied
        for arg in args:
            if isinstance(arg, cls._zero_func):
                count += 1
                zeroflag = True
            elif arg == S(0):
                zeroflag = True
            elif isinstance(arg, (cls._base_func, cls._mul_func)):
                count += 1
                expr = arg._base_instance
                measure_number *= arg._measure_number
            elif isinstance(arg, cls._add_func):
                count += 1
                expr = arg
            else:
                measure_number *= arg
        # Make sure incompatible types weren't multiplied
        if count > 1:
            raise ValueError("Invalid multiplication")
        elif count == 0:
            return Mul(*args, **options)
        # Handle zero vector case
        if zeroflag:
            return cls.zero

        # If one of the args was a VectorAdd, return an
        # appropriate VectorAdd instance
        if isinstance(expr, cls._add_func):
            newargs = [cls._mul_func(measure_number, x) for
                       x in expr.args]
            return cls._add_func(*newargs)

        obj = super(BasisDependentMul, cls).__new__(cls, measure_number,
                                                    expr._base_instance,
                                                    **options)
        if isinstance(obj, Add):
            return cls._add_func(*obj.args)
        obj._base_instance = expr._base_instance
        obj._measure_number = measure_number
        assumptions = {'commutative': True}
        obj._assumptions = StdFactKB(assumptions)
        obj._components = {expr._base_instance: measure_number}
        obj._sys = expr._base_instance._sys

        return obj

    __init__ = Mul.__init__

    def __str__(self, printer=None):
        measure_str = self._measure_number.__str__()
        if ('(' in measure_str or '-' in measure_str or
                '+' in measure_str):
            measure_str = '(' + measure_str + ')'
        return measure_str + '*' + self._base_instance.__str__(printer)

    __repr__ = __str__
    _sympystr = __str__


class BasisDependentZero(BasisDependent):
    """
    Class to denote a zero basis dependent instance.
    """
    components = {}

    def __new__(cls):
        obj = super(BasisDependentZero, cls).__new__(cls)
        # Pre-compute a specific hash value for the zero vector
        # Use the same one always
        obj._hash = tuple([S(0), cls]).__hash__()
        return obj

    def __hash__(self):
        return self._hash

    @call_highest_priority('__req__')
    def __eq__(self, other):
        return isinstance(other, self._zero_func)

    __req__ = __eq__

    @call_highest_priority('__radd__')
    def __add__(self, other):
        if isinstance(other, self._expr_type):
            return other
        else:
            raise TypeError("Invalid argument types for addition")

    @call_highest_priority('__add__')
    def __radd__(self, other):
        if isinstance(other, self._expr_type):
            return other
        else:
            raise TypeError("Invalid argument types for addition")

    @call_highest_priority('__rsub__')
    def __sub__(self, other):
        if isinstance(other, self._expr_type):
            return -other
        else:
            raise TypeError("Invalid argument types for subtraction")

    @call_highest_priority('__sub__')
    def __rsub__(self, other):
        if isinstance(other, self._expr_type):
            return other
        else:
            raise TypeError("Invalid argument types for subtraction")

    def __neg__(self):
        return self

    def normalize(self):
        """
        Returns the normalized version of this vector.
        """
        return self

    def __str__(self, printer=None):
        return '0'

    __repr__ = __str__
    _sympystr = __str__
