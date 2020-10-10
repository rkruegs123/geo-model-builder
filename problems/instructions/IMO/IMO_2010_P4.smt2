(param (A B C) triangle)
(param P point (inPoly A B C))
(compute Gamma circle (circumcircle A B C))

(compute K point (interLC (line A P) Gamma (rsNeq A)))
(compute L point (interLC (line B P) Gamma (rsNeq B)))
(compute M point (interLC (line C P) Gamma (rsNeq C)))

(compute S point (interLL (perpAt C C (origin Gamma)) (line A B)))
(assert (cong S C S P))
(confirm (cong M K M L))
