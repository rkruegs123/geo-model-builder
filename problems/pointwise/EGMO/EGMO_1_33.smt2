(declare-points A B C O D1 K)

(assert (triangle A B C))
(assert (circumcenter O A B C))

;; Ray AO meets BC at D1
(assert (interLL D1 A O B C))
(assert (onRay D1 A O))

;; Point K is selected s.t. KA is tangent to ABC and <KCB = 90
(assert (perp K A A O))
(assert (perp K C C B))

;; Prove that KD1 || AB
(confirm (para K D1 A B))