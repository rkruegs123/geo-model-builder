(declare-points A B C D E F G)

;; TODO: awkward since problem statement doesn't say this explicitly
(assert (polygon A B C D))

;; ABCD is a parallelogram
(assert (para A B C D))
(assert (para A D B C))

;; BCED is a cyclic quadrilateral
(assert (cycl E B C D))

;; There is a line l that passes through A, the segment DC at F, and the line BC at G
(assert (onSeg F D C))
(assert (coll G B C))
(assert (coll A F G))

;; EF = EG = EC
(assert (cong E F E G))
(assert (cong E F E C))

;; l is the bisector of angle D A B
(prove (ibisector G D A B))
