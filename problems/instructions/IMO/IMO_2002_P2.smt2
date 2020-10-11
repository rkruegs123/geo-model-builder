(param B point)
(param C point)
(compute O point (midp B C))

(param A point (onCirc (coa O B)))
(assert (gt (uangle A O C) (div pi 3)))

(compute E point (interLC (perpBis A O) (coa O B) rsArbitrary))
(compute F point (interLC (perpBis A O) (coa O B) (rsNeq E)))

(compute D point (amidpOpp A B C))
(compute J point (interLL (paraAt O A D) (line A C)))

(confirm (incenter J C E F))