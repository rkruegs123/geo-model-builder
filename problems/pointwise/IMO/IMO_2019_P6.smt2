(declare-points A B C I D E F R P Q T)

(assert (triangle A B C))
(assert (acutes A B C))
(assert (not (cong A B A C)))

(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I A C))
(assert (foot F I A B))

(assert (perp R D E F))
(assert (cycl R D E F))

(assert (coll P A R))
(assert (cycl P R E F))

(assert (cycl Q P C E))
(assert (cycl Q P B F))

(assert (interLL T D I P Q))
(prove (perp A I A T))
