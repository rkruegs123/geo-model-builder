(declare-points A B C O I P Q)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (circumcenter O A B C))

;; Let P and Q denote the reflections of B and C across CI and BI, respectively
(assert (cong C P C B))
(assert (perp P B C I))

(assert (cong B Q B C))
(assert (perp Q C B I))

;; Show that PQ is perp to OI
(prove (perp P Q O I))