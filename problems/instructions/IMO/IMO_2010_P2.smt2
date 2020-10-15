(param (A B C) triangle)
(compute I point (incenter A B C))
(compute Gamma circle (circumcircle A B C))

(compute D point (interLC (line A I) Gamma (rsNeq A)))
(param E point (onCirc Gamma))
(assert (sameSide D E (line B C)))

(param F point (onSeg B C))
(assert (eqN (uangle B A F) (uangle C A E)))
(assert (lt (uangle C A E) (mul 0.5 (uangle B A C))))

(compute G point (midp I F))
(confirm (onCirc (interLL (line D G) (line E I)) Gamma))