(declare-points A B C D E F I1 I2 O1 O2)

;; ABC is an acute triangle
(assert (triangle A B C))
(assert (acutes A B C))

;; D, E, and F are the feet of the altitudes through A, B, and C, respectively
(assert (foot D A B C))
(assert (foot E B A C))
(assert (foot F C A B))

;; The incenters of the triangles AEF and BDF are I1 and I2, respectively
(assert (incenter I1 A E F))
(assert (incenter I2 B D F))

;; The circumcenters of the triangles ACI1 and BCI2 are O1 and O2, respectively
(assert (circumcenter O1 A C I1))
(assert (circumcenter O2 B C I2))

;; Prove that I1I2 and O1O2 are parallel
(prove (para I1 I2 O1 O2))
