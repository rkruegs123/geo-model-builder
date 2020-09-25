;; (declare-points A B C Ok D E Mc C1 E1 X)
(declare-points A B C Ok Mc D E C1 E1 X)

;; ABC is a triangle
(assert (triangle A B C))

;; k is a circle through C tangent to AB at B
(assert (cong Ok C Ok B))
(assert (perp Ok B A B))

;; Side AC and the C-median of ABC intersect k again at D and E
(assert (cong Ok C Ok D))
(assert (coll D A C))

(assert (cong Ok C Ok E))
(assert (midp Mc A B))
(assert (coll E C Mc))

;; The intersecting point of the tangents to k through C and E lies on the line BD
(assert (perp C C1 Ok C))
(assert (perp E E1 Ok E))
(assert (interLL X C C1 E E1))
(assert (coll X B D))

;; Prove that <ABC = 90
(prove (perp A B B C))
