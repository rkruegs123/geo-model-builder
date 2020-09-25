(declare-points A B C D E W X Y Z)

(assert (polygon A B C D))
(assert (perp A C B D))
(assert (interLL E A C B D))

;; Prove that the reflections of E across AB, BC, CD, DA are concyclic
(assert (cong A E A W))
(assert (perp A B E W))

(assert (cong B E B X))
(assert (perp B C E X))

(assert (cong C E C Y))
(assert (perp C D E Y))

(assert (cong D E D Z))
(assert (perp D A E Z))

(prove (cycl W X Y Z))