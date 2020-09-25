(declare-points A B C D I1 I2 K)

(assert (triangle A B C))
(assert (onSeg D B C))

(assert (incenter I1 A B D))
(assert (incenter I2 A C D))

(assert (interLL K B I2 C I1))

;; Prove that if K lies on AD, then AD is the angle bisector of angle A
(assert (onSeg K A D))
(prove (ibisector D B A C))
