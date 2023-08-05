This package was created to demonstrate results in the paper
of Lubomira Dvorakova and Jana Lepsova with the name
Critical exponent of Arnoux-Rauzy sequences.

The algorithm computes the asymptotical critical exponent
of regular d-ary Arnoux-Rauzy sequence for any dimension d.

In the examples we compute the asymptotical critical exponent (ACE)
of the Tribonacci word (d = 3).
==================

EXAMPLES:

    sage: from colored_arnoux_rauzy_sequences.ARsequence import ArnouxRauzySubstitutiveSequence
    sage: word = ArnouxRauzySubstitutiveSequence(3,[],[1])
    sage: ACE = word.asymptotic_critical_exponent()
    sage: ACE
    1/2*Lambda^2 + 3/2
    sage: ACE.n()                                                                                
    3.19148788395312

==================

``colored_arnoux_rauzy_sequences`` package 

