(param (A B C D) polygon)
(define E line (reflect-ll (line C D) (line A B)))
(eval (coll A B C))
