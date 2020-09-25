(declare-points A B C H X Mbc Y O)

(assert (triangle A B C))
(assert (orthocenter H A B C))

;; Let X be the reflection of H over BC
(assert (cong B X B H))
(assert (perp X H B C))

;; Let Y be the reflection of H over the midpoint of BC
(assert (midp Mbc B C))
(assert (midp Mbc H Y))

;; Show that AY is a diameter of ABC
(assert (circumcenter O A B C))
(prove (coll O A Y))
(prove (cycl Y A B C))