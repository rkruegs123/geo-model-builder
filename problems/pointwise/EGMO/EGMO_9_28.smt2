;; (declare-points A B C H E F)
(declare-points A B C H E F)

;; ABC is an acute scalene triangle
(assert (triangle A B C))
(assert (acutes A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong A C B C)))

;; H is a point inside ABC s.t. AH is perp. to BC
(assert (insidePolygon H A B C))
(assert (perp A H B C))

;; Rays BH and CH meet AC and AB at E, F
(assert (interLL E B H A C))
(assert (onRay E B H))
(assert (onSeg E A C))

(assert (interLL F C H A B))
(assert (onRay F C H))
(assert (onSeg F A B))

;; BFEC is cyclic
(assert (cycl B F E C))

(prove (orthocenter H A B C))