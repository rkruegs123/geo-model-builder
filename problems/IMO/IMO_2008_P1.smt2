(param (A B C) acute-tri)
(define H point (orthocenter A B C))

(define A1 point (inter-lc (line B C) (coa (midp B C) H) rs-arbitrary))
(define A2 point (inter-lc (line B C) (coa (midp B C) H) (rs-neq A1)))

(define B1 point (inter-lc (line C A) (coa (midp C A) H) rs-arbitrary))
(define B2 point (inter-lc (line C A) (coa (midp C A) H) (rs-neq B1)))

(define C1 point (inter-lc (line A B) (coa (midp A B) H) rs-arbitrary))
(define C2 point (inter-lc (line A B) (coa (midp A B) H) (rs-neq C1)))

(eval (cycl A1 A2 B1 B2 C1 C2))