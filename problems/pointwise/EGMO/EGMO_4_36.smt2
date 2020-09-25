;; O is the center of omega
;; Oabc is the circumcenter of ABC

(declare-points A B C D L K O T Oabc I)

;; ABC is a triangle
(assert (triangle A B C))

;; D is a point on AB
(assert (onSeg D A B))

;; Suppose a circle omega is tangent to CD at L...
(assert (perp O L C D))
(assert (onSeg L C D))

;; ... and tangent to AB at K ...
(assert (perp O K A B))
(assert (onSeg K A B))

(assert (cong O K O L))

;; ... and tangent to (ABC)
(assert (cycl T A B C))
(assert (cong O K O T))
(assert (circumcenter Oabc A B C))
(assert (coll T O Oabc))

;; The incenter of ABC lies on line LK
(assert (incenter I A B C))
(prove (coll I L K))