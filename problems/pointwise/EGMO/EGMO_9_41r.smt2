(declare-points A B C X Y Z X1 X2 X3 Aux)

(assert (triangle A B C))
;; (assert (triangle X Y Z))

;; If the following intersection points are collinear, then AX, BY, and CZ concur
(assert (interLL X1 A B X Y))
(assert (interLL X2 B C Y Z))
(assert (interLL X3 C A Z X))
(assert (coll X1 X2 X3))

(assert (interLL Aux A X B Y))
(prove (coll Aux C Z))
