;; Note that Ia is really the A-excenter
(declare-points A B C I L Ia)

(assert (triangle A B C))
(assert (incenter I A B C))

;; Ray AI meets (ABC) again at L
(assert (cycl L A B C))
(assert (onRay L A I))

;; Let Ia be the reflection of I over L
(assert (midp L I Ia))

;; Prove that the points I, B, C and Ia lie on a circle with diameter IIa and center L
;; Note: We already know (coll I Ia L)
(confirm (cycl I B C Ia))
