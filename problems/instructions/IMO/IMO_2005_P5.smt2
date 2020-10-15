(param (A B C D) polygon)
(assert (cong B C D A))
(assert (not (para (line B C) (line D A))))

(param E point (onSeg B C))
(param F point (onSeg D A))
(assert (cong B E D F))

(compute P point (interLL (line A C) (line B D)))
(compute Q point (interLL (line B D) (line E F)))
(compute R point (interLL (line E F) (line A C)))
