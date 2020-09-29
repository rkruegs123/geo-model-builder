(declare-points A B C D I1 I2)

(assert (polygon A B C D))
(assert (cycl A B C D))

(assert (incenter I1 A B C))
(assert (incenter I2 D B C))

(confirm (cycl I1 I2 B C))