(declare-points A B C D E F P Q)

;; ABC is an acute triangle with D, E, F the feet of the altitudes lying on BC, CA, AB, respectively
(assert (triangle A B C))
(assert (acutes A B C))

(assert (foot D A B C))
(assert (foot E B C A))
(assert (foot F C A B))

;; One of the intersection points of the line EF and the circumcircle is P
(assert (coll E F P))
(assert (cycl A B C P))

;; The lines BP and DF meet at Q
(assert (interLL Q B P D F))

;; Prove that AP = AQ
(prove (cong A P A Q))
