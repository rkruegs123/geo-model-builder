(declare-points A B C D O P O1 O2 O3 O4 Mo1o3 Mo2o4 Mop)

(assert (polygon A B C D))
(assert (cycl A B C D))
(assert (circumcenter O A B C))

(assert (circumcenter O1 P A B))
(assert (circumcenter O2 P B C))
(assert (circumcenter O3 P C D))
(assert (circumcenter O4 P D A))

;; Prove that the midpoints of segments (O1,O3), (O2,O4), and (O,P) are collinear
(assert (midp Mo1o3 O1 O3))
(assert (midp Mo2o4 O2 O4))
(assert (midp Mop O P))
(prove (coll Mo1o3 Mo2o4 Mop))