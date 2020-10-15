(param (A B C) triangle)
(compute Omega circle (circumcircle A B C))
(compute O point (circumcenter A B C))

(param D point (onSeg B C))
(compute Gamma circle (coa A D))

(compute E point (interLC (line B C) Gamma (rsNeq D)))
(assert (onSeg E B C))
(assert (onSeg E D C))

;; Note that order isn't explicitly stated
(compute F point (interCC Gamma Omega rsArbitrary))
(compute G point (interCC Gamma Omega (rsNeq F)))

(compute K point (interLC (line A B) (circumcircle B D F) (rsNeq B)))
(assert (onSeg K A B))

(compute L point (interLC (line C A) (circumcircle C G E) (rsNeq C)))
(assert (onSeg L C A))

(compute X point (interLL (line F K) (line G L)))
(confirm (coll X A O))
