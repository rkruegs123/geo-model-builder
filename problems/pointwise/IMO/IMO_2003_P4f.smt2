(declare-points A B C D P Q R Aux)

;; ABCD is cyclic
(assert (polygon A B C D))
(assert (cycl A B C D))

;; The feet of the perpendicular from D to lines AB, BC, CA are P, Q, R respectively
(assert (foot P D A B))
(assert (foot Q D B C))
(assert (foot R D C A))

;; Angle bisectors of ABC and CDA meet on AC
(assert (ibisector Aux A B C))
(assert (ibisector Aux C D A))
(assert (coll Aux A C))

;; RP = RQ
(prove (cong R P R Q))
