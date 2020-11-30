;; Note that the following causes a NaN
;; (param (A B C) (iso-tri A))

(param (A B C) triangle)
(assert (cong A B A C))

(define D point (inter-ll (i-bisector C A B) (line B C)))
(define E point (inter-ll (i-bisector A B C) (line C A)))

(define K point (incenter A D C))
(assert (= (uangle B E K) (div pi 4)))