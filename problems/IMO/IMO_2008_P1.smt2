(param (A B C) acute-tri)
(let H point (orthocenter A B C))

(let A1 point (inter-lc (line B C) (coa (midp B C) H) rs-arbitrary))
(let A2 point (inter-lc (line B C) (coa (midp B C) H) (rs-neq A1)))

(let B1 point (inter-lc (line C A) (coa (midp C A) H) rs-arbitrary))
(let B2 point (inter-lc (line C A) (coa (midp C A) H) (rs-neq B1)))

(let C1 point (inter-lc (line A B) (coa (midp A B) H) rs-arbitrary))
(let C2 point (inter-lc (line A B) (coa (midp A B) H) (rs-neq C1)))

(eval (cycl A1 A2 B1 B2 C1 C2))