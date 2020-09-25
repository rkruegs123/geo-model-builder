;; (a) Prove that I,G, N are collinear
;; (b) prove that NG = 2*GI

(declare-points A B C I G Ia Ib Ic Ta Tb Tc N)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (centroid G A B C))

(assert (excenter Ia A B C))
(assert (excenter Ib B A C))
(assert (excenter Ic C A B))

(assert (foot Ta Ia B C))
(assert (foot Tb Ib C A))
(assert (foot Tc Ic A B))

(assert (interLL N A Ta B Tb))
;; Note: The below is unnecessary
(assert (coll N C Tc))

(prove (coll I G N))