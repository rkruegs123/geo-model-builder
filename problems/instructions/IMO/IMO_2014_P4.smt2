(param (A B C) acuteTri)
(param P point (onSeg B C))
(param Q point (onSeg B C))

(assert (= (uangle P A B) (uangle B C A)))
(assert (= (uangle C A Q) (uangle A B C)))

;; (assert (eqangle P A A B B C C A))
;; (assert (eqangle C A A Q A B B C))

(compute M point (midpFrom P A))
(compute N point (midpFrom Q A))

(confirm (onCirc (interLL (line B M) (line C N)) (circumcircle A B C)))