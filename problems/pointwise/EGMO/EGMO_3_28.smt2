(declare-points A B C H O M N P Q R)

(assert (triangle A B C))
(assert (circumcenter O A B C))
(assert (orthocenter H A B C))

;; M and N are the midpoints of AB and AC, respectively
(assert (midp M A B))
(assert (midp N A C))

;; Rays MH and NH meet (ABC) at P and Q, respectively
(assert (cycl P A B C))
(assert (onRay P M H))

(assert (cycl Q A B C))
(assert (onRay Q N H))

;; Lines MN and PQ meet at R
(assert (interLL R M N P Q))

;; Prove that OA is perpendicular to RA
(prove (perp O A R A))
