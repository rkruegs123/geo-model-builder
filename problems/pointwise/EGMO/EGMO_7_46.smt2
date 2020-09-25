(declare-points A B C P Q C1 B1)

(assert (triangle A B C))
(assert (acutes A B C))

(assert (onSeg P B C))
(assert (onSeg Q B C))

(assert (cycl A P B C1))
(assert (para Q C1 C A))
(assert (oppSides C1 Q A B))

(assert (cycl A P C B1))
(assert (para Q B1 B A))
(assert (oppSides B1 Q A C))

(prove (cycl B1 C1 P Q))