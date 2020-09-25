(declare-points A B C D E F I J K)

;; ABCD is a trapezoid with parallel sides AB and CD
(assert (polygon A B C D))
(assert (para A B C D))

;; E is on line BC outside segment BC
(assert (coll E B C))
(assert (not (onSeg E B C)))

;; F is inside segment AD
(assert (onSeg F A D))

;; <DAE = <CBF
(assert (eqangle D A A E C B B F))

;; I is the point of intersection of CD and EF
(assert (interLL I C D E F))

;; J is the point of intersection of AB and EF
(assert (interLL J A B E F))

;; K is the midpoint of EF (and doesn't lie on line AB)
(assert (midp K E F))
(assert (not (coll K A B)))

;; If K belongs to the circumcircle of CDJ, then I belongs to the circumcircle of ABK
(assert (cycl K C D J))
(prove (cycl I A B K))
