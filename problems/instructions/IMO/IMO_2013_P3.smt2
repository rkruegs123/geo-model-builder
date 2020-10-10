(param (A B C) (rightTri A))

(param A1 point (onCirc (excircle A B C)))
(assert (tangentAt A1 (line B C) (excircle A B C)))
;; (compute A1 point (interLC (line B C) (excircle A B C) rsArbitrary))

(param B1 point (onCirc (excircle B A C)))
(assert (tangentAt B1 (line C A) (excircle B A C)))

(param C1 point (onCirc (excircle C B A)))
(assert (tangentAt C1 (line A B) (excircle C B A)))

(assert (onCirc (circumcenter A1 B1 C1) (circumcircle A B C)))

;; (confirm (rightTri A B C))
