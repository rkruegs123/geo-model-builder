(param (B C E D) polygon)
(assert (cycl B C E D))
(compute A point (interLL (paraAt D B C) (paraAt B D C)))

(param l line (through A))
(compute F point (interLL l (line D C)))
(assert (onSeg F D C))
(compute G point (interLL l (line B C)))

(assert (cong E F E G))
(assert (cong E F E C))
