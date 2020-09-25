(declare-points A B C D I W X Y Z M N)

(assert (polygon A B C D))
(assert (insidePolygon I A B C D))

;; W, X, Y, Z denote the tangency points of the incircle of ABCD to sides AB, BC, CD, DA
(assert (cong I W I X))
(assert (cong I W I Y))
(assert (cong I W I Z))
(assert (foot W I A B))
(assert (foot X I B C))
(assert (foot Y I C D))
(assert (foot Z I D A))

;; Prove that I lies on the line joining the midpoints of AC and BD
(assert (midp M A C))
(assert (midp N B D))
(prove (coll I M N))
