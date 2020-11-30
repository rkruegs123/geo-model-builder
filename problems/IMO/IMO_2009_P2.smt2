(param (A B C) triangle)
(define O point (circumcenter A B C))

(param P point (on-seg C A))
(param Q point (on-seg A B))

(define K point (midp B P))
(define L point (midp C Q))
(define M point (midp P Q))
(define Gamma circle (circ K L M))

(assert (tangent-lc (line P Q) Gamma))
(eval (cong O P O Q))