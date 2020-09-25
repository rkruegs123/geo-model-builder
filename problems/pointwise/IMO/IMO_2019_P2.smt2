(declare-points A B C A1 B1 P Q P1 Q1)

(assert (triangle A B C))

(assert (onSeg A1 B C))
(assert (onSeg B1 A C))

(assert (onSeg P A A1))
(assert (onSeg Q B B1))
(assert (para A B P Q))

(assert (onSeg B1 P P1))
(assert (eqangle P P1 P1 C B A A C))

(assert (onSeg A1 Q Q1))
(assert (eqangle C Q1 Q1 Q C B B A))

(prove (cycl P Q P1 Q1))
