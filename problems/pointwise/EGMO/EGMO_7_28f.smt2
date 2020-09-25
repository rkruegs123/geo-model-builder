(declare-points A B C D I1 I2 K)

(assert (triangle A B C))
(assert (onSeg D B C))

(assert (incenter I1 A B D))
(assert (incenter I2 A C D))

(assert (interLL K B I2 C I1))

;; Prove that if AD is the angle bisector of angle A, then K lies on AD
(assert (ibisector D B A C))
(prove (onSeg K A D))