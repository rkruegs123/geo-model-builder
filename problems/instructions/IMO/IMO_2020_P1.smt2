(param (A B C D) polygon)
(param P point (in-poly A B C D))

(assert (= (div (uangle P A D) (uangle P B A)) 0.5))
(assert (= (div (uangle P A D) (uangle D P A)) (div 1 3)))

(assert (= (div (uangle C B P) (uangle B A P)) 0.5))
(assert (= (div (uangle C B P) (uangle B P C)) (div 1 3)))

(eval (concur (i-bisector A D P) (i-bisector P C B) (perp-bis A B)))