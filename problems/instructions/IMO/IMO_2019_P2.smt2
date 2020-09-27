(sample (A B C) triangle)

(param A1 (onSeg A1 (line B C)))
(param B1 (onSeg B1 (line A C)))

(param P (onSeg P (line A A1)))
(compute Q (interLL (line B B1) (paraAt P (line A B))))

(param P1 (onSeg B1 (line P P1)))
(assert (= (oangle (slope (line P P1)) (slope (line P1 C))) (oangle (slope (line B A)) (slope (line A C)))))

(param Q1 (onSeg A1 Q Q1))
(assert (= (oangle (slope (line C Q1)) (slope (line Q1 Q))) (oangle (slope (line C B)) (slope (line B A)))))

(confirm (onC P (circ Q P1 Q1)))
