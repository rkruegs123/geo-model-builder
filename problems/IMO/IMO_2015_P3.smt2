(param (A B C) acute-tri)
(assert (gt (dist A B) (dist A C)))
(let Gamma circle (circumcircle A B C))
(let H point (orthocenter A B C))
(let F point (foot A (line B C)))
(let M point (midp B C))

(param Q point (on-circ Gamma))
(assert (right H Q A))
(param K point (on-circ Gamma))
(assert (right H K Q))

(eval (tangent-cc (circumcircle K Q H) (circumcircle F K M)))