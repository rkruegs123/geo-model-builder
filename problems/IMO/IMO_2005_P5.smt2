(param (A B C D) polygon)
(assert (cong B C D A))
(assert (not (para (line B C) (line D A))))

(param E point (on-seg B C))
(param F point (on-seg D A))
(assert (cong B E D F))

(let P point (inter-ll (line A C) (line B D)))
(let Q point (inter-ll (line B D) (line E F)))
(let R point (inter-ll (line E F) (line A C)))
