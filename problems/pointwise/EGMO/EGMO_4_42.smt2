(declare-points A B C I Ciab Cibc Cica Cabc)

;; I is the incenter of triangle ABC
(assert (triangle A B C))
(assert (incenter I A B C))

;; Show that the circumcenters of IAB, IBC, and ICA lie on a circle whose center is the circumcenter of ABC
(assert (circumcenter Ciab I A B))
(assert (circumcenter Cibc I B C))
(assert (circumcenter Cica I C A))
(assert (circumcenter Cabc A B C))
(prove (cong Cabc Ciab Cabc Cibc))
(prove (cong Cabc Ciab Cabc Cica))