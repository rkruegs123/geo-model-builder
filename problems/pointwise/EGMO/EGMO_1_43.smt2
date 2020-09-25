(declare-points A B C D E O P M)

;; ABCDE lie on a circle
(assert (polygon A B C D E))
(assert (cycl A B C D))
(assert (cycl A B C E))
(assert (circumcenter O A B C))

;; P lies outside the circle
(assert (distGt O P O A))

;; PB and PD are tangent to (ABCDE)
(assert (perp P B O B))
(assert (perp P D O D))

;; P, A, C are collinear
(assert (coll P A C))

;; DE is parallel to AC
(assert (para D E A C))

;; Prove that BE bisects AC
(assert (interLL M B E A C))
(prove (midp M A C))