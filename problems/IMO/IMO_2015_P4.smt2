(param (A B C) triangle)
(let Omega circle (circumcircle A B C))
(let O point (circumcenter A B C))

(param D point (on-seg B C))
(let Gamma circle (coa A D))

(let E point (inter-lc (line B C) Gamma (rs-neq D)))
(assert (on-seg E B C))
(assert (on-seg E D C))

;; Note that order isn't explicitly stated
(let F point (inter-cc Gamma Omega rs-arbitrary))
(let G point (inter-cc Gamma Omega (rs-neq F)))

(let K point (inter-lc (line A B) (circumcircle B D F) (rs-neq B)))
(assert (on-seg K A B))

(let L point (inter-lc (line C A) (circumcircle C G E) (rs-neq C)))
(assert (on-seg L C A))

(let X point (inter-ll (line F K) (line G L)))
(eval (coll X A O))
