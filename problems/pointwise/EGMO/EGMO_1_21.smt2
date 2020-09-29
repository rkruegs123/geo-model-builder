(declare-points A B C H)

(assert (triangle A B C))
(assert (orthocenter H A B C))
(confirm (orthocenter A H B C))