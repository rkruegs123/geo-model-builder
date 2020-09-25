(declare-points A B C I O D E F G1)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (circumcenter O A B C))

(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))
(assert (centroid G1 D E F))

(prove (coll G1 I O))