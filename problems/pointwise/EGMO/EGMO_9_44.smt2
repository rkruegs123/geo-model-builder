(declare-points A B C D H E F)

(assert (triangle A B C))
(assert (acutes A B C))

(assert (foot D A B C))

(assert (onSeg H A D))

(assert (interLL E B H A C))
(assert (interLL F C H A B))

(prove (eqangle E D D H H D D F))
