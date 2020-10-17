(param (A B C) acute-tri)
(assert (gt (dist A B) (dist A C)))
(compute Gamma circle (circumcircle A B C))
(compute H point (orthocenter A B C))
(compute F point (foot A (line B C)))
(compute M point (midp B C))

(param Q point (on-circ Gamma))
(assert (right H Q A))
(param K point (on-circ Gamma))
(assert (right H K Q))

(confirm (tangent-cc (circumcircle K Q H) (circumcircle F K M)))