r"""
    This file contains a class to represent an Arnoux-Rauzy sequence
    a regular substitutive Arnoux-Rauzy sequence.
"""
#import sage.all_cmdline - if I want to put sage -python b
class ArnouxRauzySubstitutiveSequence:
    def __init__(self, d, preperiod, period):
        self._preperiod = preperiod
        self._period = period
        self._directive = [preperiod, period]
        self._d = d

    def __repr__(self):
        return ("An Arnoux-Rauzy sequence with the directive sequence {}.".format(self._directive))

    def matrix_A(self, a_i):
        r'''
        Compute an auxiliary matrix ``A_{h+i}`` of an Arnoux-Rauzy sequence with
        the directive sequence ``[a_1,...,a_h][a_{h+1},...,a_{h+p}]^omega``.
        The matrix A of dimension d times d is defined as 
        ``A(a_i) = Matrix([[a_i,a_i,...,a_i,1],[1,0,...,0],...,[0,0,...,1,0]])``.
        
        EXAMPLES::

            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: w = ArnouxRauzySubstitutiveSequence(3,[],[1])
            sage: w.matrix_A(1)
            [1 1 1]
            [1 0 0]
            [0 1 0]

        :: 

            sage: w = ArnouxRauzySubstitutiveSequence(4,[],[3])
            sage: w.matrix_A(3)
            [3 3 3 1]
            [1 0 0 0]
            [0 1 0 0]
            [0 0 1 0]
        '''
        from sage.matrix.constructor import Matrix
        from sage.matrix.constructor import vector
        from sage.rings.integer_ring import ZZ
        d = self._d
        Id = Matrix.identity(d)
        A = Matrix(ZZ, d)
        for i in range(d):
            A[i,:] = Id.row(i-1)
        for j in range(d-1):
            A[0,j] = a_i
        return A
        

    def matrices_M(self):
        r'''

        Computes a list of matrices ``M^i`` defined for every i=0,...,p-1
        as M^i = A_{h+1} A_{h+2} ... A_{h+i}

        for an AR sequence with the directive sequence 
        ``[a_1,...,a_h][a_{h+1},...,a_{h+p}]^omega``.

        EXAMPLES::

            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: w = ArnouxRauzySubstitutiveSequence(3,[],[2,1,1])
            sage: w.matrices_M()
            [
            [1 0 0]  [2 2 1]  [4 3 2]  [7 6 4]
            [0 1 0]  [1 0 0]  [1 1 1]  [2 2 1]
            [0 0 1], [0 1 0], [1 0 0], [1 1 1]
            ]
            sage: w = ArnouxRauzySubstitutiveSequence(4,[],[1,3])
            sage: w.matrices_M()
            [
            [1 0 0 0]  [1 1 1 1]  [4 4 4 1]
            [0 1 0 0]  [1 0 0 0]  [3 3 3 1]
            [0 0 1 0]  [0 1 0 0]  [1 0 0 0]
            [0 0 0 1], [0 0 1 0], [0 1 0 0]
            ]

        '''
        from sage.matrix.constructor import Matrix
        d = self._d
        M = Matrix.identity(d)
        matrices = []
        matrices.append(M)
        for a_i in self._period:
            M *= self.matrix_A(a_i)
            matrices.append(M)
        return matrices 

    def eigenvector_x(self):
        r'''
        Computes the left eigenvector of the matrix
        ``M`` defined as ``M = matrix_A(p)`` for an AR sequence with
        the directive sequence ``[a_1,...,a_h][a_{h+1},...,a_{h+p}]^omega``.
        The output is given as a function of ``Lambda``
        - the dominant eigenvalue of the matrix ``M``.

        EXAMPLES::

            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: w = ArnouxRauzySubstitutiveSequence(3,[],[2,1,1])
            sage: w.eigenvector_x()
            (1, -Lambda^2 + 10*Lambda - 5, 2*Lambda^2 - 19*Lambda + 3)
            sage: w.eigenvector_x().n()
            (1.00000000000000, 0.893289196304499, 0.584543980843328)

        ::

            sage: w = ArnouxRauzySubstitutiveSequence(4,[],[1,3])
            sage: w.eigenvector_x()
            (1, -1/9*Lambda^3 + 8/9*Lambda^2 - 13/9, 1/3*Lambda^3 - 8/3*Lambda^2 + Lambda + 1/3, 4/9*Lambda^3 - 29/9*Lambda^2 - 4/3*Lambda + 4/9)
            sage: w.eigenvector_x().n()
            (1.00000000000000, 0.917081221812298, 0.884198166173816, 0.251076658573389)

        '''
        from sage.matrix.constructor import Matrix
        from sage.matrix.constructor import vector
        from sage.rings.number_field.number_field import NumberField
        from sage.rings.real_mpfr import RR
        M = self.matrices_M()[-1]
        char_poly = M.characteristic_polynomial()
        eigenvalues = M.eigenvalues()
        eigenvalues.sort(key=abs)
        K = NumberField(char_poly, "Lambda", embedding=RR(eigenvalues[-1]))
        Lambda = K.gen()
        k = (M.transpose() - Lambda).right_kernel_matrix()
        x = k[0]
        return x

    def matrix_of_y(self):
        r'''
        Compute an auxiliary matrix Y of an Arnoux-Rauzy sequence with
        the directive sequence ``[a_1,...,a_h][a_{h+1},...,a_{h+p}]^omega``.
        The ``i``-th row of the matrix ``Y`` is defined as 
        ``Y[i] = x*M^{i}`` where ``M^{i} = self.matrix_M()[i]``.


        EXAMPLES::


            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: w = ArnouxRauzySubstitutiveSequence(3,[3],[3,1,1,1])
            sage: w.matrix_of_y()
            [                               1  -1/4*Lambda^2 + 6*Lambda - 11/4   1/2*Lambda^2 - 23/2*Lambda - 4]
            [  -1/4*Lambda^2 + 6*Lambda + 1/4   1/2*Lambda^2 - 23/2*Lambda - 1                                1]
            [1/4*Lambda^2 - 11/2*Lambda - 3/4   -1/4*Lambda^2 + 6*Lambda + 5/4   -1/4*Lambda^2 + 6*Lambda + 1/4]
            [                1/2*Lambda + 1/2                 1/2*Lambda - 1/2 1/4*Lambda^2 - 11/2*Lambda - 3/4]
            sage: w.matrix_of_y().n()
            [ 1.00000000000000 0.835975919081305 0.521379706804598]
            [ 3.83597591908131  3.52137970680460  1.00000000000000]
            [ 7.35735562588590  4.83597591908130  3.83597591908131]
            [ 12.1933315449672  11.1933315449672  7.35735562588590]

        '''
        from sage.matrix.constructor import Matrix
        x = self.eigenvector_x()
        p = len(self._period)
        matrices = self.matrices_M()
        Y_rows = []
        for index in range(p):
            row = x*matrices[index]
            Y_rows.append(row)
        return Matrix(Y_rows)

    def betas(self):
        r'''
        Auxiliary function to produce the list of beta_i.

        EXAMPLES::

            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: w = ArnouxRauzySubstitutiveSequence(3,[3],[3,1,1,1])
            sage: w.betas()
            [-1/8*Lambda^2 + 3*Lambda + 1/8,
            -1/4*Lambda^2 + 6*Lambda + 1/4,
            -1/8*Lambda^2 + 3*Lambda + 1/8,
            -3/8*Lambda^2 + 35/4*Lambda + 17/8]

        ::

            sage: w = ArnouxRauzySubstitutiveSequence(3,[],[1])
            sage: w.betas()
            [Lambda]
        '''
        from sage.matrix.constructor import Matrix
        d = self._d
        Y = self.matrix_of_y()
        betas = []
        for row in Y:
            betas.append(row[0]/row[d-1])
        return betas

    def asymptotic_critical_exponent(self):
        r'''
        Compute the asymptotic critical exponent (ACE) of an Arnoux-Rauzy
        sequence with an eventually periodic directive sequence.

        EXAMPLES::

            sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
            sage: word = ArnouxRauzySubstitutiveSequence(3,[],[1])
            sage: ACE = word.asymptotic_critical_exponent()
            sage: ACE
            1/2*Lambda^2 + 3/2
            sage: ACE.n()
            3.19148788395312

        ::

            sage: word = ArnouxRauzySubstitutiveSequence(3,[],[2,1,1])
            sage: ACE = word.asymptotic_critical_exponent()
            sage: ACE
            1/2*Lambda^2 - 9/2*Lambda + 5/2
            sage: ACE.n()
            4.23891658857391

        ::

            sage: word = ArnouxRauzySubstitutiveSequence(3,[3],[3,1,1,1])
            sage: ACE = word.asymptotic_critical_exponent()
            sage: ACE
            1/8*Lambda^2 - 11/4*Lambda + 9/8
            sage: ACE.n()
            5.17867781294295


        '''
        from sage.rings.integer import Integer
        from sage.misc.misc_c import prod
        d = self._d
        a = self._period
        p = len(self._period)
        betas = self.betas()
        limits = []
        for i in range(p):
            nominator = 0
            for j in range(2, d+1):
                nominator += ((d-j)*a[(i-j+1) % p] + 1)*prod([betas[(i - k + 1) % p] for k in range(j,d)])
            denominator = prod([betas[(i - k + 1) % p] for k in range(1,d)])
            L = a[i] + Integer(1)/(d-1)*nominator/denominator
            limits.append(L)
        asymptotic_critical_exponent = Integer(d)/(d-1) + max(limits)
        return asymptotic_critical_exponent
