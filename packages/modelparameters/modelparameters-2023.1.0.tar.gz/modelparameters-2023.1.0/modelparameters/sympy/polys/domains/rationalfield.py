"""Implementation of :class:`RationalField` class. """

from __future__ import print_function, division

from .field import Field
from .simpledomain import SimpleDomain
from .characteristiczero import CharacteristicZero

from ...utilities import public

@public
class RationalField(Field, CharacteristicZero, SimpleDomain):
    """General class for rational fields. """

    rep = 'QQ'

    is_RationalField = is_QQ = True
    is_Numerical = True

    has_assoc_Ring = True
    has_assoc_Field = True

    def algebraic_field(self, *extension):
        r"""Returns an algebraic field, i.e. `\mathbb{Q}(\alpha, \ldots)`. """
        from ..domains import AlgebraicField
        return AlgebraicField(self, *extension)

    def from_AlgebraicField(K1, a, K0):
        """Convert a ``ANP`` object to ``dtype``. """
        if a.is_ground:
            return K1.convert(a.LC(), K0.dom)
