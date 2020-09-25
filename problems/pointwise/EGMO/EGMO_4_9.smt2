(declare-points A B C I D E X Ia)

(assert (triangle A B C))

(assert (incenter I A B C))
(assert (foot D I B C))

;; DE is a diameter of the incircle
(assert (coll E D I))
(assert (cong I D I E))

;; Ray AE meets BC at X
(assert (interLL X A E B C))
(assert (onRay X A E))

;; Prove that BD = CX
(prove (cong B D C X))

;; Prove that X is the tangency point of the A-excircle to BC
(assert (excenter Ia A B C))
;; Note: At this point, we know X is on BC
(prove (perp B C Ia X))