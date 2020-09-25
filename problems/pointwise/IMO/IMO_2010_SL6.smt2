(declare-points A B C X Y Z I)

;; vertices X, Y, Z of an equilateral triangle XYZ lie respectively on the sides BC, CA, AB of an
;; acute-angled triangle ABC
(assert (triangle A B C))
(assert (acutes A B C))

(assert (cong X Y X Z))
(assert (cong X Y Y Z))
(assert (onSeg X B C))
(assert (onSeg Y C A))
(assert (onSeg Z A B))

;; Prove that the incenter of ABC lies inside XYZ
(assert (incenter I A B C))

(prove (insidePolygon I X Y Z))
