(declare-points A B C P Q R OA OB OC X Y Z)

(assert (triangle A B C))

(assert (onSeg P B C))
(assert (onSeg Q C A))
(assert (onSeg R A B))

(assert (circumcenter OA A Q R))
(assert (circumcenter OB B R P))
(assert (circumcenter OC C P Q))

;; AP intersects omegaA omegaB omegaC again at X, Y, Z, respectively
(assert (onSeg X A P))
(assert (onSeg Y A P))
(assert (onSeg Z A P))
(assert (cycl X A Q R))
(assert (cycl Y B R P))
(assert (cycl Z C P Q))

(prove (eqratio Y X X Z B P P C))