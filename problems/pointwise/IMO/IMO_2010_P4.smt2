(declare-points A B C P K L M O S)

;; P is a point inside the triangle ABC
(assert (triangle A B C))
(assert (insidePolygon P A B C))

;; AP, BP, and CP intersect (ABC) at points K, L, and M, respectively
(assert (coll K A P))
(assert (cycl K A B C))

(assert (coll L B P))
(assert (cycl L A B C))

(assert (coll M C P))
(assert (cycl M A B C))

(assert (circumcenter O A B C))

;; The tangent to (ABC) at C intersects AB at S
(assert (perp C S C O))
(assert (coll S A B))

;; Suppose that SC = SP
(assert (cong S C S P))

;; Prove that MK = ML
(prove (cong M K M L))
