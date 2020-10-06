(declare-points A B C D P)

(assert (polygon A B C D))
(assert (insidePolygon P A B C D))

(assert (eq (div (uangle P A D) (uangle P B A)) 0.5))
(assert (eq (div (uangle P A D) (uangle D P A)) (div 1 3)))

(assert (eq (div (uangle C B P) (uangle B A P)) 0.5))
(assert (eq (div (uangle C B P) (uangle B P C)) (div 1 3)))