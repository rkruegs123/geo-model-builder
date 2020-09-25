(declare-points A B C O K D)

(assert (triangle A B C))
(assert (acutes A B C))
(assert (circumcenter O A B C))

(assert (perp K A O A))
(assert (perp K C C B))

(assert (onSeg D B C))
(assert (para K D A B))

(prove (coll A D O))