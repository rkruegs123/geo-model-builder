(param (A B C) acute-tri)
(compute Gamma circle (circumcircle A B C))

(param l line)
(assert (tangent-lc l Gamma))

(compute la line (reflect-ll l (line B C)))
(compute lb line (reflect-ll l (line C A)))
(compute lc line (reflect-ll l (line A B)))

(eval (tangent-cc Gamma (circumcircle (inter-ll la lb) (inter-ll la lc) (inter-ll lb lc))))