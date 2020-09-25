(declare-points A B C I)

(assert (triangle A B C))
(assert (ibisector I A B C))
(assert (ibisector I B C A))

(prove (incenter I A B C))