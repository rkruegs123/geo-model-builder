(param (A B C) acute-tri)
(let Gamma circle (circumcircle A B C))

(param l line (tangent-lc Gamma))
;; (assert (tangent-lc l Gamma))

(let la line (reflect-ll l (line B C)))
(let lb line (reflect-ll l (line C A)))
(let lc line (reflect-ll l (line A B)))

(eval (tangent-cc Gamma (circumcircle (inter-ll la lb) (inter-ll la lc) (inter-ll lb lc))))