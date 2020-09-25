(declare-points A B C O X Mbc Aux)

(assert (triangle A B C))

;; Let X be the intersection of the tangents to (ABC) at B and C
(assert (circumcenter O A B C))
(assert (perp O B B X))
(assert (perp O C C X))

(assert (midp Mbc B C))

;; Prove that AX is a symmedian
(assert (isogonal Aux Mbc A B C))
(prove (coll X Aux A))
