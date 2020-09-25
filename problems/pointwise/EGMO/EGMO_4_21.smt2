(declare-points A B C P Q)

(assert (triangle A B C))
(assert (insidePolygon P A B C))

(assert (isogonal Q P A B C))
(prove (isogonal P Q A B C))