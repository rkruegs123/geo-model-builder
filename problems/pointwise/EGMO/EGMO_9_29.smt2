(declare-points A B C D E F X1 X2 X3)

;;(assert (polygon A B C))
(assert (cycl A B C D))
(assert (cycl A B C E))
(assert (cycl A B C F))

(assert (interLL X1 A B D E))
(assert (interLL X2 B C E F))
(assert (interLL X3 C D F A))

(prove (coll X1 X2 X3))
