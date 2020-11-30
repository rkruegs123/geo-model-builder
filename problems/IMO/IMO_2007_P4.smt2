(param (A B C) triangle)
(define R point (inter-lc (i-bisector B C A) (circumcircle A B C) (rs-neq C)))
(define P point (inter-ll (i-bisector B C A) (perp-bis B C)))
(define Q point (inter-ll (i-bisector B C A) (perp-bis A C)))
(define K point (midp B C))
(define L point (midp A C))
(eval (= (area R P K) (area R Q L)))