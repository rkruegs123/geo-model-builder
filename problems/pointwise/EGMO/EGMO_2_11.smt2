(declare-points A B C P Oabp Oacp M)

(assert (triangle A B C))
(assert (insidePolygon P A B C))

;; Suppose BC is tangent to the circumcircles of triangles ABP and ACP
(assert (circumcenter Oabp A B P))
(assert (circumcenter Oacp A C P))
(assert (perp Oabp B B C))
(assert (perp Oacp C B C))

;; Prove that ray AP bisects BC
(assert (interLL M A P B C))
(assert (onRay M A P))
(prove (cong M B M C))