(param (A B C) triangle)
(define I point (incenter A B C))
(define Gamma circle (circumcircle A B C))

(define D point (inter-lc (line A I) Gamma (rs-neq A)))
(param E point (on-circ Gamma))
(assert (same-side D E (line B C)))

(param F point (on-seg B C))
(assert (= (uangle B A F) (uangle C A E)))
(assert (lt (uangle C A E) (mul 0.5 (uangle B A C))))

(define G point (midp I F))
(eval (on-circ (inter-ll (line D G) (line E I)) Gamma))