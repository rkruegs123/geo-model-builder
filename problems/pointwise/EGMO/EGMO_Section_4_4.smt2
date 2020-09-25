;; Note: The following problem is the global goal of section 4.4

(declare-points A B C I D E F X M)

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

;; Prove that ray AX bisects BC
(assert (interLL M A X B C))
(prove (cong M B M C))