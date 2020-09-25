(declare-points A B C D P Q R X1 X2 Y1 Y2 Aux)

(assert (polygon A B C D))

(assert (interLL P A D B C))
(assert (interLL Q A B C D))
(assert (interLL R A C B D))

(assert (interLL X1 P R A D))
(assert (interLL X2 P R B C))
(assert (interLL Y1 Q R A B))
(assert (interLL Y2 Q R C D))

(assert (interLL Aux X1 Y1 X2 Y2))
(prove (coll Aux P Q))