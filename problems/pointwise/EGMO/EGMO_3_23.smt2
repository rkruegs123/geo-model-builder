(declare-points A B C X Y Aux1 Z D E Aux2 F Aux3)

(assert (triangle A B C))

;; AX, BY, CZ are concurrent cevians of ABC
(assert (onSeg X B C))
(assert (onSeg Y C A))
(assert (interLL Aux1 A X B Y))
(assert (onSeg Z A B))
(assert (coll Aux1 C Z))

;; XD, YE, ZF are concurrent cevians of XYZ
(assert (onSeg D Y Z))
(assert (onSeg E Z X))
(assert (interLL Aux2 X D Y E))
(assert (onSeg F X Y))
(assert (coll Aux2 Z F))

;; Prove that rays AD, BE, CF concur
(assert (onRay Aux3 A D))
(assert (onRay Aux3 B E))
(prove (onRay Aux3 C F))