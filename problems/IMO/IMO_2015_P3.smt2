(param (A B C) acute-tri)
(assert (gt (dist A B) (dist A C)))
(define Gamma circle (circumcircle A B C))
(define H point (orthocenter A B C))
(define F point (foot A (line B C)))
(define M point (midp B C))

(param Q point (on-circ Gamma))
(assert (right H Q A))
(param K point (on-circ Gamma))
(assert (right H K Q))

(eval (tangent-cc (circumcircle K Q H) (circumcircle F K M)))