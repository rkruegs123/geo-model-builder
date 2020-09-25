(declare-points A B C I Ia D X)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (excenter Ia A B C))
(assert (foot D I B C))
(assert (foot X Ia B C))

(prove (cong B X C D))
(prove (cong B D C X))