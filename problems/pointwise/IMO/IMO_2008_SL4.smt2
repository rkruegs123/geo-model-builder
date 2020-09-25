(declare-points A B C E F P Q Oafp Oafq Aux)

;; ABC is an acute triangle
(assert (triangle A B C))
(assert (acutes A B C))

;; BE and CF are altitudes
(assert (foot E B A C))
(assert (foot F C A B))

;; Two circles passing through A and F are tangent to the line BC at the points P and Q so that B lies between C and Q
(assert (onSeg B C Q))
(assert (coll P B C))

;;      Circle through A, F, and P
(assert (circumcenter Oafp A F P))
(assert (circumcenter Oafq A F Q))
(assert (perp P B P Oafp))
(assert (perp Q B Q Oafq))

;; Prove that lines PE and QF intersect on the circumcircle of triangle AEF
(assert (interLL Aux P E Q F))
(prove (cycl Aux A E F))
