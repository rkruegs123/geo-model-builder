(declare-points A B C Q I D E F P)

(assert (triangle A B C))

(assert (perp A B Q B))
(assert (perp A C Q C))

(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))

(assert (onRay P Q I))
(assert (coll P E F))

(prove (perp D P E F))