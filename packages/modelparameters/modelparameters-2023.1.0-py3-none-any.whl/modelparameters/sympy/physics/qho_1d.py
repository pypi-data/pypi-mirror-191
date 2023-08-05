from __future__ import print_function, division

from ..core import S, pi, Rational
from ..functions import hermite, sqrt, exp, factorial, Abs
from .quantum.constants import hbar


def psi_n(n, x, m, omega):
    """
    Returns the wavefunction psi_{n} for the One-dimensional harmonic oscillator.

    ``n``
        the "nodal" quantum number.  Corresponds to the number of nodes in the
        wavefunction.  n >= 0
    ``x``
        x coordinate
    ``m``
        mass of the particle
    ``omega``
        angular frequency of the oscillator

    Examples
    ========

    >>> from .qho_1d import psi_n
    >>> from .. import var
    >>> var("x m omega")
    (x, m, omega)
    >>> psi_n(0, x, m, omega)
    (m*omega)**(1/4)*exp(-m*omega*x**2/(2*hbar))/(hbar**(1/4)*pi**(1/4))

    """

    # sympify arguments
    n, x, m, omega = map(S, [n, x, m, omega])
    nu = m * omega / hbar
    # normalization coefficient
    C = (nu/pi)**(S(1)/4) * sqrt(1/(2**n*factorial(n)))

    return C * exp(-nu* x**2 /2) * hermite(n, sqrt(nu)*x)


def E_n(n, omega):
    """
    Returns the Energy of the One-dimensional harmonic oscillator

    ``n``
        the "nodal" quantum number
    ``omega``
        the harmonic oscillator angular frequency

    The unit of the returned value matches the unit of hw, since the energy is
    calculated as:

        E_n = hbar * omega*(n + 1/2)

    Examples
    ========

    >>> from .qho_1d import E_n
    >>> from .. import var
    >>> var("x omega")
    (x, omega)
    >>> E_n(x, omega)
    hbar*omega*(x + 1/2)
    """

    return hbar * omega*(n + Rational(1, 2))


def coherent_state(n, alpha):
    """
    Returns <n|alpha> for the coherent states of 1D harmonic oscillator.
    See http://en.wikipedia.org/wiki/Coherent_states

    ``n``
        the "nodal" quantum number
    ``alpha``
        the eigen value of annihilation operator
    """

    return exp(- Abs(alpha)**2/2)*(alpha**n)/sqrt(factorial(n))
