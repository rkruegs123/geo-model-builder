(joint (A B C) (triangle A B C))

(param   A1 (onL A1 (line B C)) (btw A1 B C))
(param   B1 (onL B1 (line A C)) (btw B1 A C))

(param   P  (onL P (line A A1)) (btw P A A1))
(compute Q  (interLL (line B B1) (paraAt P (line A B))))

(param   P1 (onL P1 (line P B1)) (btw B1 P P1))
(assert (= (oangle (slope (line P P1)) (slope (line P1 C))) (oangle (slope (line B A)) (slope (line A C)))))

(param   Q1 (onL Q1 (line Q A1)) (btw A1 Q Q1))
(assert (= (oangle (slope (line C Q1)) (slope (line Q1 Q))) (oangle (slope (line C B)) (slope (line B A)))))

(prove (onC P (circ Q P1 Q1)))
