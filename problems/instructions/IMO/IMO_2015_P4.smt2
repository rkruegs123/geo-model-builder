(param (A B C) triangle)
(compute Omega circle (circumcircle A B C))
(compute O point (circumcenter A B C))

(param D point (on-seg B C))
(compute Gamma circle (coa A D))

(compute E point (inter-lc (line B C) Gamma (rs-neq D)))
(assert (on-seg E B C))
(assert (on-seg E D C))

;; Note that order isn't explicitly stated
(compute F point (inter-cc Gamma Omega rs-arbitrary))
(compute G point (inter-cc Gamma Omega (rs-neq F)))

(compute K point (inter-lc (line A B) (circumcircle B D F) (rs-neq B)))
(assert (on-seg K A B))

(compute L point (inter-lc (line C A) (circumcircle C G E) (rs-neq C)))
(assert (on-seg L C A))

(compute X point (inter-ll (line F K) (line G L)))
(eval (coll X A O))
