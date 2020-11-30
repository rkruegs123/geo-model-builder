(param Omega circle)
(param R point (on-circ Omega))
(param S point (on-circ Omega))
(assert (not (coll R S (origin Omega))))

(define l line (perp-at R (line (origin Omega) R)))
(define T point (midp-from S R))

(param J point (on-minor-arc Omega R S))
(define Gamma circle (circumcircle J S T))

(define A point (inter-lc l Gamma (rs-closer-to-p R)))
(assert (not (eq A (inter-lc l Gamma (rs-neq A)))))

(define K point (inter-lc (line A J) Omega (rs-neq J)))

(eval (tangent-lc (line K T) Gamma))