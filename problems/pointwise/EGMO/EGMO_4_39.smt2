;; Oa is the center of the A-mixtilinear circle
;; O is the circumcenter of ABC

(declare-points A B C O Oa Mbc T I S)

;; ABC is a triangle
(assert (triangle A B C))
(assert (circumcenter O A B C))
(assert (incenter I A B C))
(assert (mixtilinearIncenter Oa A B C))

(assert (cycl T A B C))
(assert (onSeg Oa O T))

(assert (cycl S T B C))
(assert (onSeg I T S))

(assert (amidpOpp Mbc B C A))

(prove (amidpSame S B C A))
