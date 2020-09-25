(declare-points A B C H O M N P Q R)

(assert (triangle A B C))
(assert (acutes A B C))
(assert (orthocenter H A B C))
(assert (circumcenter O A B C))

(assert (midp M A B))
(assert (midp N A C))

(assert (onRay P M H))
(assert (cycl P A B C))

(assert (onRay Q N H))
(assert (cycl Q A B C))

(assert (interLL R M N P Q))

(prove (perp O A R A))