from ..core import Rational
from ..core.compatibility import range
from .cartan_type import Standard_Cartan
from ..matrices import Matrix


class TypeF(Standard_Cartan):

    def __new__(cls, n):
        if n != 4:
            raise ValueError("n should be 4")
        return Standard_Cartan.__new__(cls, "F", 4)

    def dimension(self):
        """Dimension of the vector space V underlying the Lie algebra

        Examples
        ========

        >>> from .cartan_type import CartanType
        >>> c = CartanType("F4")
        >>> c.dimension()
        4
        """

        return 4


    def basic_root(self, i, j):
        """Generate roots with 1 in ith position and -1 in jth postion

        """

        n = self.n
        root = [0]*n
        root[i] = 1
        root[j] = -1
        return root

    def simple_root(self, i):
        """The ith simple root of F_4

        Every lie algebra has a unique root system.
        Given a root system Q, there is a subset of the
        roots such that an element of Q is called a
        simple root if it cannot be written as the sum
        of two elements in Q.  If we let D denote the
        set of simple roots, then it is clear that every
        element of Q can be written as a linear combination
        of elements of D with all coefficients non-negative.

        Examples
        ========

        >>> from .cartan_type import CartanType
        >>> c = CartanType("F4")
        >>> c.simple_root(3)
        [0, 0, 0, 1]

        """

        if i < 3:
            return basic_root(i-1, i)
        if i == 3:
            root = [0]*4
            root[3] = 1
            return root
        if i == 4:
            root = [Rational(-1, 2)]*4
            return root

    def positive_roots(self):
        """Generate all the positive roots of A_n

        This is half of all of the roots of F_4; by multiplying all the
        positive roots by -1 we get the negative roots.

        Examples
        ========

        >>> from .cartan_type import CartanType
        >>> c = CartanType("A3")
        >>> c.positive_roots()
        {1: [1, -1, 0, 0], 2: [1, 0, -1, 0], 3: [1, 0, 0, -1], 4: [0, 1, -1, 0],
                5: [0, 1, 0, -1], 6: [0, 0, 1, -1]}

        """

        n = self.n
        posroots = {}
        k = 0
        for i in range(0, n-1):
            for j in range(i+1, n):
               k += 1
               posroots[k] = self.basic_root(i, j)
               k += 1
               root = self.basic_root(i, j)
               root[j] = 1
               posroots[k] = root

        for i in range(0, n):
            k += 1
            root = [0]*n
            root[i] = 1
            posroots[k] = root

        k += 1
        root = [Rational(1, 2)]*n
        posroots[k] = root
        for i in range(1, 4):
            k += 1
            root = [Rational(1, 2)]*n
            root[i] = Rational(-1, 2)
            posroots[k] = root

        posroots[k+1] = [Rational(1, 2), Rational(1, 2), Rational(-1, 2), Rational(-1, 2)]
        posroots[k+2] = [Rational(1, 2), Rational(-1, 2), Rational(1, 2), Rational(-1, 2)]
        posroots[k+3] = [Rational(1, 2), Rational(-1, 2), Rational(-1, 2), Rational(1, 2)]
        posroots[k+4] = [Rational(1, 2), Rational(-1, 2), Rational(-1, 2), Rational(-1, 2)]

        return posroots


    def roots(self):
        """
        Returns the total number of roots for F_4
        """
        return 48

    def cartan_matrix(self):
        """The Cartan matrix for F_4

        The Cartan matrix matrix for a Lie algebra is
        generated by assigning an ordering to the simple
        roots, (alpha[1], ...., alpha[l]).  Then the ijth
        entry of the Cartan matrix is (<alpha[i],alpha[j]>).

        Examples
        ========

        >>> from .cartan_type import CartanType
        >>> c = CartanType('A4')
        >>> c.cartan_matrix()
        Matrix([
        [ 2, -1,  0,  0],
        [-1,  2, -1,  0],
        [ 0, -1,  2, -1],
        [ 0,  0, -1,  2]])
        """

        m = Matrix( 4, 4, [2, -1, 0, 0, -1, 2, -2, 0, 0,
            -1, 2, -1, 0, 0, -1, 2])
        return m

    def basis(self):
        """
        Returns the number of independent generators of F_4
        """
        return 52

    def dynkin_diagram(self):
        diag = "0---0=>=0---0\n"
        diag += "   ".join(str(i) for i in range(1, 5))
        return diag
