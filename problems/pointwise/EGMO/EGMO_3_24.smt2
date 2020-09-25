(declare-points A B C X G K)

(assert (triangle A B C))

;; X is on (ABC) with AX || BC and X /= A
(assert (cycl X A B C))
(assert (para A X B C))

;; G is the centroid of ABC
(assert (centroid G A B C))

;; K is the foot of the altitude from A to BC
(assert (foot K A B C))

;; Prove that K, G, X are collinear
(prove (coll K G X))