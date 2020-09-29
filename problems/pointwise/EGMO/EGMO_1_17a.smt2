(declare-points A B C H X Mbc Y)

(assert (triangle A B C))
(assert (orthocenter H A B C))

;; Let X be the reflection of H over BC
(assert (cong B X B H))
(assert (perp X H B C))

;; Let Y be the reflection of H over the midpoint of BC
(assert (midp Mbc B C))
(assert (midp Mbc H Y))

;; Prove that X lies on (ABC)
(confirm (cycl X A B C))