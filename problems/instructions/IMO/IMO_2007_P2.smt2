(param (B C E D) polygon)
(assert (cycl B C E D))
(compute A point (interLL (paraAt D B C) (paraAt B D C)))

(compute F point (interLC (line D C) (coa E C) (rsNeq C)))
(assert (between F D C))

(compute l line (line F A))
(compute G point (interLL l (line B C)))

(assert (cong E F E G))
