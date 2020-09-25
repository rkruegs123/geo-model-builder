(declare-points A B C I A1 B1 C1)

;; I is the incenter of ABC
(assert (triangle A B C))
(assert (incenter I A B C))

;; Internal bisectors of angles A, B, C meet opposite sides in A1, B1, C1, respectively
(assert (ibisector A1 C A B))
(assert (coll A1 B C))

(assert (ibisector B1 A B C))
(assert (coll B1 C A))

(assert (ibisector C1 B C A))
(assert (coll C1 A B))

;; TODO: goal is too arithmetic for us currently
