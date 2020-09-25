(declare-points A B C Ia I D K M)

(assert (triangle A B C))

;; Ia is the A-excenter of ABC
(assert (excenter Ia A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; D is the foot from the incenter to BC
(assert (foot D I B C))

;; K is the foot of A to BC
(assert (foot K A B C))

;; M is the midpoitn of AK
(assert (midp M A K))

;; Prove that D, Ia, and M are collinear
(prove (coll D Ia M))