(param (A B C) triangle)

(param A1 point (onSeg B C))
(param B1 point (onSeg A C))

(param P point (onSeg A A1))
(compute Q point (interLL (line B B1) (paraAt P (line A B))))

;; P1 is a point on line PB1 s.t. B1 lies strictly between P and P1
(param P1 point (onRayOpp B1 P))
(assert (= (uangle P P1 C) (uangle B A C)))

(param Q1 point (onRayOpp A1 Q))
(assert (= (uangle C Q1 Q) (uangle C B A)))

(confirm (onCirc P (circ Q P1 Q1)))
