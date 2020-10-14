(param (A B C) acuteTri)
(compute Gamma circle (circumcircle A B C))

(param l line)
(assert (tangentLC l Gamma))

(compute la line (reflectLL l (line B C)))
(compute lb line (reflectLL l (line C A)))
(compute lc line (reflectLL l (line A B)))

(confirm (tangentCC Gamma (circumcircle (interLL la lb) (interLL la lc) (interLL lb lc))))