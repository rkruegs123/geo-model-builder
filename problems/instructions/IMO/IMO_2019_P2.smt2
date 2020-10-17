(param (A B C) triangle)

(param A1 point (on-seg B C))
(param B1 point (on-seg A C))

(param P point (on-seg A A1))
(compute Q point (inter-ll (line B B1) (para-at P (line A B))))

;; P1 is a point on line PB1 s.t. B1 lies strictly between P and P1
(param P1 point (on-ray-opp B1 P))
(assert (= (uangle P P1 C) (uangle B A C)))

(param Q1 point (on-ray-opp A1 Q))
(assert (= (uangle C Q1 Q) (uangle C B A)))

(confirm (on-circ P (circ Q P1 Q1)))
