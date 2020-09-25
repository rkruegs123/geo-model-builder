(declare-points A B C H)

(assert (triangle A B C))
(assert (orthocenter H A B C))
(prove (orthocenter A H B C))