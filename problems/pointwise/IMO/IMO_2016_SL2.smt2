(declare-points A B C I M D Iperp F E X Aux)

;; I is the incenter of ABC
(assert (triangle A B C))
(assert (incenter I A B C))

;; M is the midpoint of BC
(assert (midp M B C))

;; D is the foot from I to BC
(assert (foot D I B C))

;; The line through I perp. to AI meets sides AB and AC at F and E, respectively
(assert (perp I Iperp A I))
(assert (interLL F I Iperp A B))
(assert (interLL E I Iperp A C))

;; The circumcircle of AEF intersects the circumcircle of ABC at a point X other than A
(assert (cycl A E F X))
(assert (cycl A B C X))

;; Prove that lines XD and AM meet on the circumcircle of ABC
(assert (interLL Aux X D A M))
(prove (cycl Aux A B C))