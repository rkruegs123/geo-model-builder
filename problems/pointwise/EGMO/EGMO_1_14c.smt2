(declare-points A B C D E F H)

(assert (triangle A B C))

;; D, E, F are the feet of the altitudes from A, B, and C
(assert (foot D A B C))
(assert (foot E B A C))
(assert (foot F C A B))

;; H is the orthocenter
(assert (orthocenter H A B C))

;; Prove that H is the incenter of DEF
(prove (incenter H D E F))