;; (a) - P lies in both of the segments AB and XY
;; (b) - P lies in neither of the segments AB and XY

(declare-points A B X Y P)

(assert (interLL P A B X Y))
(assert (not (onSeg P A B)))
(assert (not (onSeg P X Y)))

(assert (eqratio P B P X P Y P A))
(prove (cycl A B X Y))
