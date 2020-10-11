(param (A B C D) polygon)
(assert (cong B C D A))
(assert (not (para B C D A)))

(param E point (onSeg B C))
(param F point (onSeg D A))
(assert (cong B E D F))

(compute P point (interLL A C B D))
(compute Q point (interLL B D E F))
(compute R point (interLL E F A C))
