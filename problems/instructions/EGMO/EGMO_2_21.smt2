(param O1 coords)
(param O2 coords)
(param X coords)
(let Y (interCC (coa O1 X) (coa O2 X) (rsNeq X)))

(param P (onCirc (coa O2 X)))
(let Q (interLC (line O1 P) (coa O2 X) (rsNeq P)))

(param R (onCirc (coa O1 X)))
(let S (interLC (line O2 R) (coa O1 X) (rsNeq R)))

(assert (cycl P Q R S))
(confirm (onLine (circumcenter P Q R) (line X Y)))
