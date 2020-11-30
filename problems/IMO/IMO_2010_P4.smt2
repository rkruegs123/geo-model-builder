(param (A B C) triangle)
(param P point (in-poly A B C))
(define Gamma circle (circumcircle A B C))

(define K point (inter-lc (line A P) Gamma (rs-neq A)))
(define L point (inter-lc (line B P) Gamma (rs-neq B)))
(define M point (inter-lc (line C P) Gamma (rs-neq C)))

(define S point (inter-ll (perp-at C (line C (origin Gamma))) (line A B)))
(assert (cong S C S P))
(eval (cong M K M L))
