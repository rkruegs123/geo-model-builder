(param (A B C D) polygon)
(compute E line (reflect-ll (line C D) (line A B)))
(eval (coll A B C))
