(param (A B C D) polygon)
(assert (eqratio A B B C D A C D))
(param X point (inPoly A B C D))
(assert (eqangle X A A B X C C D))
(assert (eqangle X B B C X D D A))

(confirm (eq (add (uangle B X A) (uangle D X C)) pi))