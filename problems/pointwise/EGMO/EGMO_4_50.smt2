(declare-points A B C O I H K L A0 B0 C0 D E F Aux)

;; ABC is a scalene triangle
(assert (triangle A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong A C B C)))

;; O is the circumcenter of ABC
(assert (circumcenter O A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; H, K, and L are the feet of the altitudes of triangle ABC from vertices A, B, C, respectively
(assert (foot H A B C))
(assert (foot K B A C))
(assert (foot L C A B))

;; Denote by A0, B0, C0 the midpoints of altitudes AH, BK, CL
(assert (midp A0 A H))
(assert (midp B0 B K))
(assert (midp C0 C L))

;; The incircle of triangle ABC touches sides BC, CA, AB at points D, E, F respectively
(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))

;; Prove that the four lines A0D, B0E, C0F, and OI are concurrent
(assert (interLL Aux A0 D B0 E))
(prove (interLL Aux C0 F O I))