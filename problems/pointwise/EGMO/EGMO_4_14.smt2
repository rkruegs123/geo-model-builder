;; Note: This lemma is a summary of the results from problems 4.12 and 4.13

(declare-points A B C Ia I D X K M)

(assert (triangle A B C))

;; Ia is the A-excenter of ABC
(assert (excenter Ia A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; D is the foot from the incenter to BC
(assert (foot D I B C))

;; The A-excircle is tangent to BC at X
(assert (onSeg X B C))
(assert (perp B C X Ia))

;; K is the foot of A to BC
(assert (foot K A B C))

;; Prove that lines DIa and XI concur at the midpoint of the altitude from A
(assert (midp M A K))
(prove (interLL M D Ia X I))
