(declare-points A B C O D E mBD F mCE G)

;; really acute, tmp disabled to test skolem
(assert (triangle A B C))
(assert (circumcenter O A B C))

;; D, E
(assert (onSeg D A B))
(assert (onSeg E A C))
(assert (cong A D A E))

;; F, G
(assert (midp mBD B D))
(assert (cycl F A B C))
(assert (perp F mBD B D))
(assert (oppSides F C A B))

(assert (midp mCE C E))
(assert (cycl G A B C))
(assert (perp G mCE C E))
(assert (oppSides G B A C))

(confirm (para D E F G))
