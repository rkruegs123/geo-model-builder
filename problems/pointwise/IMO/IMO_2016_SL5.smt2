(declare-points A B C CCabc O D X Y S P M CCxsy)

;; ABC is an acute scalene triangle
;; TODO: More natural way to express acute scalene
(assert (triangle A B C))
(assert (acutes A B C))

(assert (not (cong A B B C)))
(assert (not (cong A B A C)))
(assert (not (cong B C A C)))

;; CCabc is the circumcenter of ABC
(assert (circumcenter CCabc A B C))

;; O is the orthocenter of ABC
(assert (orthocenter O A B C))

;; The Euler line is the line passing through the circumcenter and the orthocenter
;; D is the foot from A to the Euler line
(assert (foot D A O CCabc))

;; A circle with center S passes through A and D, and intersects sides AB and AC at X and Y, respectively
(assert (cycl A D X Y))
(assert (circumcenter S A D X))
(assert (onSeg X A B))
(assert (onSeg Y A C))

;; P is the foot from A to BC
(assert (foot P A B C))

;; M is the midpoint of BC
(assert (midp M B C))

;; Prove that the circumcenter of triangle XSY is equidistance from P and M
(assert (circumcenter CCxsy X S Y))
(prove (cong CCxsy P CCxsy M))
