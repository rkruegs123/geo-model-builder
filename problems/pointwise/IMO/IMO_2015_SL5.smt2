(declare-points A B C D F G H I O H1 I1 Q M P)

;; ABC is a triangle with CA /= CB
(assert (triangle A B C))
(assert (not (cong C A C B)))

;; D, F, and G are the midpoints of the sides AB, AC, and BC, respectively
(assert (midp D A B))
(assert (midp F A C))
(assert (midp G B C))

;; Gamma passes through C and is tangent to AB at D
;; Gamma meets AF and BG at H and I, respectively
(assert (cycl C D H I))
(assert (cong O C O D))
(assert (cong O C O H))
(assert (perp O D A B))
(assert (onSeg H A F))
(assert (onSeg I B G))

;; H1 and I1 are symmetric to H and I about F and G, respectively
(assert (midp F H H1))
(assert (midp G I I1))

;; H1I1 meets CD and FG at Q and M, respectively
(assert (interLL Q H1 I1 C D))
(assert (interLL M H1 I1 F G))

;; CM meets Gamma again at P
(assert (cycl P C D H))
(assert (coll P C M))

;; Prove that CQ = QP
(prove (cong C Q Q P))
