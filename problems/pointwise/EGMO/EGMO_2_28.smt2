(declare-points A B C P Q R S)

(assert (triangle A B C))
(assert (onSeg P A B))
(assert (onSeg Q A C))
(assert (cong A P A Q))

(assert (onSeg R B C))
(assert (onSeg S B R))
(assert (eqangle B P P S P R R S))
(assert (eqangle C Q Q R Q S S R))

(prove (cycl P Q R S))