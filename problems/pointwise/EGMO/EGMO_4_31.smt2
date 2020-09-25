(declare-points A B T O K P M)

;; Omega is a circle with center O and a chord AB
;; Consider a circle omega tangent internally to Omega at T and to AB at K
(assert (triangle A B T))
(assert (circumcenter O A B T))
(assert (onSeg K A B))
(assert (cong P K P T))
(assert (perp A B P K))
(assert (onSeg P O T))
(assert (amidpOpp M A B T))

(prove (coll T K M))
