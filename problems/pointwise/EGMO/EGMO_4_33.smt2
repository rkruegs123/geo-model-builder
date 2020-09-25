;; O is the center of Omega
;; P is the center of omega

(declare-points A B T O P K M)

;; Omega is a circle with center O and a chord AB
;; Consider a circle omega tangent internally to Omega at T and to AB at K
(assert (triangle A B T))
(assert (circumcenter O A B T))
(assert (onSeg K A B))
(assert (cong P K P T))
(assert (perp A B P K))
(assert (onSeg P O T))

;; M is the midpoint of arc AB not containing T
(assert (amidpOpp M A B T))

;; Ray TK passes through the midpoint M of the arc AB not containing T
(prove (onRay M T K))
