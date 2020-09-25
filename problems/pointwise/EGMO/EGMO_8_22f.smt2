(declare-points A B C D G P Q G1 R S)

;; ABCD is a trapezoid with AB || CD
(assert (polygon A B C D))
(assert (para A B C D))

;; G lies inside BCD
(assert (insidePolygon G B C D))

;; Rays AG and BG meet (ABCD) again at points P and Q, respectively
(assert (onRay P A G))
(assert (onRay Q B G))
(assert (cycl P A C D))
(assert (cycl Q B C D))

;; The line through G parallel to AB intersects BD and BC at R and S, respectively
(assert (para G R A B))
(assert (coll R B D))
(assert (coll S G R))
(assert (coll S B C))

;; Prove that PQRS is cyclic if BG bisects CBD
(assert (ibisector G C B D))
(prove (cycl P Q R S))