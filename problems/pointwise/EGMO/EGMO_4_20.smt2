(declare-points A B C P X Y Z Mbc X1 Mac Y1 Mab Z1 P1)

(assert (triangle A B C))
(assert (insidePolygon P A B C))

;; X, Y, and Z are the feet of the cevians through P
(assert (onSeg X B C))
(assert (coll X A P))

(assert (onSeg Y A C))
(assert (coll Y B P))

(assert (onSeg Z A B))
(assert (coll Z C P))

;; X1 is the reflection of X about the midpoint of BC
(assert (midp Mbc B C))
(assert (midp Mbc X X1))

;; Y1 is the reflection of Y about the midpoint of AC
(assert (midp Mac A C))
(assert (midp Mac Y Y1))

;; Z1 is the reflection of Z about the midpoint of AB
(assert (midp Mab A B))
(assert (midp Mab Z Z1))

;; Prove that the cevians AX1, BY1, CZ1 concur at a point P1
;; Note: P1 is the isotomic conjugate of P!
(assert (interLL P1 A X1 B Y1))
(prove (coll P1 C Z1))