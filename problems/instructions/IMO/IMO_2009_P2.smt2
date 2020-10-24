(param (A B C) triangle)
(compute O point (circumcenter A B C))

(param P point (on-seg C A))
(param Q point (on-seg A B))

(compute K point (midp B P))
(compute L point (midp C Q))
(compute M point (midp P Q))
(compute Gamma circle (circ K L M))

(assert (tangent-lc (line P Q) Gamma))
(eval (cong O P O Q))