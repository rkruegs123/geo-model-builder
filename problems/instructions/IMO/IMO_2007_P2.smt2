(param (B C D) polygon)
(param E point (on-circ (circumcircle B C D)))

(compute A point (inter-ll (para-at D (line B C)) (para-at B (line D C))))

(compute F point (inter-lc (line D C) (coa E C) (rs-neq C)))
(assert (on-seg F D C))

(compute l line (line F A))
(compute G point (inter-ll l (line B C)))

(assert (cong E F E G))

(eval (eq l (i-bisector D A B)))
