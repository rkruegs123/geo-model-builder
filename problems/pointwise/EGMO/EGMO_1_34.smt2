(declare-points A B C Mbc K)

;; ABC is a scalene triangle
(assert (triangle A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong A C B C)))

;; K is the intersection of the angle bisector of <A and the perpendicular bisector of BC
(assert (midp Mbc B C))
(assert (perp K Mbc B C))
(assert (ibisector K C A B))

(prove (cycl A B C K))