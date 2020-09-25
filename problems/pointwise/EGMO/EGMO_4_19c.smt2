(declare-points A B C P P1)

(assert (triangle A B C))
(assert (insidePolygon P A B C))

(assert (eqangle A C C P P1 C C B))
(assert (eqangle C B B P P1 B B A))
(prove (eqangle B A A P P1 A A C))