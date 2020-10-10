(param (A B C) acuteTri)
(compute H point (orthocenter A B C))

(compute A1 point (interLC (line B C) (coa (midp B C) H) rsArbitrary))
(compute A2 point (interLC (line B C) (coa (midp B C) H) (rsNeq A1)))

(compute B1 point (interLC (line C A) (coa (midp C A) H) rsArbitrary))
(compute B2 point (interLC (line C A) (coa (midp C A) H) (rsNeq B1)))

(compute C1 point (interLC (line A B) (coa (midp A B) H) rsArbitrary))
(compute C2 point (interLC (line A B) (coa (midp A B) H) (rsNeq C1)))

(confirm (cycl A1 A2 B1 B2 C1 C2))