(declare-points A B C H D E F S T U)

(assert (triangle A B C))
(assert (orthocenter H A B C))

(assert (cycl D A B C))
(assert (cycl E A B C))
(assert (cycl F A B C))
(assert (para A D B E))
(assert (para A D C F))

;; S, T, U are the reflections of D, E, and F across lines BC, CA, and AB

(assert (perp S D B C))
(assert (cong B S B D))

(assert (perp T E C A))
(assert (cong C T C E))

(assert (perp U F A B))
(assert (cong A U A F))

;; Prove that S, T, U and H are concyclic
(prove (cycl S T U H))
