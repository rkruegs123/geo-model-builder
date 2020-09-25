(declare-points A B C D L M Q P N H Ohmn)

(assert (triangle A B C))

;; The interior angle bisector of <A intersects BC and (ABC) at D and L, respectively
(assert (ibisector D B A C))
(assert (onSeg D B C))

(assert (ibisector L B A C))
(assert (cycl L A B C))

;; M is the midpoint of BC
(assert (midp M B C))

;; The circumcircle of ADM intersects sides AB and AC again at Q and P, respectively
(assert (cycl Q A D M))
(assert (onSeg Q A B))

(assert (cycl P A D M))
(assert (onSeg P A C))

;; N is the midpoint of PQ
(assert (midp N P Q))

;; H is the foot of the perpendicular from L to ND
(assert (foot H L N D))

;; Prove that ML is tangent to (HMN)
(assert (circumcenter Ohmn H M N))
(prove (perp Ohmn M M L))