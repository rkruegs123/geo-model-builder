(param (A B C) triangle)
(define Omega circle (circumcircle A B C))
(define O point (circumcenter A B C))

(param D point (on-seg B C))
(define Gamma circle (coa A D))

(define E point (inter-lc (line B C) Gamma (rs-neq D)))
(assert (on-seg E B C))
(assert (on-seg E D C))

;; Note that order isn't explicitly stated
(define F point (inter-cc Gamma Omega rs-arbitrary))
(define G point (inter-cc Gamma Omega (rs-neq F)))

(define K point (inter-lc (line A B) (circumcircle B D F) (rs-neq B)))
(assert (on-seg K A B))

(define L point (inter-lc (line C A) (circumcircle C G E) (rs-neq C)))
(assert (on-seg L C A))

(define X point (inter-ll (line F K) (line G L)))
(eval (coll X A O))
