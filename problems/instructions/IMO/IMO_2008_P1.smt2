(param (A B C) acute-tri)
(compute H point (orthocenter A B C))

(compute A1 point (inter-lc (line B C) (coa (midp B C) H) rs-arbitrary))
(compute A2 point (inter-lc (line B C) (coa (midp B C) H) (rs-neq A1)))

(compute B1 point (inter-lc (line C A) (coa (midp C A) H) rs-arbitrary))
(compute B2 point (inter-lc (line C A) (coa (midp C A) H) (rs-neq B1)))

(compute C1 point (inter-lc (line A B) (coa (midp A B) H) rs-arbitrary))
(compute C2 point (inter-lc (line A B) (coa (midp A B) H) (rs-neq C1)))

(eval (cycl A1 A2 B1 B2 C1 C2))