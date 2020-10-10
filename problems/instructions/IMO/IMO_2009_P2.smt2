(param (A B C) triangle)
(compute O point (circumcenter A B C))

(param P point (onSeg C A))
(param Q point (onSeg A B))

(compute K point (midp B P))
(compute L point (midp C Q))
(compute M point (midp P Q))
(compute Gamma circle (circ K L M))

(assert (tangent (line P Q) Gamma))
(confirm (cong O P O Q))