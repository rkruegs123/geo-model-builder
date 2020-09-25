(declare-points A B M C D N)

;; Choose a point M on AB
(assert (onSeg M A B))

;; Two equilateral triangles AMC and BMD are constructed on the same side of AB
(assert (sameSide C D A B))
(assert (cong A M A C))
(assert (cong A M M C))
(assert (cong B M B D))
(assert (cong B M M D))

;; The circumcircles of the two triangles intersect in a point M and another point N
(assert (cycl N A M C))
(assert (cycl N B M D))

;; Prove that AD and BC pass through point N
(prove (interLL N A D B C))
