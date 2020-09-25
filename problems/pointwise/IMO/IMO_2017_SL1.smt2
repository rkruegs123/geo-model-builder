(declare-points A B C D E Efoot Aux)

;; ABCDE is a convex pentagon s.t. AB = BC = CD
(assert (polygon A B C D E))
(assert (cong A B B C))
(assert (cong B C C D))

;; ang(EAB) = ang(BCD)
(assert (eqangle E A A B B C C D))

;; ang(EDC) = ang(CBA)
(assert (eqangle E D D C C B B A))

;; prove that the perpendicular line from E to BC and the line segments AC and BD are concurrent
(assert (foot Efoot E B C))
(assert (interLL Aux A C B D))
(prove (coll Aux Efoot E))