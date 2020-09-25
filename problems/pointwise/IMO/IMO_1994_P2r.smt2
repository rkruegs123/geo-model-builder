(declare-points A B C M O Q E F)

;; ABC is an isosceles triangle with AB = AC
(assert (triangle A B C))
(assert (cong A B A C))

;; M is the midpoint of BC
(assert (midp M B C))

;; O is the point on line AM s.t. OB is perpendicular to AB
(assert (coll O A M))
(assert (perp O B A B))

;; Q is an arbitrary point on the segment BC
(assert (onSeg Q B C))

;; E lies on the line AB
(assert (coll E A B))

;; F lies on the line AC s.t. E, Q, F are distinct and collinear
(assert (coll F A C))
(assert (coll E Q F))

;; If OQ is perpendicular to EF, then QE = QF,
(assert (perp O Q E F))
(prove (cong Q E Q F))
