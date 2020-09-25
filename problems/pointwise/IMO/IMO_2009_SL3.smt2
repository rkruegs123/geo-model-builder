(declare-points A B C I Y Z G R S)

;; ABC is a triangle
(assert (triangle A B C))

;; The incircle of ABC touches AB and AC at Z and Y, respectively
(assert (incenter I A B C))
(assert (onSeg Z A B))
(assert (onSeg Y A C))
(assert (perp I Y A C))
(assert (perp I Z A B))

;; Let G be the point where the lines BY and CZ meet
(assert (interLL G B Y C Z))

;; Let R and S be points s.t. the two quadrilaterals BCYR and BCSZ are parallelograms
(assert (para B C Y R))
(assert (para B R C Y))
(assert (para B C S Z))
(assert (para B Z C S))

;; Prove that GR = GS
(prove (cong G R G S))
