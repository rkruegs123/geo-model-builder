(param (A B C) triangle)
(let O point (circumcenter A B C))

(param P point (on-seg C A))
(param Q point (on-seg A B))

(let K point (midp B P))
(let L point (midp C Q))
(let M point (midp P Q))
(let Gamma circle (circ K L M))

(assert (tangent-lc (line P Q) Gamma))
(eval (cong O P O Q))