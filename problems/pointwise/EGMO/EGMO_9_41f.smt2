(declare-points A B C X Y Z Aux X1 X2 X3)

;; (temp workaround)
(assert (polygon A B C X Y Z))
;; (assert (triangle X Y Z))

;; If lines AX, BY, and CZ concur, then the following intersection points are collinear
(assert (interLL Aux A X B Y))
(assert (coll Aux C Z))

(assert (interLL X1 A B X Y))
(assert (interLL X2 B C Y Z))
(assert (interLL X3 C A Z X))
(prove (coll X1 X2 X3))
