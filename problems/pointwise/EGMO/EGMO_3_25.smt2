;; Identical to 8.12

(declare-points A B C D E Eab Ebc Ecd Eda)

(assert (polygon A B C D))

;; The diagonals of ABCD AC and BD are perpendicular and intersect at E
(assert (perp A C B D))
(assert (interLL E A C B D))

;; Prove that the reflections of E across AB, BC, CD, DA are concyclic
(assert (cong A E A Eab))
(assert (perp A B E Eab))

(assert (cong B E B Ebc))
(assert (perp B C E Ebc))

(assert (cong C E C Ecd))
(assert (perp C D E Ecd))

(assert (cong D E D Eda))
(assert (perp D A E Eda))

(prove (cycl Eab Ebc Ecd Eda))