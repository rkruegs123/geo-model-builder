(declare-points A B C I D P)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot P I A D))
(prove (eqangle B P P D D P P C))