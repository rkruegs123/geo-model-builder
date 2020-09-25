(declare-points A B C H G I M J)

;; Acute triangle ABC has orthocenter H
(assert (triangle A B C))
(assert (acutes A B C))

(assert (orthocenter H A B C))

;; G is the point s.t. ABGH is a parallelogram
(assert (para A B G H))
(assert (para A H B G))

;; I is the point on the line GH s.t. AC bisects HI
(assert (coll I G H))
(assert (coll M A C))
(assert (midp M H I))

;; AC intersects the circumcircle of triangle GCI at C and J
(assert (coll A C J))
(assert (cycl G C I J))

;; Prove that IJ = AH
(prove (cong I J A H))
