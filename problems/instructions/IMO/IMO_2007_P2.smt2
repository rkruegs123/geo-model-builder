(param (B C D) polygon)
(param E point (onCirc (circumcircle B C D)))

(compute A point (interLL (paraAt D (line B C)) (paraAt B (line D C))))

(compute F point (interLC (line D C) (coa E C) (rsNeq C)))
(assert (onSeg F D C))

(compute l line (line F A))
(compute G point (interLL l (line B C)))

(assert (cong E F E G))
