(param (A B C D E F) polygon)

;; AB and DE
(assert (eqN (dist (midp A B) (midp D E)) (mul (div (sqrt 3) 2) (add (dist A B) (dist D E)))))

;; BC and EF
(assert (eqN (dist (midp B C) (midp E F)) (mul (div (sqrt 3) 2) (add (dist B C) (dist E F)))))

;; CD and FA
(assert (eqN (dist (midp C D) (midp F A)) (mul (div (sqrt 3) 2) (add (dist C D) (dist F A)))))

;; (confirm (eqangle A B B C B C C D))
;; (confirm (eqangle A B B C C D D E))
;; (confirm (eqangle A B B C D E E F))
;; (confirm (eqangle A B B C E F F A))
;; (confirm (eqangle A B B C F A A B))
