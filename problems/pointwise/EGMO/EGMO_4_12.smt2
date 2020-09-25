(declare-points A B C Ia I X K M)

(assert (triangle A B C))

;; Ia is the A-excenter of ABC
(assert (excenter Ia A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; The A-excircle is tangent to BC at X
(assert (onSeg X B C))
(assert (perp B C X Ia))

;; K is the foot of A to BC
(assert (foot K A B C))

;; M is the midpoitn of AK
(assert (midp M A K))

;; Prove that X, I and M are collinear
(prove (coll X I M))