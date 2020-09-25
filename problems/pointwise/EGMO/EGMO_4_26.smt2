(declare-points A B C O X K D Mbc Aux)

(assert (triangle A B C))

;; Let X be the intersection of the tangents to (ABC) at B and C
(assert (circumcenter O A B C))
(assert (perp O B B X))
(assert (perp O C C X))

;; Let AX meet (ABC) at again at K at BC at D
(assert (cycl K A B C))
(assert (coll K A X))
(assert (interLL D A X B C))

;; Prove that AD is the A-symmedian
(assert (midp Mbc B C))
(assert (isogonal Aux Mbc A B C))
(prove (coll D Aux A))

;; FIXME: Prove a-g