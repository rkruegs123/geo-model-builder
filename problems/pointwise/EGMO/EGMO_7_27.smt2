(declare-points A B C D E F X1 X2 X3)

(assert (cycl A B C D))
(assert (cycl A B C E))
(assert (cycl A B C F))

;; Prove that the three intersections of lines AB and DE, BC and EF, and CD and FA are collinear
(assert (interLL X1 A B D E))
(assert (interLL X2 B C E F))
(assert (interLL X3 C D F A))

(prove (coll X1 X2 X3))