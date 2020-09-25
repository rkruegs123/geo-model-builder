;; Note: This is a subproblem of proving that AX bisects BC

(declare-points A B C I D E F X B1 C1)

(assert (triangle A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; DEF is the contact triangle of ABC
(assert (foot D I B C))
(assert (foot E I A C))
(assert (foot F I A B))

;; X is on EF s.t. XD is perpendicular to BC
(assert (onSeg X E F))
(assert (perp X D B C))

;; We take the line through X parallel to BC that meets AB and AC again at B1 and C1
(assert (para B1 X B C))
(assert (onSeg B1 A B))
(assert (interLL C1 X B1 A C))

;; Prove that I lies on (AB1C1)
(prove (cycl I A B1 C1))