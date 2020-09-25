(declare-points P0 P1 P2 P3 P4 Q0 Q1 Q2 Q3 Q4 M0 M1 M2 M3 M4)

(assert (polygon P0 P1 P2 P3 P4))

(assert (interLL Q1 P0 P1 P2 P3))
(assert (interLL Q2 P1 P2 P3 P4))
(assert (interLL Q3 P2 P3 P4 P0))
(assert (interLL Q4 P3 P4 P0 P1))
(assert (interLL Q0 P4 P0 P1 P2))

(assert (cycl M1 Q0 P0 P1))
(assert (cycl M1 Q1 P1 P2))

(assert (cycl M2 Q1 P1 P2))
(assert (cycl M2 Q2 P2 P3))

(assert (cycl M3 Q2 P2 P3))
(assert (cycl M3 Q3 P3 P4))

(assert (cycl M4 Q3 P3 P4))
(assert (cycl M4 Q4 P4 P0))

(assert (cycl M0 Q4 P4 P0))
(assert (cycl M0 Q0 P0 P1))

(prove (cycl M0 M1 M2 M3 M4))
