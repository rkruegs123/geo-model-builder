;; O is the center of Omega
;; P is the center of omega

(declare-points A B T O P K M D L C I)

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

;; D is a point on AB s.t. CD is tangent to omega at L
(assert (onSeg D A B))
(assert (perp D L L P))
(assert (cong P L P K))
(assert (cong P L P T))

;; C is another point on arc AB not containing T
(assert (coll D L C))
(assert (cycl C T A B))
(assert (oppSides C M A B))

;; I is the intersection of CM and KL
(assert (interLL I C M K L))

;; prove that C, L, I, T are concyclic
(prove (cycl C L I T))
