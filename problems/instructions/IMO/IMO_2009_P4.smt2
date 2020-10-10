;; Note that the following causes a NaN
;; (param (A B C) (isoTri A))

(param (A B C) triangle)
(assert (cong A B A C))

(compute D point (interLL (ibisector C A B) (line B C)))
(compute E point (interLL (ibisector A B C) (line C A)))

(compute K point (incenter A D C))
(assert (eq (uangle B E K) (div pi 4)))