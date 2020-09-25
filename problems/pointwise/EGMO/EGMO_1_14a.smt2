(declare-points A B C D E F H Oaef)

(assert (triangle A B C))

;; D, E, F are the feet of the altitudes from A, B, and C
(assert (foot D A B C))
(assert (foot E B A C))
(assert (foot F C A B))

;; H is the orthocenter
(assert (orthocenter H A B C))

;; Prove that points A, E, F, H lie on a circle with diameter AH
(prove (cycl A E F H))

(assert (circumcenter Oaef A E F))
(prove (coll Oaef A H))