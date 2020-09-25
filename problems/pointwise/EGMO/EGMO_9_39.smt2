(declare-points A B C D O P C1 Q R E)

(assert (polygon A B C D))
(assert (cycl A B C D))

(assert (circumcenter O A B C))

(assert (onRay P A C))
(assert (perp O B B P))
(assert (perp O D D P))

(assert (perp C C1 O C))
(assert (interLL Q C C1 P D))
(assert (interLL R C C1 A D))

(assert (coll E A Q))
(assert (cong O A O E))

(prove (coll B E R))