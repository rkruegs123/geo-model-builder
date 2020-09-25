(declare-points A B C I X Y Z)

;; Triangle ABC has incenter I
(assert (triangle A B C))
(assert (incenter I A B C))

;; X, Y, and Z are the incenters of the triangles BIC, CIA, and AIB, respectively
(assert (incenter X B I C))
(assert (incenter Y C I A))
(assert (incenter Z A I B))

;; Let triangle XYZ be equilateral
(assert (cong X Y X Z))
(assert (cong X Y Y Z))

;; Prove that ABC is equilateral too
(prove (cong A B A C))
(prove (cong A B B C))