(declare-points A B C A1 A2 B1 B2 C1 C2 Aux)

;; ABC is an equilateral triangle
(assert (triangle A B C))
(assert (cong A B A C))
(assert (cong A B B C))

;; A1 and A2 are on BC
(assert (onSeg A1 B C))
(assert (onSeg A2 A1 C))

;; B1 and B2 are on CA
(assert (onSeg B1 C A))
(assert (onSeg B2 B1 A))

;; C1 and C2 are on AB
(assert (onSeg C1 A B))
(assert (onSeg C2 C1 B))

;; The side lengths of the convex hexagon are equal
(assert (cong A1 A2 A2 B1))
(assert (cong A2 B1 B1 B2))
(assert (cong B1 B2 B2 C1))
(assert (cong B2 C1 C1 C2))
(assert (cong C1 C2 C2 A1))
(assert (cong C2 A1 A1 A2))

;; A1B2, B1C2, and C1A2 are concurrent (i.e., meet at Aux)
(assert (interLL Aux A1 B2 B1 C2))
(prove (coll Aux C1 A2))
