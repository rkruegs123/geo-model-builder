(param (A B C) acute-tri)
(define Gamma circle (circumcircle A B C))

(param l line (tangent-lc Gamma))
;; (assert (tangent-lc l Gamma))

(define la line (reflect-ll l (line B C)))
(define lb line (reflect-ll l (line C A)))
(define lc line (reflect-ll l (line A B)))

(eval (tangent-cc Gamma (circumcircle (inter-ll la lb) (inter-ll la lc) (inter-ll lb lc))))