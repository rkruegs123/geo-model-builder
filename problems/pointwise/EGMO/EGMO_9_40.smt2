(declare-points A B C I D E F K)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))

(assert (interLL K E F B C))
(prove (perp I K A D))