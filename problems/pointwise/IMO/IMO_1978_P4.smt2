(declare-points A B C T P Q O M)

;; In triangle ABC, AB = AC
(assert (triangle A B C))
(assert (cong A B A C))

;; A circle is tangent internally to the circumcircle of triangle ABC...
(assert (cycl A B C T))

;; ... and also to sides AB, AC at P, Q, respectively
(assert (onSeg P A B))
(assert (onSeg Q A C))

(assert (circumcenter O P Q T))
(assert (perp O P A B))
(assert (perp O Q A C))

;; Prove that the midpoint of PQ is the center of the incircle of triangle ABC
(assert (midp M P Q))
(prove (incenter M A B C))
