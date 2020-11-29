(param (A B C) acute-tri)
(param P point (on-seg B C))
(param Q point (on-seg B C))

(assert (= (uangle P A B) (uangle B C A)))
(assert (= (uangle C A Q) (uangle A B C)))

;; (assert (eq-angle P A A B B C C A))
;; (assert (eq-angle C A A Q A B B C))

(let M point (midp-from P A))
(let N point (midp-from Q A))

(eval (on-circ (inter-ll (line B M) (line C N)) (circumcircle A B C)))