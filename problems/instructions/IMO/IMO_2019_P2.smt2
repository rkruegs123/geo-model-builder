(param (A B C) triangle)

(param A1 point (onSeg B C))
(param B1 point (onSeg A C))

(param P point (onSeg A A1))
(compute Q point (interLL (line B B1) (paraAt P A B)))

(param P1 point (onLine (line P B1)))
(assert (onSeg B1 P P1))
(assert (= (uangle P P1 C) (uangle B A C)))

(param Q1 point (onLine (line Q A)))
(assert (onSeg A1 Q Q1))
(assert (= (uangle C Q1 Q) (uangle C B A)))

(confirm (onCirc P (circ Q P1 Q1)))
