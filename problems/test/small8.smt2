(param (A B C D) polygon)
(let E line (reflect-ll (line C D) (line A B)))
(eval (coll A B C))
