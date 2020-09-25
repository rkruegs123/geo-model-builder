(declare-points A B C Ib Ic I)

(assert (triangle A B C))
(assert (excenter Ib B C A))
(assert (excenter Ic C A B))
(assert (incenter I A B C))

(prove (perp I A A Ib))
(prove (perp I A A Ic))
