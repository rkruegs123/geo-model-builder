(param (A B C) acute-tri)
(assert (not (cong A B A C)))

(define I point (incenter A B C))

(define omega circle (incircle A B C))
(define D point (inter-lc (line B C) omega rs-arbitrary))
(define E point (inter-lc (line C A) omega rs-arbitrary))
(define F point (inter-lc (line A B) omega rs-arbitrary))

(define R point (inter-lc (perp-at D (line E F)) omega (rs-neq D)))
(define P point (inter-lc (line A R) omega (rs-neq R)))
(define Q point (inter-cc (circ P C E) (circ P B F) (rs-neq P)))

(eval (concur (line D I) (line P Q) (perp-at A (line A I))))
