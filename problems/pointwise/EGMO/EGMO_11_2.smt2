(declare-points A B C O D E F K)

(assert (triangle A B C))
(assert (circumcenter O A B C))

(assert (onSeg D B C))
(assert (onSeg E C A))
(assert (onSeg F A B))
(assert (perp D E C O))
(assert (perp D F B O))

(assert (circumcenter K A F E))

(prove (perp D K B C))