(param (A B C) triangle)

(define P point (inter-ll (i-bisector B A C) (line B C)))
(define Q point (inter-ll (i-bisector A B C) (line C A)))

(assert (= (uangle B A C) (div pi 3)))
(assert (= (add (dist A B) (dist B P)) (add (dist A Q) (dist Q B))))