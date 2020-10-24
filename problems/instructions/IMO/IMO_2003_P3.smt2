(param (A B C D E F) polygon)

;; AB and DE
(assert (= (dist (midp A B) (midp D E)) (mul (div (sqrt 3) 2) (add (dist A B) (dist D E)))))

;; BC and EF
(assert (= (dist (midp B C) (midp E F)) (mul (div (sqrt 3) 2) (add (dist B C) (dist E F)))))

;; CD and FA
(assert (= (dist (midp C D) (midp F A)) (mul (div (sqrt 3) 2) (add (dist C D) (dist F A)))))

(eval (eq (uangle A B C) (uangle B C D)))
(eval (eq (uangle A B C) (uangle C D E)))
(eval (eq (uangle A B C) (uangle D E F)))
(eval (eq (uangle A B C) (uangle E F A)))
(eval (eq (uangle A B C) (uangle F A B)))
