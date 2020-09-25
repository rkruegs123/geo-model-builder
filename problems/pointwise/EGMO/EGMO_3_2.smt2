(declare-points A B C D)

(assert (triangle A B C))
(assert (onSeg D B C))
(assert (ibisector D B A C))

(prove (eqratio A B A C D B D C))